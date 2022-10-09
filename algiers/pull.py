import requests
import json
import os
import wget

cookies = {"session": "BLAH"}

with open("./challenges.json") as cfile:
    jschal = json.loads(cfile.read())
for problem in jschal["data"]:
    pid, name = problem["id"], problem["name"]
    dirname = f"challenges/{name}"
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    json_path = f"challenges/{name}/{pid}.json"
    if not os.path.exists(json_path):
        c = requests.get(f"https://ctf.gdgalgiers.com/api/v1/challenges/{pid}", cookies=cookies).content
        try:
            jsp = json.loads(c)
            with open(json_path, "wb") as jsonfile:
                jsonfile.write(c)
        except Exception as e:
            print(e)
            continue
    else:
        with open(json_path) as chalfile:
            chal = json.load(chalfile)
        print(chal["data"]["files"])
        files = chal["data"]["files"]
        for f in files:
            file_name = f.split("?")[0].split("/")[-1]
            resp = requests.get(f"https://ctf.gdgalgiers.com/{f}")
            with open(f"{dirname}/{file_name}", "wb") as outputfile:
                outputfile.write(resp.content)
