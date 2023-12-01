FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5002", "app:app"]

