from pathlib import Path
import re
import shutil
import yaml

# create navigation with names
mkdocs_conf = None
with open("mkdocs.yml", "r", encoding="utf8") as f:
    mkdocs_conf = yaml.load(f.read(), yaml.Loader)
    mkdocs_conf["nav"] = []

name_to_path = {}
p = Path("docs")
for fname in p.iterdir():
    if fname.name == ".git":
        continue
    # replace with correct formatting for display
    title = fname.stem.replace("-", " ")
    name_to_path[title] = fname.name
# alphabetical order for readability
sorted_name_to_path = dict(sorted(name_to_path.items()))

# has to be in this format
mkdocs_conf["nav"] = [{k: v} for k, v in sorted_name_to_path.items()]

with open("mkdocs.yml", "w", encoding="utf8") as f:
    yaml.dump(mkdocs_conf, f, yaml.Dumper)

# copy index.md to /docs
shutil.copy("index.md", "docs")

r = re.compile(r"\n *[*\-+] ")
for fname in p.iterdir():
    if fname.is_dir():
        continue

    with open(fname, "r", encoding="utf8") as f:
        fdata = f.read()

    # fix spacing for lists
    fdata = r.sub(lambda m: f"\n{m.group(0)}", fdata)

    with open(fname, "w", encoding="utf8") as f:
        f.write(fdata)

# TODO: convert call-outs
# TODO: fix weird spacing
