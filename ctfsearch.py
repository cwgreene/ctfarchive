import argparse
import colorama
import os
import json

def find_metadata_files():
    metadata_files = []

    ctfs = []
    # open root metadat file
    with open("metadata.json") as metadata:
        js = json.load(metadata)
        for ctf in js["ctfs"]:
            ctfs.append(os.path.join(ctf, "metadata.json"))
    return ctfs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    options = parser.parse_args()

    metadatafiles = find_metadata_files()

    if options.check:
        for m in metadatafiles:
            if os.path.exists(m):
                print(colorama.Style.BRIGHT + colorama.Fore.GREEN + f"{m} exists")
            else:
                print(colorama.Style.BRIGHT + colorama.Fore.RED + f"{m} does not exists")

if __name__ == "__main__":
    main()
