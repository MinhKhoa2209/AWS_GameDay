# hadolint ignore=DL3026
FROM public.ecr.aws/docker/library/python:3.13-alpine
LABEL maintainer="jd"

COPY . /app

WORKDIR /app
RUN pip install --no-cache-dir --requirement requirements.txt

EXPOSE 5000
CMD python ./app/index.py
