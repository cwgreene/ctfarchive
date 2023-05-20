from itertools import islice
from hashlib import sha256 as H
import sys, os

BLOCK_LEN = 16
CHUNK_LEN = 4

def chunk(data):
    return [data[CHUNK_LEN*i:CHUNK_LEN*(i+1)] for i in range(BLOCK_LEN//CHUNK_LEN)]

def compress_chunks(chunks):
    output = b""
    cur = H()
    for chunk in chunks:
        output += H(chunk).digest()[:3]
        cur.update(chunk)
    output += cur.digest()[:3]
    return output

def compress(fdr, fdw):
    assert (os.fstat(fdr.fileno()).st_size) % BLOCK_LEN == 0, f"Input length must be a multiple of {BLOCK_LEN}"
    while (data := fdr.read(BLOCK_LEN)):
        fdw.write(compress_chunks(chunk(data)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} [compress|extract] inputfile")
        exit(-1)
    if sys.argv[1] == "compress":
        with open(sys.argv[2], "rb") as fdr, open(sys.argv[2]+".z1p", "wb") as fdw:
            compress(fdr, fdw)

    elif sys.argv[1] == "extract":
        print("Not implemented")

    else:
        print("Unknown operation")