FROM debian:bookworm-slim

RUN useradd -m -s /bin/bash agent

WORKDIR /workspace

COPY dev.md ./dev.md
COPY memory.md ./memory.md

# dev.md is read-only; memory.md is owned by the agent
RUN chmod 444 dev.md \
 && chown agent:agent memory.md \
 && chmod 644 memory.md

USER agent

CMD ["bash"]
