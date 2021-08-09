import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--link", required=True)
    parser.add_argument("--folder", required=True)
    options = parser.parse_args()
    try:
        os.mkdir(options.folder)
    except:
        pass
    with open(f"{options.folder}/README.md", "w") as readme:
        readme.write(f"{options.name} available here:\n\n")
        readme.write(f"{options.link}\n\n")
        readme.write(f"Metadata to be added later.")
main()
