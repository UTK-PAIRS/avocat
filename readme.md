# Avocat

Automatic Shell-Level Monitoring and Error Resolution
University of Tennessee, Knoxville PAIRS Lab

Avocat is a project which seeks to bring cutting-edge error resolution strategies directly into the terminal. Rather than users copying and pasting relevant information from their shell into a search engine, avocat automatically queries its database and Q&A services to suggest immediate resolution strategies.

## example

```shell
shell> python3 -mavocat -- echo hi
avocat> $ echo hi
avocat> > hi
```


# avocat

avocat is the program that is called anytime a user wishes for program execution to be monitored. It intercepts the outputs of the program saves a copy into history in system memory, also redirecting to the user. Upon unsuccessful execution, avocat queries either avocat-local or avocat-db for a resolution strategy which is then returned to the user.

This program relies on a few UNIX syscalls, so non-UNIX systems will likely encounter issues.

Dependencies: `libcurl`

Installation instructions:
```
sudo apt-get install libcurl4-openssl-dev
cd avocat
make
../bin/avocat
```

# avocat-local
avocat-local is a system-level server which seeks to mediate database-client interaction and allow for process monitoring (FUTURE FEATURE)

SOON TO BE REWRITTEN IN PYTHON

