"""Flow extraction over blackboard ops (from ops.classify_ops): transfer, carry and unexplained edges.

Matching, strongest first:
  direct      same content id
  exact_copy  one text (>= MIN_TEXT chars) contained in the other, after normalisation
  fragment    >= MIN_SHARED shared word K-shingles, excluding a `background` set of common shingles
              (e.g. built from control runs, so phrasing shared by same-model agents is not evidence)
Every read gets an incoming edge: from the writers that explain it, and from an unknown source ("?")
for whatever no observed write explains. Paraphrase (LLM) checks on what remains come later.
"""

from __future__ import annotations

from gleeb.ops import normalize
from gleeb.schema import BlackboardOp, FlowEdge, Trace

UNKNOWN = "?"                                          # from_agent of a read with no observed source
K = 5                                                  # words per shingle
MIN_SHARED = 2                                         # shared distinctive shingles for a fragment match
MIN_TEXT = 20                                          # shortest text that counts as an exact copy


def shingles(text: str) -> set[str]:
    words = normalize(text).lower().split()
    return {" ".join(words[i:i + K]) for i in range(len(words) - K + 1)}


def uncovered(text: str, covered: set[str]) -> tuple[int, int]:
    """(words not inside any covered shingle, longest run of such words)."""
    words = normalize(text).lower().split()
    hit = [False] * len(words)
    for i in range(len(words) - K + 1):
        if " ".join(words[i:i + K]) in covered:
            hit[i:i + K] = [True] * K
    total = run = best = 0
    for h in hit:
        run = 0 if h else run + 1
        total += not h
        best = max(best, run)
    return total, best


def background_from(ops: list[BlackboardOp]) -> frozenset[str]:
    """Shingles seen in other runs (e.g. control): pass to flow_edges to discount common phrasing."""
    return frozenset(s for o in ops for s in shingles(o.content))


def match(src: BlackboardOp, dst: BlackboardOp, background: frozenset[str] = frozenset()) -> tuple[str, float] | None:
    if src.content_id and src.content_id == dst.content_id:
        return "direct", 1.0
    a, b = normalize(src.content), normalize(dst.content)
    short, long = sorted((a, b), key=len)
    if len(short) >= MIN_TEXT and short in long:
        return "exact_copy", 1.0
    shared = (shingles(a) & shingles(b)) - background
    return ("fragment", float(len(shared))) if len(shared) >= MIN_SHARED else None


def before(a: BlackboardOp, b: BlackboardOp) -> bool:
    """a could feed b: a happened earlier, or both come from the same tool call (e.g. `grep | tee`)."""
    return a.seq < b.seq or (a.call_seq >= 0 and a.call_seq == b.call_seq and a.op == "R" and b.op == "W")


def flow_edges(ops: list[BlackboardOp], trace: Trace | None = None,
               background: frozenset[str] = frozenset()) -> list[FlowEdge]:
    refs = {e.seq: e.ref for e in trace.events} if trace else {}
    ops = sorted(ops, key=lambda o: o.seq)
    edges: list[FlowEdge] = []

    def add(src, dst, kind, m, to_board=""):
        versions = (src.content_id,) if m[0] == "direct" else ()
        edges.append(FlowEdge(src.agent, src.blackboard_id, dst.agent, src.seq, dst.seq, kind, m[0], m[1],
                              to_board, versions, (refs.get(src.seq, ""), refs.get(dst.seq, ""))))

    # transfer: A writes, B later reads the same blackboard
    for r in (o for o in ops if o.op == "R"):
        for w in (o for o in ops if o.op == "W" and o.blackboard_id == r.blackboard_id):
            if w.seq < r.seq and w.agent != r.agent and (m := match(w, r, background)):
                add(w, r, "transfer", m)

    # unknown source: what a read returned that no earlier write to that blackboard explains
    for r in (o for o in ops if o.op == "R"):
        prior = [w for w in ops if w.op == "W" and w.blackboard_id == r.blackboard_id and w.seq < r.seq]
        explained = any(match(w, r, background) for w in prior)
        covered = set().union(*(shingles(w.content) for w in prior)) | background
        rest = normalize(r.content)
        for w in prior:                                  # drop text an earlier write fully explains
            rest = rest.replace(normalize(w.content), " ") if normalize(w.content) else rest
        new_words, longest = uncovered(rest, covered)
        if (not explained and normalize(r.content)) or longest >= K:     # a full shingle of new text
            edges.append(FlowEdge(UNKNOWN, r.blackboard_id, r.agent, -1, r.seq, "transfer", "unknown",
                                  float(new_words), "", (), ("", refs.get(r.seq, ""))))

    # carry: an agent reads one blackboard, later writes that content to another; keep the best source
    for w in (o for o in ops if o.op == "W"):
        best: dict[str, tuple] = {}
        for r in (o for o in ops if o.op == "R" and o.agent == w.agent and before(o, w)
                  and o.blackboard_id != w.blackboard_id):
            if (m := match(r, w, background)) and (r.blackboard_id not in best or m[1] >= best[r.blackboard_id][1][1]):
                best[r.blackboard_id] = (r, m)
        for r, m in best.values():
            add(r, w, "carry", m, w.blackboard_id)

    # unexplained: a write shares distinctive shingles with another agent's earlier write that the
    # writer never saw (not in anything it read, wrote or was sent before)
    for w in (o for o in ops if o.op == "W"):
        seen = set(background)
        for o in ops:
            if o.agent == w.agent and o is not w and before(o, w):
                seen |= shingles(o.content)
        if trace:
            for e in trace.events:
                if e.agent == w.agent and e.kind == "message_in" and e.seq < w.seq:
                    seen |= shingles(e.content)
        novel = shingles(w.content) - seen
        if len(novel) < MIN_SHARED:
            continue
        for src in (o for o in ops if o.op == "W" and o.agent != w.agent and o.seq < w.seq):
            shared = novel & shingles(src.content)
            if len(shared) >= MIN_SHARED:
                add(src, w, "unexplained", ("fragment", float(len(shared))), w.blackboard_id)

    return sorted(edges, key=lambda e: (e.dst_seq, e.src_seq))
