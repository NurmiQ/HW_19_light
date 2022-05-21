FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./views ./views
COPY volumes/movies.db .
COPY app.py .
COPY config.py .
COPY constants.py .
COPY models.py .
COPY setup_db.py .

CMD flask run -h 0.0.0.0 -p 80