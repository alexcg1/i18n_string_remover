import difflib
import json
import os
import sys

from git import Repo

# repo = 'BestBanner'
# commit_hash = 'a23b2e5'

repo = sys.argv[1]
commit_hash = sys.argv[2]

langs = ['de', 'es', 'fr', 'it', 'ja', 'ko', 'mn', 'ru', 'zh-CN', 'zh-TW']
json_dir = f'./{repo}/webapp/src/i18n/'
json_filename = 'index.json'


def get_changed_lines(repo: str, commit_hash: str):
    changed_lines = set()
    # Instantiate the repository
    r = Repo(repo)

    # Get the specified commit
    commit = r.commit(commit_hash)

    # Compare this commit with its parent(s)
    diffs = commit.parents[0].diff(commit)

    for diff in diffs.iter_change_type('M'):
        a_blob = diff.a_blob.data_stream.read().decode('utf-8')
        b_blob = diff.b_blob.data_stream.read().decode('utf-8')
        a_lines = a_blob.split("\n")
        b_lines = b_blob.split("\n")

        diff_lines = difflib.unified_diff(a_lines, b_lines,
                                          fromfile=diff.a_path,
                                          tofile=diff.b_path,
                                          lineterm='')

        # print the lines that start with '-' or '+', excluding the header lines
        for line in diff_lines:
            if line.startswith('- ') or line.startswith('+ '):
                # print(line[3:-1])
                line_parts = line.split('"')
                key = line_parts[1]
                # print(key)
                changed_lines.add(key)
                # print(line_parts)

        return changed_lines

# def delete_keys(files: list, keys: list, ignore: list = []):


def delete_keys_from_json_file(keys: list, filename: list):
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")

    with open(filename, 'r+') as f:
        data = json.load(f)

        for key in keys:
            if key in data:
                del data[key]

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


keys = get_changed_lines(repo=repo, commit_hash=commit_hash)
print(keys)

# delete_keys_from_json_file(keys=keys, filename='fr.json')

for lang in langs:
    path = os.path.join(json_dir, lang, json_filename)
    if os.path.isfile(path):
        delete_keys_from_json_file(keys=keys, filename=str(path))
    print(path)
