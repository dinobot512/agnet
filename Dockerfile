FROM python:3.12-slim

RUN useradd -m -s /bin/bash agent

WORKDIR /workspace

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY dev.md memory.md agent.py ./

RUN chmod 444 dev.md \
 && chown agent:agent memory.md agent.py \
 && chmod 644 memory.md

USER agent

CMD ["python", "agent.py"]
