#   This is Chase trying to figure out docker. Give him time. #
FROM python:3.8.2

# Update apps on the base image
RUN apt -y update && apt-get install -y nodejs npm

# Install required programs / libs
RUN pip install selectors requests

# Delete git
RUN apt remove -y git

#   Copies current folder we're in and puts inside of image #
COPY . /usr/src/errors

COPY ./avocat /usr/src/errors/avocat

WORKDIR /usr/src/errors

RUN python avocat/main.py npm install https://github.com/visionmedia/express 2>&1 > output.txt

