#!/usr/bin/env python3
"""
build_plugin.py — build map-decks, the plugin the organisation installs.

In claude.ai the two skills ship together as one plugin, uploaded by an Owner in
Organization settings > Plugins & skills (Add > Upload a plugin; for a new
release, the plugin's menu > Upload new version). Inside it they carry the names
people know them by:

  map-decks/
    .claude-plugin/plugin.json    name, displayName, version, description, author
    README.md
    skills/slides-builder/        wpp-es-html-deck/, its `name:` set to slides-builder
    skills/deck-builder/          deck-content-builder/, its `name:` set to deck-builder

A skill's folder has to match its `name`, and this repository keeps its own
folder names (the design system's cards and refresh_design_system.py point at
them), so the plugin is built, not kept. It is built from a commit (git archive,
the same bytes as a GitHub download), never from the working copy, and its
version is that commit's newest release in CHANGELOG.md.

  python3 authoring/build_plugin.py                  # dist/map-decks-<version>.zip
  python3 authoring/build_plugin.py --out ~/Downloads

It checks claude.ai's plugin limits (5,000 files, 200 MB, no top-level bin/)
and, when the Claude Code CLI is installed, runs `claude plugin validate` on
what it wrote. It exits non-zero if either fails.
"""
import argparse, io, json, os, re, shutil, subprocess, sys, tarfile, tempfile, time, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = "map-decks"
SKILLS = {"wpp-es-html-deck": "slides-builder", "deck-content-builder": "deck-builder"}
MAX_FILES, MAX_MB = 5000, 200   # claude.ai, per plugin

MANIFEST = {
    "name": PLUGIN,
    "displayName": "MAP Decks",
    "description": "WPP Enterprise Solutions | MAP decks. deck-builder writes the content; "
                   "slides-builder builds the on-brand deck as a Claude Slides deck wherever Claude "
                   "Slides is available (a chat, Claude Design, Claude Code), otherwise as one "
                   "self-contained HTML file.",
    "author": {"name": "Carlos Lucero"},
}

README = """# MAP Decks

WPP Enterprise Solutions | MAP decks, made with Claude. Version {version}.

- **deck-builder** writes the words. It shows you the slide titles first and
  writes the full slide-by-slide text once you approve them.
- **slides-builder** builds the deck in the MAP look. Wherever Claude Slides
  is available (a chat, Claude Design, Claude Code) you get a Claude Slides deck you can
  edit, share and export to PowerPoint or PDF; where it isn't, one
  self-contained HTML file. It asks you a few questions and a style before it
  builds.

Ask in plain words, for example "Make a MAP deck from these notes", or "Use
deck-builder to write the content for a sales deck from these notes".

The fonts, logos and illustrations are proprietary to WPP and not for
redistribution. The photographs have no recorded source or licence: confirm the
licence before one goes into a client-facing or published deck.

Built from github.com/carloslucero-map/slides-skills at {commit}.
"""


def git(*args, binary=False):
    return subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True,
                          text=not binary).stdout


def fail(msg):
    sys.exit(f"FAIL — {msg}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default=os.path.join(REPO, "dist"), help="folder for the zip")
    ap.add_argument("--ref", default="HEAD", help="the commit to build (default HEAD)")
    a = ap.parse_args()

    commit = git("rev-parse", "--short", a.ref).strip()
    m = re.search(r"^## \[(\d+\.\d+\.\d+)\]", git("show", f"{a.ref}:CHANGELOG.md"), re.M)
    if not m:
        fail(f"no release heading in CHANGELOG.md at {commit}")
    version = m.group(1)
    if a.ref == "HEAD" and git("status", "--porcelain", "--", *SKILLS, "CHANGELOG.md").strip():
        print(f"note: uncommitted changes are not in the plugin; it is built from {commit}")

    files = {}   # path inside the plugin -> (bytes, mode)
    tar = git("archive", "--format=tar", a.ref, *SKILLS, binary=True)
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        for member in t.getmembers():
            if member.isfile():
                src, rest = member.name.split("/", 1)
                files[f"skills/{SKILLS[src]}/{rest}"] = (t.extractfile(member).read(), member.mode)

    for src, name in SKILLS.items():
        path = f"skills/{name}/SKILL.md"
        text, n = re.subn(rf"\A---\nname: {re.escape(src)}\n", f"---\nname: {name}\n",
                          files[path][0].decode("utf-8"))
        if n != 1:
            fail(f"{src}/SKILL.md does not start with `name: {src}`")
        files[path] = (text.encode("utf-8"), files[path][1])

    manifest = {"name": MANIFEST["name"], "displayName": MANIFEST["displayName"], "version": version,
                "description": MANIFEST["description"], "author": MANIFEST["author"]}
    files[".claude-plugin/plugin.json"] = ((json.dumps(manifest, indent=2, ensure_ascii=False)
                                            + "\n").encode("utf-8"), 0o644)
    files["README.md"] = (README.format(version=version, commit=commit).encode("utf-8"), 0o644)

    size = sum(len(data) for data, _ in files.values())
    if len(files) > MAX_FILES:
        fail(f"{len(files)} files, the cap is {MAX_FILES}")
    if size > MAX_MB * 1024 * 1024:
        fail(f"{size / 1048576:.1f} MB, the cap is {MAX_MB} MB")
    if any(p.startswith("bin/") for p in files):
        fail("a top-level bin/ stops claude.ai and Cowork from installing the plugin")

    os.makedirs(a.out, exist_ok=True)
    out = os.path.join(a.out, f"{PLUGIN}-{version}.zip")
    stamp = time.localtime(int(git("log", "-1", "--format=%ct", a.ref)))[:6]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(files):
            data, mode = files[path]
            info = zipfile.ZipInfo(f"{PLUGIN}/{path}", date_time=stamp)
            info.external_attr = (0o100000 | (mode & 0o777)) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)

    claude = shutil.which("claude")
    if claude:
        with tempfile.TemporaryDirectory() as tmp:
            zipfile.ZipFile(out).extractall(tmp)
            r = subprocess.run([claude, "plugin", "validate", os.path.join(tmp, PLUGIN)],
                               capture_output=True, text=True)
            print((r.stdout + r.stderr).strip())
            if r.returncode:
                fail("claude plugin validate")
    else:
        print("note: the claude CLI is not installed, so `claude plugin validate` was not run")

    per_skill = {name: sum(1 for p in files if p.startswith(f"skills/{name}/")) for name in SKILLS.values()}
    print(f"BUILT — {out}\n  {PLUGIN} {version} from {commit}: {len(files)} files "
          f"(cap {MAX_FILES}), {size / 1048576:.2f} MB (cap {MAX_MB}), {os.path.getsize(out) / 1048576:.2f} MB zipped\n  "
          + ", ".join(f"{name} {n} files" for name, n in per_skill.items()))


if __name__ == "__main__":
    main()
