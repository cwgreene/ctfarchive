import requests
import argparse
import json
import os
import wget
import sys
import pathlib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--root-url", action="store_true", required=True)
    parser.add_argument("--api-url", action="store_true", default=None)
    parser.add_argument("--root-dir", required=True)
    options = parser.parse_args()
    session = options.session
    if options.api_url == None:
        options.api_url = f"{options.root_url}/api/v1"

    if not os.path.exists(options.root_dir):
        pathlib.Path(options.root_dir).mkdir(parents=True, exist_ok=True)       

    challenges = requests.get(f"{options.api_url}challenges", headers = {
                "Cookie": f"session={session}"
            })
    problems = json.loads(challenges.content)

    for chal in problems["data"]:
        if not os.path.exists(chal["name"]):
            os.mkdir(chal["name"])
        target_dir = os.path.join(options.root_dir, chal["name"])
        problem_filename = f"{target_dir}/problem.json"
        if not os.path.exists(problem_filename) or options.force:
            result = requests.get(f"{options.api_url}/challenges/{chal['id']}",
                headers = {
                    "Cookie": f"session={session}"
                }).content
            with open(problem_filename, "wb") as probfile:
                probfile.write(result)
        else:
            with open(problem_filename) as probfile:
                result = probfile.read()
        problem = json.loads(result)
        for f in problem["data"]["files"]:
            file_name = f.split("?")[0].split("/")[-1]
            if os.path.exists(f"{target_dir}/{file_name}") and not options.force:
                print(f"'{file_name}' is downloaded")
                continue
            wget.download(f"{options.root_url}/{f}", f"{target_dir}/{file_name}")

if __name__ == "__main__":
    main()
