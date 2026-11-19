"""Build testers/index.html: the page tester invitations link to (Joey, 19 Nov 2026).

One card per app: icon, what it is, a short "picture this" example, real screenshots from its Play listing,
what to try, and the Become a tester link. Each card has its own anchor, e.g. testers/#road-camera.

When Google approves an app's closed test, set ready=True and run:   py -I testers/build_testers.py
Screenshots live in testers/img/<slug>/ (icon.webp, shot-1.jpg ...), taken from the app's Play listing.
Never put unlock codes on this page: it is public. Codes stay in the members-only group post.
"""
import html
import os

GROUP = "https://groups.google.com/g/ullama-app-testers"

APPS = [
    dict(slug="diet-and-dexa", name="Diet & DEXA", pkg="com.usefulllama.dietanddexa", ready=True, kind="Health",
         tag="Your food, your body scans and your exercise in one clear picture.",
         about="Point the camera at your plate and see calories, protein and every vitamin and mineral against "
               "Australian targets. Add a DEXA or InBody report and it explains each number in plain colours. "
               "Tell Dex, the fitness llama, what you ate or ask him anything.",
         example="Mia has just had her first DEXA scan and has no idea what “visceral fat 105 cm²” "
                 "means. She photographs the report and the app shows where each number sits for her age. At lunch "
                 "she snaps her plate and sees she is short on fibre for the day.",
         tryit=["Log a few meals, with the food camera at least once", "Add a scan report if you have one",
                "Track a walk or a run"],
         note="Everything is free for the first 59 days, so you won't need to buy anything."),
    dict(slug="road-camera", name="Road Camera", pkg="com.usefulllama.roadcamera", ready=True, kind="Driving",
         tag="Your phone is your dash cam.",
         about="Mount your phone, start recording while parked, and drive. Keep the clips that matter, and turn "
               "them into a tidy incident report with photos, a map and your own account, ready as a PDF.",
         example="Sam starts recording before the morning commute. A car runs a red light just ahead. Once he is "
                 "parked, he saves that clip so it is never recorded over, and builds a report for his insurer "
                 "with the clip's photos and the map pin.",
         tryit=["Record a drive (set it up while parked)", "Save a clip and look through your footage",
                "Start an incident report and export the PDF"],
         note="Never touch the phone while driving. Testers get a free unlock code in the tester group."),
    dict(slug="funspanol", name="Funspañol", pkg="com.usefulllama.funefficientlanguage", ready=True,
         kind="Learn Spanish",
         tag="Learn Spanish from the words you already know.",
         about="Lots of English words turn into Spanish with a simple pattern: information → información, "
               "university → universidad. Build on that with short lessons from beginner to advanced, chats "
               "with friendly neighbours, speaking practice and quick games.",
         example="Priya is going to Mexico in two months. On the bus she does a ten-minute lesson, answers a "
                 "neighbour's question out loud, and finishes with a lightning round of words she saved yesterday.",
         tryit=["Do a few lessons, starting from Lo esencial", "Try a speaking activity", "Play one of the games"],
         note="Testers get a free unlock code in the tester group."),
    dict(slug="invoice-maker", name="Invoice Maker", pkg="com.usefulllama.invoicemaker", ready=True,
         kind="Business",
         tag="Invoices, estimates and contracts on your phone.",
         about="Make a PDF invoice or estimate in a minute, with your saved clients and rates. See what is paid, "
               "unpaid or overdue, record expenses with receipt photos, and export reports to Excel at tax time.",
         example="Tom, a tiler, finishes a bathroom job. Before he packs up the van he picks the client, adds the "
                 "hours and materials, checks the PDF and sends the invoice. In June he exports the year's "
                 "invoices and expenses for his accountant.",
         tryit=["Make a sample invoice and look at the PDF", "Turn an estimate into an invoice",
                "Add an expense with a photo"],
         note=""),
    dict(slug="time-card", name="Time Card", pkg="com.usefulllama.timecard", ready=True, kind="Work",
         tag="Your hours and duties, ready for your boss.",
         about="Add what you did each day and when you started and finished. Time Card adds up the hours, any "
               "overtime and breaks, and makes a clear time card you can share as a PDF.",
         example="Lena works casual shifts at two cafés. Each evening she adds her start and finish times and "
                 "what she did. At the end of the fortnight she sends each manager a clean PDF time card.",
         tryit=["Add a few days of sample work", "Try the check-in and check-out buttons",
                "Export and share a time card"],
         note=""),
    dict(slug="cats-vs-llamas", name="Cats vs Llamas", pkg="com.usefulllama.catsvsllamas", ready=True,
         kind="Game",
         tag="Cute cats or fluffy llamas, in turn-based battles.",
         about="Pick a side and lead your little army across a field of hexagons: knights, wizards, archers, "
               "ninjas and more, each with their own moves. Between battles, grow a 3D city and level up your "
               "heroes. Nobody really gets hurt: a beaten llama just stomps off in a huff.",
         example="On the train home, Alex plays a battle: Sir Paws the knight cat shields the archers while the "
                 "wizard splashes the llamas. Back in town he builds another house, so his squad can grow.",
         tryit=["Play a few battles", "Build up your city", "Equip a hero with new gear"],
         note="Testers get a free unlock code in the tester group."),
    dict(slug="hold-the-line", name="Crimson Defiance: Hold the Line", pkg="com.usefulllama.holdtheline",
         ready=True, kind="Game",
         tag="Tower defence on Mars: hold 50 waves.",
         about="The enemy is coming down the road and your HQ is at the end of it. Build towers beside the road, "
               "place soldiers and tanks, wall the road off, and stop every wave. Play either side, on four "
               "battlefields, with a boss every tenth wave.",
         example="With ten minutes to spare, Jordan picks the Solar Legion, puts a laser tower on the first bend "
                 "and a wall across the road, and sees how many waves they can hold before the titan arrives.",
         tryit=["Play some waves on each side", "Upgrade a tower and build a wall",
                "Tell me which waves feel too easy or too hard"],
         note="In-game coins are earned in each run. Watching an ad is always your choice, never forced."),
    dict(slug="crimson-defiance", name="Crimson Defiance: True RTS", pkg="com.usefulllama.crimsondefiance",
         ready=False, kind="Game",
         tag="A real-time strategy war for Mars, built for your phone.",
         about="Build a base, harvest Dark Grain and power, train soldiers, roll out tanks and hover craft, and "
               "lead your army across the red planet. Two campaigns with comic-panel stories, skirmish, a map "
               "editor, and battles with friends on the same Wi-Fi. No ads.",
         example="Riley plays the Prometheans' first mission on the couch: builds up a base, "
                 "holds the walls of New Red City, then sends the tanks out to strike back.",
         tryit=["Play the first mission on each side", "Try a skirmish on a small map",
                "Tell me if anything is slow on your phone"],
         note="A big download (about 2.4 GB), so use Wi-Fi and check your phone has room."),
    dict(slug="divertinglish", name="Divertinglish", pkg="com.usefulllama.divertinglish", ready=False,
         kind="Learn English (for Spanish speakers)", lang="es",
         tag="Aprende inglés con explicaciones en español.",
         about="Funspañol's twin for Spanish speakers: lessons from A1 to C2, chats with five friendly "
               "neighbours, speaking practice and games, all explained in Spanish. "
               "(Para hispanohablantes que aprenden inglés.)",
         example="Lucía practica cinco minutos cada mañana: una lección corta, una charla con Maya "
                 "y una partida de Word Rain con sus propias palabras.",
         tryit=["Haz algunas lecciones", "Prueba una actividad para hablar", "Juega a uno de los juegos"],
         note=""),
]


def esc(s):
    return html.escape(s, quote=True)


def jpeg_size(path):
    """(width, height) from a JPEG's frame header, so the page reserves each screenshot's space before it loads."""
    b = open(path, "rb").read()
    i = 2
    while i < len(b):
        marker, seg = b[i + 1], int.from_bytes(b[i + 2:i + 4], "big")
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            return int.from_bytes(b[i + 7:i + 9], "big"), int.from_bytes(b[i + 5:i + 7], "big")
        i += 2 + seg
    raise ValueError("no JPEG frame header in " + path)


def card(a):
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", a["slug"])
    shots = sorted((f for f in os.listdir(d) if f.startswith("shot-")), key=lambda f: int(f[5:].split(".")[0]))
    lang = ' lang="%s"' % a["lang"] if a.get("lang") else ""
    imgs = "\n".join(
        '      <a href="img/%s/%s"><img src="img/%s/%s" alt="%s screenshot %d" width="%d" height="%d"%s loading="lazy"></a>'
        % ((a["slug"], f, a["slug"], f, esc(a["name"]), i) + jpeg_size(os.path.join(d, f))
           + (' class="wide"' if jpeg_size(os.path.join(d, f))[0] > jpeg_size(os.path.join(d, f))[1] else "",))
        for i, f in enumerate(shots, 1))
    tries = "".join("<li%s>%s</li>" % (lang, esc(t)) for t in a["tryit"])
    if a["ready"]:
        join = ('<a class="join" href="https://play.google.com/apps/testing/%s">Become a tester</a>'
                '<span class="small">New here? <a href="%s">Join the tester group</a> first.</span>' % (a["pkg"], GROUP))
    else:
        join = '<span class="soon">Testing opens soon</span><span class="small">Google is still checking it.</span>'
    note = '\n    <p class="small">%s</p>' % esc(a["note"]) if a["note"] else ""
    return """  <section class="app" id="{slug}">
    <div class="head">
      <img class="icon" src="img/{slug}/icon.webp" alt="" width="64" height="64">
      <div><h2>{name}</h2><p class="kind">{kind}</p></div>
    </div>
    <p class="tag"{lang}>{tag}</p>
    <p>{about}</p>
    <div class="shots">
{imgs}
    </div>
    <div class="example"><b>Picture this</b><p{lang}>{example}</p></div>
    <p class="try-h">What to try</p>
    <ul>{tries}</ul>{note}
    <div class="cta">{join}</div>
    <p class="back"><a href="#top">↑ How to join and all the apps</a></p>
  </section>""".format(slug=a["slug"], name=esc(a["name"]), kind=esc(a["kind"]), lang=lang, tag=esc(a["tag"]),
                       about=esc(a["about"]), imgs=imgs, example=esc(a["example"]), tries=tries, note=note,
                       join=join)


def page():
    nav = "\n".join('    <a href="#%s"><img src="img/%s/icon.webp" alt="" width="40" height="40">%s%s</a>'
                    % (a["slug"], a["slug"], esc(a["name"].replace("Crimson Defiance: ", "")),
                       "" if a["ready"] else " <i>soon</i>") for a in APPS)
    cards = "\n\n".join(card(a) for a in APPS)
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Test our apps · Useful Llama</title>
<meta name="description" content="Help test Useful Llama's Android apps before they reach the Play Store: what each app is like, with real screenshots.">
<link rel="stylesheet" href="../style.css">
<style>
  main {{ max-width: 860px; }}
  .steps {{ background: var(--page); border: 1px solid var(--line); border-radius: 14px; padding: 12px 16px 12px 36px; }}
  .steps li {{ margin: 8px 0; }}
  .nav {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; margin: 16px 0 8px; }}
  .nav a {{ display: flex; align-items: center; gap: 8px; padding: 8px; border: 1px solid var(--line); border-radius: 12px;
           text-decoration: none; color: var(--ink); font-size: 15px; line-height: 1.2; }}
  .nav img {{ border-radius: 9px; flex: none; }}
  .nav i {{ color: var(--muted); font-style: normal; font-size: 13px; }}
  .app {{ border-top: 1px solid var(--line); padding-top: 24px; margin-top: 28px; scroll-margin-top: 12px; }}
  .head {{ display: flex; gap: 14px; align-items: center; }}
  .head h2 {{ margin: 0; font-size: 22px; }}
  .icon {{ border-radius: 14px; flex: none; }}
  .kind {{ margin: 2px 0 0; color: var(--muted); font-size: 15px; }}
  .tag {{ font-weight: 600; font-size: 18px; margin-bottom: 4px; }}
  .shots {{ display: flex; gap: 10px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 4px 0 10px;
            -webkit-overflow-scrolling: touch; }}
  .shots a {{ flex: none; scroll-snap-align: start; }}
  .shots img {{ height: 340px; width: auto; display: block; border-radius: 12px; border: 1px solid var(--line); }}
  @media (max-width: 600px) {{ .shots img {{ height: 300px; }} }}
  .shots img.wide {{ height: auto; width: min(604px, 84vw); }}
  .example {{ background: var(--page); border-left: 4px solid var(--accent); border-radius: 0 12px 12px 0; padding: 10px 14px; margin: 14px 0; }}
  .example p {{ margin: 4px 0 0; }}
  .try-h {{ font-weight: 600; margin: 14px 0 0; }}
  .try-h + ul {{ margin-top: 4px; }}
  .small {{ color: var(--muted); font-size: 15px; }}
  .cta {{ display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; margin-top: 12px; }}
  .join {{ display: inline-block; background: var(--primary); color: #fff; font-weight: 700; padding: 12px 20px;
           border-radius: 12px; text-decoration: none; }}
  @media (prefers-color-scheme: dark) {{ .join {{ background: #2d5bb3; }} }}
  .back {{ margin: 16px 0 0; font-size: 15px; }}
  header.bar {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; position: sticky; top: 0; z-index: 5; }}
  header.bar .all {{ color: #fff; font-size: 15px; font-weight: 600; text-decoration: none; border: 1px solid rgba(255,255,255,.5);
                    border-radius: 999px; padding: 6px 12px; white-space: nowrap; }}
  .app, #top {{ scroll-margin-top: 72px; }}
  .soon {{ display: inline-block; border: 2px dashed var(--line); color: var(--muted); font-weight: 700; padding: 10px 18px; border-radius: 12px; }}
</style>
</head>
<body>
<header class="bar"><a class="brand" href="../">Useful Llama</a><a class="all" href="#top">How to join · All apps</a></header>
<main>
  <h1 id="top">Help test our apps</h1>
  <p>Before Google lets a new app onto the Play Store for everyone, real people have to test it for 14 days.
  Pick any apps you like the look of below. Each one shows what it is like, with real screenshots from the app.</p>

  <h2>How to join</h2>
  <ol class="steps">
    <li><b>Join the tester group</b> (once is enough for every app): <a href="{group}">open the group</a> and press
      <b>Join group</b>. It won't send you emails, and nobody in it can see your address.</li>
    <li>On an app below, press <b>Become a tester</b>, then <b>Become a tester</b> again on Google's page.</li>
    <li>When it says <b>You are a tester</b>, tap <b>download it on Google Play</b> and install the app.</li>
  </ol>
  <p class="small">Android phones only. Use the same Google account as your phone's Play Store. Please keep each
  app installed for at least 14 days (that's the most important part), use it now and then, and tell me anything
  confusing, broken or annoying: <a href="mailto:useful.llama@gmail.com">useful.llama@gmail.com</a>.</p>

  <div class="nav">
{nav}
  </div>

{cards}
</main>
<footer>Made by Useful Llama · <a href="../">All apps and privacy policies</a></footer>
</body>
</html>
""".format(group=GROUP, nav=nav, cards=cards)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(page())
    print("wrote", out, "-", sum(a["ready"] for a in APPS), "of", len(APPS), "apps ready")
