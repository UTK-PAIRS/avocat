# Avocat
Automatic Shell-Level Monitoring and Error Resolution
University of Tennessee, Knoxville PAIRS Lab

Avocat is a project which seeks to bring cutting-edge error resolution strategies directly into the terminal. Rather than users copying and pasting relevant information from their shell into a search engine, avocat automatically queries its database and Q&A services to suggest immediate resolution strategies.

This project is split into three portions:
1. avocat: this program listens to stdin, stdout, and the return value of its preceding arguments and queries an avocat database upon an error
2. avocat-local: this optional local server acts as an intermediate between the avocat instance and an external database for improved caching and monitoring support
3. avocat-db: this is the database which avocat can query in order to suggest resolution strategies

If you have all of the dependencies installed, you can use the makefile in the root directory to compile all components.

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

Usage:
```
./avocat programname arg1 arg2 ...
```

Example:
```
./avocat echo hi
```

# avocat-local
avocat-local is a system-level server which seeks to mediate database-client interaction and allow for process monitoring (FUTURE FEATURE)

SOON TO BE REWRITTEN IN PYTHON

# avocat-db
avocat-db is the database which serves resolutions suggestions. Currently, it relies solely on Google and StackOverflow.

Dependencies: `libcurl`

Installation instructions:
```
cd avocat-db
pip install -r requirements.txt
python3 server.py
```
