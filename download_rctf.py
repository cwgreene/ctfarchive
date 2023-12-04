import requests
import argparse
import json
import os
import sys
import pathlib
import collections
#hyper needs the four following aliases to be done manually.
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
from hyper.contrib import HTTP20Adapter

def get_with_bearer(s, bearer, url):
    return s.get(url, headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer}",
    })

def download(s, bearer, source, dest):
    res = get_with_bearer(s, bearer, source)
    print(res)
    if res.status_code != 200:
        raise Exception("Oh Noes!")
    with open(dest, "wb") as target_file:
        target_file.write(res.content)

def remove_trailing_slash(url):
    if url.endswith("/"):
        return url[:-1]
    return url

def join_url(*args):
    normalized_args = [remove_trailing_slash(part) for part in args]
    return "/".join(normalized_args)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bearer-token", required=True, help="bearer token")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--root-url", required=True, help="url of challenges")
    parser.add_argument("--api-url", action="store_true", default=None)
    parser.add_argument("--root-dir", required=True, help="target output dir")
    options = parser.parse_args()
    bearer = options.bearer_token
    options.root_url = remove_trailing_slash(options.root_url)
    if options.api_url is None:
        options.api_url = f"{options.root_url}/api/v1"
    options.api_url = remove_trailing_slash(options.api_url)

    if not os.path.exists(options.root_dir):
        pathlib.Path(options.root_dir).mkdir(parents=True, exist_ok=True)       
    
    s = requests.Session()
    s.mount(f'{options.api_url}', HTTP20Adapter())

    print(f"Obtaining challenges from {options.api_url}/challs", f"{options.api_url}/challs")
    challenges = get_with_bearer(s, bearer, f"{options.api_url}/challs")
    problems = json.loads(challenges.content)

    for chal in problems["data"]:
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
            result = json.dumps(chal)
            with open(problem_filename, "w") as probfile:
                probfile.write(result)
        else:
            with open(problem_filename) as probfile:
                result = probfile.read()
    
        # Load back stringified reuslt (could use chal directly, but this is for
        # consistency with ctfd.
        print(result)
        problem = json.loads(result)
        for f in problem["files"]:
            if type(f) == dict:
                file_name = f["name"]
                url = join_url(options.root_url, f"{f['url']}")
                print(url)
            else:
                file_name = f.split("?")[0].split("/")[-1]
                url = f
            if os.path.exists(f"{target_dir}/{file_name}") and not options.force:
                print(f"'{file_name}' is downloaded")
                continue
            print(f"'{file_name}' is being downloaded...")
            # TODO: we should dynamically determine if the path is relative or not
            download(s, bearer, f"{url}", f"{target_dir}/{file_name}")

if __name__ == "__main__":
    main()
