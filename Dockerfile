# Get the base Ubuntu image from Docker Hub
FROM ubuntu:latest

# Update apps on the base image
RUN apt-get -y update && apt-get install -y

# Install required programs / libs
RUN apt-get -y install g++ libncurses5-dev libncursesw5-dev make

# Copy the current folder which contains C++ source code to the Docker image under /usr/src
COPY . /usr/src/avocat

# Specify the working directory
WORKDIR /usr/src/avocat

# Use Clang to compile the avocat.cpp source file
RUN make
