"""gleeb: goal and information-flow monitors for multi-agent transcripts.

Import the data model from here; parsers live in gleeb.parsers and are imported explicitly.
"""

from gleeb.schema import (
    Agent,
    Alignment,
    AppendBoard,
    Blackboard,
    BlackboardOp,
    BlackboardUniverse,
    BoardEntry,
    DMThread,
    Event,
    ExternalBoard,
    FileBoard,
    FlowEdge,
    GoalSpan,
    GoalStream,
    MessageBoard,
    SpanMatch,
    ToolInfo,
    Trace,
)

__version__ = "0.1.0"

__all__ = [
    "Agent", "Alignment", "AppendBoard", "Blackboard", "BlackboardOp", "BlackboardUniverse",
    "BoardEntry", "DMThread", "Event", "ExternalBoard", "FileBoard", "FlowEdge", "GoalSpan",
    "GoalStream", "MessageBoard", "SpanMatch", "ToolInfo", "Trace",
]
