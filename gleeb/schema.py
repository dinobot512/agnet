"""Data model for gleeb. Data only; pipeline stages live in goals/flow/align/score.

Ordering: Event.seq is the global event axis every output refers to. Event.turn is the agent's own
turn index (one model response plus the tool results returned for it), comparable within an agent.
References between objects are by id, never back-pointers. Ground truth never appears here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Literal

BlackboardKind = Literal["file", "dm", "board", "external"]
EventKind = Literal["reasoning", "text", "tool_call", "tool_result", "message_in", "external"]
Channel = Literal["expressed", "behavioral", "all"]
Level = Literal["objective", "step"]


# --- input: what parsers produce --------------------------------------------------------------

@dataclass(frozen=True)
class Agent:
    id: str
    name: str = ""
    model: str = ""                           # provider model ID, "" if unknown
    aliases: tuple[str, ...] = ()
    meta: dict = field(default_factory=dict)  # parser-specific extras


@dataclass(frozen=True)
class ToolInfo:
    name: str
    call_id: str                              # pairs a tool_call with its tool_result
    args: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Event:
    seq: int
    agent: str
    turn: int
    kind: EventKind
    content: str = ""
    t: float = 0.0                            # wall clock seconds, if known
    tool: ToolInfo | None = None
    source: Literal["thinking", "assistant_text"] | None = None   # for reasoning/text
    ref: str = ""                             # pointer to the raw source line


@dataclass
class Trace:
    id: str
    agents: dict[str, Agent]
    events: list[Event]

    def __post_init__(self) -> None:
        self.events.sort(key=lambda e: e.seq)

    def of_kind(self, agent: str, *kinds: EventKind) -> list[Event]:
        return [e for e in self.events if e.agent == agent and e.kind in kinds]


# --- goals: each monitor segments the event axis independently ------------------------------

@dataclass
class GoalSpan:
    """An interval of the event axis with one goal. A stream's spans (per level) partition it.

    start/end are ranges (earliest, latest) of Event.seq: where the boundary could be, given the
    evidence. Span k's end range is the event just before each end of span k+1's start range.
    """
    id: str
    agent: str
    stream: Channel
    start: tuple[int, int]
    end: tuple[int, int]
    goal: str                                 # the outcome being pursued (what would count as done)
    level: Level = "objective"
    confidence: float = 1.0
    evidence: list[int] = field(default_factory=list)   # Event.seq values

    @staticmethod
    def mid(r: tuple[int, int]) -> float:
        return (r[0] + r[1]) / 2

    def overlap(self, other: GoalSpan) -> int:
        """Shared positions of the outer intervals [start.earliest, end.latest]."""
        return max(0, min(self.end[1], other.end[1]) - max(self.start[0], other.start[0]) + 1)


@dataclass
class GoalStream:
    agent: str
    stream: Channel
    method: str                               # whole | windowed | bullets_whole | bullets_windowed
    codebook: str                             # prompt version + model
    level: Level = "objective"
    sample_id: int = 0
    spans: list[GoalSpan] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)      # validation flags and failures
    meta: dict = field(default_factory=dict)            # e.g. has_thinking, tokens

    @property
    def id(self) -> str:
        return f"{self.agent}:{self.stream}:{self.method}:{self.level}:{self.codebook}:s{self.sample_id}"


@dataclass(frozen=True)
class SpanMatch:
    a: str                                    # GoalSpan.id in stream a
    b: str                                    # GoalSpan.id in stream b
    overlap: int
    start_lag: float                          # mid(b.start) - mid(a.start); a=expressed: >0 means said before done
    end_lag: float
    verdict: str = ""                         # pairwise judge: same | refinement
    reason: str = ""


@dataclass
class Alignment:
    agent: str
    a: str                                    # GoalStream.id
    b: str
    matches: list[SpanMatch] = field(default_factory=list)
    a_only: list[str] = field(default_factory=list)     # e.g. stated, never acted on
    b_only: list[str] = field(default_factory=list)     # e.g. acted on, never explained


# --- flow: every read comes from, and every write goes to, a blackboard ---------------------

@dataclass(frozen=True)
class BlackboardOp:
    """One read or write of one blackboard, produced by ops.classify_ops (rules or LLM)."""
    seq: int                                  # Event.seq: the tool_result for reads, the tool_call for writes
    agent: str
    op: Literal["R", "W"]
    blackboard_id: str                        # "file:brief.md", "dm:inbox:tomas", "board:team", "external:..."
    kind: BlackboardKind
    content: str = ""                         # what was returned (R) or written (W), raw
    content_id: str = ""                      # hash of the normalised content
    source: Literal["rule", "llm"] = "rule"
    confidence: float = 1.0
    call_seq: int = -1                        # Event.seq of the tool_call that produced it


@dataclass(frozen=True)
class BoardEntry:
    seq: int
    agent: str
    op: Literal["R", "W"]
    versions: tuple[str, ...]
    summary: str = ""


@dataclass
class Blackboard:
    """Overwrite semantics: a read sees the latest write."""
    kind: ClassVar[str] = "generic"
    blackboard_id: str
    entries: list[BoardEntry] = field(default_factory=list)

    def reads(self) -> list[BoardEntry]:
        return [e for e in self.entries if e.op == "R"]

    def writes(self) -> list[BoardEntry]:
        return [e for e in self.entries if e.op == "W"]

    def visible_at(self, seq: int) -> tuple[str, ...]:
        prior = [e.versions for e in self.writes() if e.seq <= seq]
        return prior[-1] if prior else ()


@dataclass
class FileBoard(Blackboard):
    kind: ClassVar[str] = "file"


@dataclass
class AppendBoard(Blackboard):
    """Message log: a read sees every message written so far."""
    kind: ClassVar[str] = "append"

    def visible_at(self, seq: int) -> tuple[str, ...]:
        return tuple(v for e in self.writes() if e.seq <= seq for v in e.versions)


@dataclass
class DMThread(AppendBoard):
    kind: ClassVar[str] = "dm"


@dataclass
class MessageBoard(AppendBoard):
    kind: ClassVar[str] = "board"


@dataclass
class ExternalBoard(Blackboard):
    """Unobserved channel; entries are inferred, not logged."""
    kind: ClassVar[str] = "external"


BOARD_TYPES: dict[str, type[Blackboard]] = {
    c.kind: c for c in (Blackboard, FileBoard, AppendBoard, DMThread, MessageBoard, ExternalBoard)
}


@dataclass
class BlackboardUniverse:
    boards: dict[str, Blackboard] = field(default_factory=dict)
    contents: dict[str, str] = field(default_factory=dict)        # content_id -> raw content, stored once

    @classmethod
    def from_ops(cls, ops: list[BlackboardOp]) -> BlackboardUniverse:
        u = cls()
        for o in sorted(ops, key=lambda o: o.seq):
            board = u.boards.setdefault(o.blackboard_id, BOARD_TYPES[o.kind](o.blackboard_id))
            board.entries.append(BoardEntry(o.seq, o.agent, o.op, (o.content_id,)))
            u.contents.setdefault(o.content_id, o.content)
        return u


@dataclass(frozen=True)
class FlowEdge:
    """Information moving from a source op to a destination op.

    transfer    : agent A's write, then agent B's read of the same blackboard. A read whose content
                  (or part of it) no observed write explains gets a transfer edge from an unknown
                  source (from_agent "?", src_seq -1): the blackboard exists, its upstream does not.
    carry       : an agent's read, then its own later write elsewhere containing that content
    unexplained : a write containing content from another agent's earlier write, with no observed path
    """
    from_agent: str
    blackboard_id: str                       # blackboard of the source op
    to_agent: str
    src_seq: int                             # source op (a write, or for carry a read)
    dst_seq: int                             # destination op (a read, or for carry/unexplained a write)
    kind: Literal["transfer", "carry", "unexplained"] = "transfer"
    match: Literal["direct", "exact_copy", "fragment", "unknown"] = "direct"
    score: float = 1.0                       # shared distinctive shingles; unknown source: unexplained words
    to_blackboard: str = ""                  # carry/unexplained: blackboard written
    versions: tuple[str, ...] = ()           # shared content ids (direct)
    evidence: tuple[str, ...] = ()           # Event.ref of source and destination
