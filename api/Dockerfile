FROM python:3.9.9-alpine3.15

ENV PYTHONUNBUFFERED 1

ARG GIT_VERSION
ARG GIT_BRANCH
ARG GIT_LASTCOMMITDATE

ENV VITE_APP_VERSION=$GIT_VERSION
ENV VITE_APP_BRANCH=$GIT_BRANCH
ENV VITE_APP_LASTCOMMITDATE=$GIT_LASTCOMMITDATE

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev git bash
RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev libffi-dev
RUN apk --no-cache add nodejs yarn --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community
RUN rm -f package.json yarn.lock
RUN pip --disable-pip-version-check install --upgrade pip
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user