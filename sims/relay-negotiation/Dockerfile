FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN useradd -m -s /bin/bash agent

WORKDIR /workspace

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY agent.py ./

RUN chown -R root:root /workspace && chmod 700 /workspace

CMD ["tail", "-f", "/dev/null"]
