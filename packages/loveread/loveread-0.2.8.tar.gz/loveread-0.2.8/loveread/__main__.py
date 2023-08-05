#!/usr/bin/env python3
import sys
from .loveread import *

if __name__ == "__main__":
    urls=[]
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        urls=[input("Enter book url from loberead.ec: ")]
    
    for url in urls:
        download(url)
    