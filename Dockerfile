FROM python:3.9.6-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update && apk upgrade && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --no-cache bash\
                       python3 \
                       pkgconfig \
                       git \
                       gcc \
                       openldap \
                       libcurl \
                       python3-dev \
                       gpgme-dev \
                       libc-dev \
    && rm -rf /var/cache/apk/*
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py
RUN pip3 install setuptools==30.1.0

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install --upgrade pip
RUN pip3 install psycopg2-binary

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
ADD . /app/
COPY entrypoint.sh .

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# copy project
ADD . /app/


ENTRYPOINT ["/app/entrypoint.sh"]