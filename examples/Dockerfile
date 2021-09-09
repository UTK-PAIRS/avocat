#   This is Chase trying to figure out docker. Give him time. #
FROM node:latest

# Update apps on the base image
RUN apt-get -y update && apt-get install -y

# Install required programs / libs
RUN apt-get -y install make

#   Copies current folder we're in and puts inside of image #
COPY . /usr/src/errors

WORKDIR /usr/src/errors

