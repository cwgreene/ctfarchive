import argparse
import requests
import json
import os
import wget

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--session", required=True)
    options = parser.parse_args()
    cookies = {"session": options.session}

    if not os.path.exists("challenges.json"):
        res = requests.get(f"https://{options.target}/api/v1/challenges", cookies=cookies, headers={
        })
        with open("./challenges.json", "wb") as cfile:
            cfile.write(res.content)

    with open("./challenges.json") as cfile:
        jschal = json.loads(cfile.read())
    if not os.path.exists("challenges"):
        os.mkdir("challenges")
    for problem in jschal["data"]:
        pid, name = problem["id"], problem["name"]
        dirname = f"challenges/{name}"
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        json_path = f"challenges/{name}/{pid}.json"
        if not os.path.exists(json_path):
            c = requests.get(f"https://{options.target}/api/v1/challenges/{pid}", cookies=cookies).content
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
                resp = requests.get(f"https://{options.target}/{f}")
                with open(f"{dirname}/{file_name}", "wb") as outputfile:
                    outputfile.write(resp.content)

if __name__ == "__main__":
    main()
