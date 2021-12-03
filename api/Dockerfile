# 1 
FROM python:3.8.6

RUN pip -V
# 2
RUN pip install -r requirements.txt

# 3
COPY ../skillQuery-api/ /app
WORKDIR /app

# 4
ENV PORT 8080

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app