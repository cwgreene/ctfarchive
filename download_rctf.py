import requests
import argparse
import json
import os
import sys
import pathlib
from hyper.contrib import HTTP20Adapter

def download(s, source, dest):
    res = s.get(source)
    with open(dest, "wb") as target_file:
        target_file.write(res.content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True, help="session token")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--root-url", required=True, help="url of challenges")
    parser.add_argument("--api-url", action="store_true", default=None)
    parser.add_argument("--root-dir", required=True, help="target output dir")
    options = parser.parse_args()
    session = options.session
    if options.api_url is None:
        options.api_url = f"{options.root_url}/api/v1"

    if not os.path.exists(options.root_dir):
        pathlib.Path(options.root_dir).mkdir(parents=True, exist_ok=True)       
    
    s = requests.Session()
    s.mount(f'{options.api_url}', HTTP20Adapter())

    print(f"Obtaining challenges from {options.api_url}/challs")
    challenges = s.get(f"{options.api_url}/challs", headers = {
                "Cookie": f"session={session}",
            })
    problems = json.loads(challenges.content)

    for chal in problems:
        print(f"Downloading {chal['name']}...")

        # Generate Directory for Challenge (if it doesn't exist)
        target_dir = os.path.join(options.root_dir, chal["name"])
        if not os.path.exists(target_dir):
            print(f"Creating directory {target_dir}...")
            pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)       
            if not os.path.exists(target_dir):
                raise Exception("mkdir failed")

        # Save chal to json
        problem_filename = f"{target_dir}/problem.json"
        if not os.path.exists(problem_filename) or options.force:
            result = json.stringify(chal)
            with open(problem_filename, "wb") as probfile:
                probfile.write(result)
        else:
            with open(problem_filename) as probfile:
                result = probfile.read()
    
        # Load back stringified reuslt (could use chal directly, but this is for
        # consistency with ctfd.
        problem = json.loads(result)
        for f in problem["files"]:
            file_name = f.split("?")[0].split("/")[-1]
            if os.path.exists(f"{target_dir}/{file_name}") and not options.force:
                print(f"'{file_name}' is downloaded")
                continue
            print(f"'{file_name}' is being downloaded...")
            download(s, f"{options.root_url}/{f}", f"{target_dir}/{file_name}")

if __name__ == "__main__":
    main()
