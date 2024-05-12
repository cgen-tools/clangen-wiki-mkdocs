from pathlib import Path
import re
import shutil
from urllib.parse import unquote
import yaml

def convert_callouts(m: re.Match) -> str:
    """Converts matched callouts to Material for MkDocs format."""
    s = f"!!! {m.group(1).lower()}\n"
    for i in range(2, len(m.groups())):
        # hacky way to get >this and > this consistent
        s += m[i].replace("> ", ">").replace(">", "    ")
    return s

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
r3 = re.compile(r"> *\[!([A-Z]+)\]((?:\n(>.*))*)")
r4 = re.compile(r"\((https://github.com/ClanGenOfficial/clangen/wiki/)([^#\n]*)(#?.*)\)")
for fname in p.iterdir():
    if fname.is_dir():
        continue

    with open(fname, "r", encoding="utf8") as f:
        fdata = f.read()

    # force indents to be 4 spaces
    fdata_new = ""
    for line in fdata.split("\n"):
        indent = re.search(r"^ +", line)
        if indent and indent.end() > 0:
            new_line = (" " * (4 - indent.end() % 4)) + line + "\n"
        else:
            new_line = line + "\n"
        fdata_new += new_line
    fdata = fdata_new

    # fix spacing for lists
    fdata = r.sub(lambda m: f"\n{m.group(0)}", fdata)
    fdata = r_n.sub(lambda m: f"\n{m.group(0)}", fdata)

    # remove "todo" notes bc they break formatting
    fdata = r2.sub("", fdata)

    # call-outs
    fdata = r3.sub(convert_callouts, fdata)

    # urls link to mkdocs
    fdata = r4.sub(lambda m: f"({unquote(m.group(2))}.md{m.group(3)})", fdata)

    with open(fname, "w", encoding="utf8") as f:
        f.write(fdata)

# copy index.md to /docs
shutil.copy("index.md", "docs")

# TODO: fix weird spacing
