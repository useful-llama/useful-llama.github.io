"""Builds the lesson lists the progress page reads (fun-lessons.json, div-lessons.json) from the two apps' course files.
Run from this folder: py -I build_lessons.py"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
PROJECTS = HERE.parent.parent
APPS = {
    "fun": PROJECTS / "Fun and Efficient Language/app/src/main/assets/courses/es",
    "div": PROJECTS / "Divertinglish/app/src/main/assets/courses/en",
}

for code, root in APPS.items():
    course = json.loads((root / "course.json").read_text(encoding="utf-8"))
    order = [u for level in course["levels"] for u in level.get("units", [])] if isinstance(course.get("levels"), list) and course["levels"] and isinstance(course["levels"][0], dict) and "units" in course["levels"][0] else None
    files = sorted((root / "units").glob("*.json"))
    units = []
    for f in files:
        u = json.loads(f.read_text(encoding="utf-8"))
        title = u.get("titleEs") or u.get("title") or u["id"]
        units.append({"id": u["id"], "title": title, "emoji": u.get("emoji", ""),
                      "lessons": [{"id": l["id"], "title": l.get("title", l["id"])} for l in u.get("lessons", [])]})
    if order:
        rank = {uid if isinstance(uid, str) else uid.get("id"): i for i, uid in enumerate(order)}
        units.sort(key=lambda x: rank.get(x["id"], 10_000))
    out = {"app": "Funspañol" if code == "fun" else "Divertinglish", "units": units}
    (HERE / f"{code}-lessons.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(code, len(units), "units", sum(len(u["lessons"]) for u in units), "lessons")
