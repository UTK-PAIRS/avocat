#!/usr/bin/env python3

import sys
from pcontain import PContain
import api
import apikey

def main():
    if len(sys.argv) < 2: return
    
    argv = sys.argv[1:]
    p = PContain(argv)

    print(f"p.ret:\n{p.ret}\n")
    print(f"p.stdout:\n{p.stdout}")
    print(f"p.stderr:\n{p.stderr}")

    if p.ret != 0:
        api.querySO(argv, p.stdout, p.stderr, p.ret, apikey=apikey.so)

if __name__ == "__main__":
    main()
