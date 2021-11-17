# avocat

Automatic Shell-Level Monitoring and Error Resolution
University of Tennessee, Knoxville PAIRS Lab

Avocat is a project which seeks to bring cutting-edge error resolution strategies directly into the terminal. Rather than users copying and pasting relevant information from their shell into a search engine, avocat automatically queries its database and Q&A services to suggest immediate resolution strategies.

## Setup

Avocat is designed to work on any platform Python does. For most platforms, run:

```shell
$ pip3 install -r requirements.txt
```

## Usage

The main way of running avocat (`./avocat.sh`) can be invoked after setup is completed. For example:

```shell
$ ./avocat.sh -h
usage: __main__.py [-h] [-t TEST] [-e STDERR] [-o STDOUT] [-f FILE] [command ...]

avocat: your terminal advocate

positional arguments:
  command               command arguments

optional arguments:
  -h, --help            show this help message and exit
  -t TEST, --test TEST  test number
  -e STDERR, --stderr STDERR
                        path to pregenerated stderr file
  -o STDOUT, --stdout STDOUT
                        path to pregenerated stdout file
  -f FILE, --file FILE  path to the command file to run
```

To run a test (from `./test`):

```shell
$ ./avocat.sh -f test/000.sh

------------------------------------------------
Running Input...
------------------------------------------------

avocat> running file: test/000.sh
out> hi
out> 
err> 

------------------------------------------------
No Problems
------------------------------------------------

avocat> Success!
```

