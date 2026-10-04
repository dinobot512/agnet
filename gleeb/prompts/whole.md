
Task: segment the whole list into consecutive spans, one goal each, at the requested level.
Together the spans must cover every item, in order, without gaps or overlaps.
- List spans in order. Each span gives the range (start_lo, start_hi) of item indices where it
  begins. The first span begins at the first item (start_lo = start_hi = first index).
  Each later span's start range must come after the previous span's start range.
- goal: the goal of the span, as an outcome.
- confidence: 0-1.
- evidence: item indices that support the goal (at least one).
If the goal never changes, return a single span.
