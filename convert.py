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

r = re.compile(r"\n *[*\-+] ")
r_n = re.compile(r"\n *[0-9]. ")
r2 = re.compile(r"#[ ]*TODO:.+")
r3 = re.compile(r"> *\[!([A-Z]+)\] *\n> *(.*)")
for fname in p.iterdir():
    if fname.is_dir():
        continue

    with open(fname, "r", encoding="utf8") as f:
        fdata = f.read()

    # fix spacing for lists
    fdata = r.sub(lambda m: f"\n{m.group(0)}", fdata)
    fdata = r_n.sub(lambda m: f"\n{m.group(0)}", fdata)

    # remove "todo" notes bc they break formatting
    fdata = r2.sub("", fdata)

    # call-outs
    fdata = r3.sub(lambda m:
                   f"!!! {m.group(1).lower()}\n    {m.group(2)}",
                   fdata)
    #FIXME: multi-line callouts are still broken

    with open(fname, "w", encoding="utf8") as f:
        f.write(fdata)

# copy index.md to /docs
shutil.copy("index.md", "docs")

# TODO: convert call-outs
# TODO: fix weird spacing
