FROM python:3

WORKDIR /app

COPY server.py .
COPY worker.py .
COPY start.sh .

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["bash", "start.sh"]
