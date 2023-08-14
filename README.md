This script aims to simplify automatic translation of i18n strings:

- Looks at a commit (based on a hash)
- For each JSON file in the commit, examines all the changed keys, and stores them in the list `keys`
- For each language (from a list of strings), change the language's JSON file and set the value of each key in `keys` to an empty string

This then lets the CI auto-rebuild translations without interfering with existing manually edited translations

## Install

```
pip install -r requirements
```

## Usage

1. Enter the directory of this repo
2. `ln -s <path_to_cloned_target_repo> .`
3. Run `python app.py <cloned_repo_folder_name> <commit_hash>`

For safety's sake, this repo doesn't make commits or push anything to git. That's for you to do (and get the blame for if anything goes wrong)!
