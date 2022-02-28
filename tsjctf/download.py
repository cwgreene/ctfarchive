import requests
import json
import os
import wget
session = ""
with open("./challenges.json") as problemsfile:
    problems = json.load(problemsfile)
    for chal in problems["data"]:
        print(chal)
        if not os.path.exists(chal["name"]):
            os.mkdir(chal["name"])
        result = requests.get(f"https://chal.ctf.tsj.tw//api/v1/challenges/{chal['id']}",
            headers = {
                "Cookie": f"session={session}"
            }).content
        target_dir = chal["name"]
        with open(f'{target_dir}/problem.json', "wb") as problemjson:
            problemjson.write(result)
        problem = json.loads(result)
        for f in problem["data"]["files"]:
            file_name = f.split("?")[0].split("/")[-1]
            wget.download(f"https://chal.ctf.tsj.tw/{f}", f"{target_dir}/{file_name}")
