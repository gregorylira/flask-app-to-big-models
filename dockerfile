FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-k", "gevent", "-b", "0.0.0.0:5000", "run:app"]