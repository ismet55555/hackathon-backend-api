###########################################################
#
# This is based on the following work:
#  - https://github.com/tiangolo/uvicorn-gunicorn-docker
#  - https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
#
###########################################################

FROM python:3.11-slim

LABEL maintainer="Ismet Handzic <ismet.handzic@gmail.com"
LABEL description="FastAPI Sample Server"

RUN apt-get update && apt-get -q install -y \
  vim \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean
RUN pip install --no-cache-dir --upgrade pip pipenv

COPY --chmod=0755 ./start.sh /start.sh
COPY --chmod=0755 ./start-dev.sh /start-dev.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY Pipfile* /
RUN pipenv requirements > /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./app /app

ENV PYTHONPATH=/app
ENV PORT=9500
ENV MAX_WORKERS=3

EXPOSE 9500

RUN useradd -ms /bin/bash appuser

COPY --chown=root:root ./.container/ /root/
COPY --chown=appuser:appuser ./.container/ /home/appuser/

USER appuser

CMD ["/start.sh"]
