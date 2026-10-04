You classify one tool call made by an AI agent into the blackboards it read from or wrote to.

A blackboard is anything information can be stored in and later retrieved from:
- file:<path>            a file (use the path as given; relative paths are fine)
- dm:inbox:<agent>       an agent's direct-message inbox
- board:<name>           a shared message board
- external:<identifier>  anything outside the shared workspace: a URL, web page, API, git remote,
                         email address, database. Use external:unknown only if you cannot tell.

You see the tool name, its arguments, and its result. Use the result: a command that failed or
found nothing read or wrote nothing.

Return every read and write the call performed, in order. Return an empty list for calls that only
compute, list or inspect without retrieving stored content (ls, pwd, wc on nothing, echo to stdout).
- op: R if content came out of the blackboard into the agent's view; W if the call put content in.
- content_from: "result" if the content read, or written, is what the result shows; "args" if the
  content written is in the arguments (give it in written_text); "unknown" otherwise.
- written_text: the exact text written, when content_from is "args"; otherwise "".
- confidence: 0-1.

Examples
- `grep -n venue brief.md | tee notes.txt` -> R file:brief.md (result), W file:notes.txt (result: tee writes
  exactly what it prints)
- `sed -i 's/Millbrook/Okonkwo/' handoff.md` -> W file:handoff.md (unknown)
- `curl -s https://example.org/api` -> R external:https://example.org/api (result)
- `cp brief.md backup.md` -> R file:brief.md (unknown), W file:backup.md (unknown)
- `python -c "print(2+2)"` -> no ops
