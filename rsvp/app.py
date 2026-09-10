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
                whatsapp TEXT,
                attending INTEGER NOT NULL CHECK (attending IN (0, 1)),
                guests INTEGER NOT NULL DEFAULT 0 CHECK (guests >= 0 AND guests <= 20),
                message TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        columns = {row[1] for row in conn.execute("PRAGMA table_info(rsvps)")}
        if "whatsapp" not in columns:
            conn.execute("ALTER TABLE rsvps ADD COLUMN whatsapp TEXT")


def save_rsvp(form):
    name = form.get("name", [""])[0].strip()
    whatsapp = form.get("whatsapp", [""])[0].strip()
    attending = form.get("attending", [""])[0]
    guests_raw = form.get("guests", ["0"])[0]
    message = form.get("message", [""])[0].strip()

    if not name or attending not in {"yes", "no"}:
        return False, "Informe seu nome e escolha se você estará presente."
    try:
        guests = max(0, min(20, int(guests_raw or 0))) if attending == "yes" else 0
    except ValueError:
        return False, "Informe um número válido de pessoas."

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO rsvps (name, whatsapp, attending, guests, message) VALUES (?, ?, ?, ?, ?)",
            (name, whatsapp, 1 if attending == "yes" else 0, guests, message),
        )
    return True, ""


def render_page(message="", error=False):
    notice = ""
    if message:
        notice = f'<div class="notice {"error" if error else "success"}" role="status">{html.escape(message)}</div>'

    return f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Rock N Fifty — Demetrius faz 50 anos</title>
  <meta name="description" content="Confirme sua presença no Rock N Fifty, a festa de 50 anos do Demetrius.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Permanent+Marker&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="noise"></div>
  <main class="poster">
    <header class="hero">
      <p class="eyebrow">Uma festa de aniversário inesquecível</p>
      <h1><span>Rock N</span> Fifty</h1>
      <p class="subtitle">Demetrius faz 50 anos</p>
      <div class="electric-line"></div>
      <p class="tagline">Guitarras altas. Calças de couro. Uma noite inesquecível.</p>
    </header>

    <section class="details" aria-label="Detalhes do evento">
      <div><span class="detail-label">Quando</span><strong>SÁBADO · 3 DE OUTUBRO DE 2026 · 17H–22H</strong></div>
      <div><span class="detail-label">Onde</span><strong>RUA PRESIDENTE CARLOS DE CAMPOS, 115</strong><small>Playground</small></div>
    </section>

    <section class="rsvp-card" id="rsvp">
      <div class="card-heading"><span class="spark">✦</span><div><p class="eyebrow">Junte-se ao bis</p><h2>Você vem?</h2></div><span class="spark">✦</span></div>
      {notice}
      <form method="post" action="/rsvp">
        <label>Seu nome <span>*</span><input name="name" required maxlength="100" placeholder="Nome de estrela do rock"></label>
        <label>WhatsApp <small>(opcional)</small><input name="whatsapp" type="tel" maxlength="30" placeholder="para receber as novidades"></label>
        <fieldset><legend>Você estará lá?</legend><div class="choices">
          <label class="choice"><input type="radio" name="attending" value="yes" required><span>COM CERTEZA<br><small>Eu vou!</small></span></label>
          <label class="choice no"><input type="radio" name="attending" value="no"><span>NÃO VOU CONSEGUIR<br><small>Vou torcer de longe</small></span></label>
        </div></fieldset>
        <label>Quantas pessoas você levará? <small>(incluindo você)</small><input name="guests" type="number" min="1" max="20" value="1" required></label>
        <label>Recado <small>(opcional)</small><textarea name="message" rows="3" maxlength="500" placeholder="Deixe uma mensagem de aniversário para o Demetrius..."></textarea></label>
        <button type="submit">Confirmar minha presença <span>→</span></button>
      </form>
    </section>

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
        self.send_html(render_page("Você está na lista — nos vemos no Rock N Fifty!" if ok else message, not ok), 200 if ok else 400)

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
