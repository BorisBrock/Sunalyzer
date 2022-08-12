# https://betterprogramming.pub/how-to-create-a-dockerfile-for-a-python-application-8d078b16bc9a

FROM python:3.11.0b5-slim-bullseye

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

COPY data data
COPY backend grabber
COPY site site

COPY run.sh .
RUN chmod a+x run.sh

RUN rm /data/db.sqlite || true


# Usage: VOLUME ["/dir_1", "/dir_2" ..]
VOLUME ["/data"]

EXPOSE 5000


ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./run.sh"]