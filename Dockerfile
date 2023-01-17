FROM python:3.10 as builder

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip wheel -r requirements.txt -w /wheels

FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --find-links /wheels

COPY . /app

ENV PYTHONPATH /app

CMD ["python3", "main.py"]