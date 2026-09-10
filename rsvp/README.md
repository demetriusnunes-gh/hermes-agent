# Rock N Fifty RSVP

Standalone RSVP site for Demetrius's 50th birthday. It uses only Python's standard library and stores submissions in `data/rsvp.sqlite3`.

## Run locally

```bash
python3 app.py
```

Open <http://127.0.0.1:8797>.

## Data

The `rsvps` table stores:

- name
- optional email
- attending / not attending
- guest count
- optional message
- submission timestamp

## Production host

The site is designed to sit behind Caddy at `rsvp.demetriusnunes.com`, proxying to `127.0.0.1:8797`. Before the public URL can work, add an `A`/`AAAA` DNS record for `rsvp.demetriusnunes.com` pointing to this server. Caddy can then issue the HTTPS certificate automatically.
