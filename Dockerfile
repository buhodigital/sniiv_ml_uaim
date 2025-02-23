FROM --platform=linux/amd64 python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libffi-dev \
        libpq-dev \
        python3-dev && \
    pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python", "manage.py", "runserver","0.0.0.0:8080"]