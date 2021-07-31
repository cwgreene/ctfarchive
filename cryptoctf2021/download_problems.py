import requests
import json
import os
import re

import supersecret
XSRF_TOKEN=supersecret.getSecret("cryptoctf2021", "X-CSRF-TOKEN")
CRYPTO_CTF_SESSION=supersecret.getSecret("cryptoctf2021", "crypto_ctf_token")

COOKIES = {
    "XSRF_TOKEN": XSRF_TOKEN,
    "crypto_ctf_session": CRYPTO_CTF_SESSION
}

def get_problems(force = False, cache=True):
    if os.path.exists("all_problems.json") and not force:
        with open("all_problems.json") as problems:
            challenges = problems.read()
    else:
        challenges_resp = requests.get("https://cr.yp.toc.tf/challenges/list",
            cookies=COOKIES)
        if challenges_resp.status_code != 200:
            raise Exception(f"Could not get challenges [{challenges_resp.status_code}]:\n{challenges_resp.content}")
        if cache:
            with open("all_problems.json", "w") as problems:
                problems.write(challenges_resp.content)
        challenges = challenges_resp.content
    return json.loads(challenges)

def download_problem(problem):
    name = problem["name"].split(" -")[0].strip().replace(" ", "_").lower()
    if not os.path.exists(name):
        print(f"making directory {name}")
        os.mkdir(name)
    match = re.match(r'.*<a href="([^"]*)".*', problem["description"])
    if match:
        download_url = match.group(1)
        filename = f"{name}/{os.path.basename(download_url)}"
        if os.path.exists(filename):
            print(f"{filename} already exists")
            return
        result = requests.get(f"https://cr.yp.toc.tf/{download_url}", cookies=COOKIES)
        print(result)
        if result.status_code != 200:
            print(result.content)
            return
        filename = f"{name}/{os.path.basename(download_url)}"
        if os.path.exists(filename):
            print(f"{filname} already exists")
            return
        with open(filename, "wb") as download_file:
            download_file.write(result.content)
    

for problem in get_problems():
    download_problem(problem)
