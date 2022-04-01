import requests
import argparse
import json
import os
import wget
import sys
ROOT_URL="https://ctfd.ritsec.club/"
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("session")
    parser.add_argument("--force", action="store_true")
    options = parser.parse_args()
    session = options.session
    challenges = requests.get(f"{ROOT_URL}/api/v1/challenges", headers = {
                "Cookie": f"session={session}"
            })
    problems = json.loads(challenges.content)

    for chal in problems["data"]:
        print(chal["name"])
        if not os.path.exists(chal["name"]):
            os.mkdir(chal["name"])
        target_dir = chal["name"]
        problem_filename = f"{target_dir}/problem.json"
        if not os.path.exists(problem_filename) or options.force:
            result = requests.get(f"{ROOT_URL}/api/v1/challenges/{chal['id']}",
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
            wget.download(f"{ROOT_URL}/{f}", f"{target_dir}/{file_name}")

if __name__ == "__main__":
    main()
