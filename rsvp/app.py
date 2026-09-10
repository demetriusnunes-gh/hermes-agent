from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
from pathlib import Path
import html
import json
import sqlite3

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "rsvp.sqlite3"
HOST = "127.0.0.1"
PORT = 8797


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rsvps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                attending INTEGER NOT NULL CHECK (attending IN (0, 1)),
                guests INTEGER NOT NULL DEFAULT 0 CHECK (guests >= 0 AND guests <= 20),
                message TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_rsvp(form):
    name = form.get("name", [""])[0].strip()
    email = form.get("email", [""])[0].strip()
    attending = form.get("attending", [""])[0]
    guests_raw = form.get("guests", ["0"])[0]
    message = form.get("message", [""])[0].strip()

    if not name or attending not in {"yes", "no"}:
        return False, "Please add your name and choose whether you are coming."
    try:
        guests = max(0, min(20, int(guests_raw or 0))) if attending == "yes" else 0
    except ValueError:
        return False, "Please enter a valid number of guests."

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO rsvps (name, email, attending, guests, message) VALUES (?, ?, ?, ?, ?)",
            (name, email, 1 if attending == "yes" else 0, guests, message),
        )
    return True, ""


def render_page(message="", error=False):
    notice = ""
    if message:
        notice = f'<div class="notice {"error" if error else "success"}" role="status">{html.escape(message)}</div>'

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Rock N Fifty — Demetrius turns 50</title>
  <meta name="description" content="RSVP for Demetrius's Rock N Fifty 50th birthday party.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Permanent+Marker&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="noise"></div>
  <main class="poster">
    <header class="hero">
      <div class="sticker">THE BIG 5-0</div>
      <p class="eyebrow">A birthday bash for the ages</p>
      <h1><span>Rock N</span> Fifty</h1>
      <p class="subtitle">Demetrius is turning 50</p>
      <div class="electric-line"></div>
      <p class="tagline">Loud guitars. Big hair. One unforgettable night.</p>
    </header>

    <section class="details" aria-label="Event details">
      <div><span class="detail-label">When</span><strong>DATE COMING SOON</strong><small>Save the night — details dropping soon</small></div>
      <div><span class="detail-label">Where</span><strong>LOCATION COMING SOON</strong><small>Venue details dropping soon</small></div>
      <div><span class="detail-label">Dress code</span><strong>HAIR METAL</strong><small>Leather, denim &amp; maximum volume</small></div>
    </section>

    <section class="rsvp-card" id="rsvp">
      <div class="card-heading"><span class="spark">✦</span><div><p class="eyebrow">Join the encore</p><h2>Are you in?</h2></div><span class="spark">✦</span></div>
      {notice}
      <form method="post" action="/rsvp">
        <label>Your name <span>*</span><input name="name" required maxlength="100" placeholder="Rock star name"></label>
        <label>Email <small>(optional)</small><input name="email" type="email" maxlength="180" placeholder="so we can send updates"></label>
        <fieldset><legend>Will you be there?</legend><div class="choices">
          <label class="choice"><input type="radio" name="attending" value="yes" required><span>HELL YEAH<br><small>I'm coming!</small></span></label>
          <label class="choice no"><input type="radio" name="attending" value="no"><span>CAN'T MAKE IT<br><small>Rock on from afar</small></span></label>
        </div></fieldset>
        <label>How many people are you bringing? <small>(including you)</small><input name="guests" type="number" min="1" max="20" value="1" required></label>
        <label>Dedication <small>(optional)</small><textarea name="message" rows="3" maxlength="500" placeholder="Leave a birthday message for Demetrius..."></textarea></label>
        <button type="submit">Lock in my RSVP <span>→</span></button>
      </form>
    </section>

    <footer><span>★</span> Come for the music. Stay for the memories. <span>★</span></footer>
  </main>
  <script>
    const radios = document.querySelectorAll('input[name="attending"]');
    const guests = document.querySelector('input[name="guests"]');
    radios.forEach(radio => radio.addEventListener('change', () => {{
      const isComing = document.querySelector('input[name="attending"]:checked')?.value === 'yes';
      guests.disabled = !isComing;
      guests.required = isComing;
      if (!isComing) guests.value = 0; else if (guests.value === '0') guests.value = 1;
    }}));
  </script>
</body>
</html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            return
        if self.path.startswith("/static/style.css"):
            css = (ROOT / "static" / "style.css").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("Cache-Control", "public, max-age=3600")
            self.end_headers()
            self.wfile.write(css)
            return
        if self.path == "/" or self.path.startswith("/?"):
            self.send_html(render_page())
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != "/rsvp":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        ok, message = save_rsvp(parse_qs(body))
        self.send_html(render_page("You're on the guest list — see you at Rock N Fifty!" if ok else message, not ok), 200 if ok else 400)

    def send_html(self, body, status=200):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")


if __name__ == "__main__":
    init_db()
    print(f"Rock N Fifty RSVP running at http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
