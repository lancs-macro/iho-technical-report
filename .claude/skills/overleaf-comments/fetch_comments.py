"""Fetch Overleaf review comments for the IHO technical report.

Uses Overleaf's internal (undocumented) JSON routes via a headless Playwright
session:
  /project/<id>/threads  -> comment threads (author, time, text, replies)
  /project/<id>/ranges   -> which text each thread is anchored to

Usage:
  python fetch_comments.py --login   # once: headed browser, sign in, session saved
  python fetch_comments.py           # headless, prints markdown to stdout
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import BrowserContext, Playwright, sync_playwright

PROJECT_ID = "6a13188773f44487d10a0a75"
BASE = "https://www.overleaf.com"
REPO = Path(__file__).resolve().parents[3]
STATE = REPO / ".overleaf-state.json"


def launch(p: Playwright, headless: bool) -> BrowserContext:
    """Open a browser context, preferring installed Chrome (Google SSO blocks bare Chromium)."""
    args = ["--disable-blink-features=AutomationControlled"]
    try:
        browser = p.chromium.launch(channel="chrome", headless=headless, args=args)
    except Exception:
        browser = p.chromium.launch(headless=headless, args=args)
    ctx = browser.new_context(storage_state=STATE if STATE.exists() and headless else None)
    if headless and (cookie := env("OVERLEAF_SESSION")):
        ctx.add_cookies([{"name": "overleaf_session2", "value": cookie, "domain": ".overleaf.com",
                          "path": "/", "secure": True, "httpOnly": True}])
    return ctx


def env(key: str) -> str | None:
    """Read a key from the repo's .env (no python-dotenv needed)."""
    f = REPO / ".env"
    for line in f.read_text(encoding="utf-8").splitlines() if f.exists() else []:
        k, _, v = line.partition("=")
        if k.strip() == key and v.strip():
            return v.strip().strip("\"'")
    return None


def login() -> None:
    """Open a visible browser, wait for the user to sign in, save the session."""
    with sync_playwright() as p:
        ctx = launch(p, headless=False)
        page = ctx.new_page()
        page.goto(f"{BASE}/login")
        print("Sign in to Overleaf in the opened window (5 min timeout)...", file=sys.stderr)
        page.wait_for_url(f"{BASE}/project**", timeout=300_000)
        ctx.storage_state(path=STATE)
        print(f"Session saved to {STATE}", file=sys.stderr)


def get_json(ctx: BrowserContext, route: str) -> object:
    """GET an Overleaf project route; exit with a hint if the session is invalid."""
    r = ctx.request.get(f"{BASE}/project/{PROJECT_ID}/{route}")
    if "/login" in r.url or "json" not in r.headers.get("content-type", ""):
        sys.exit(f"Not authenticated for /{route} (HTTP {r.status}). Run: python {Path(__file__).name} --login")
    return r.json()


def load_sources(ref: str) -> dict[str, str]:
    """Read all .tex/.bib files at a git ref (falls back to the working tree)."""
    try:
        names = subprocess.run(["git", "ls-tree", "-r", "--name-only", ref], cwd=REPO,
                               capture_output=True, text=True, check=True).stdout.split()
        return {n: subprocess.run(["git", "show", f"{ref}:{n}"], cwd=REPO, capture_output=True,
                                  encoding="utf-8", check=True).stdout
                for n in names if n.endswith((".tex", ".bib"))}
    except subprocess.CalledProcessError:
        return {str(f.relative_to(REPO)).replace("\\", "/"): f.read_text(encoding="utf-8")
                for f in REPO.rglob("*") if f.suffix in (".tex", ".bib")}


def locate(quote: str, pos: int, sources: dict[str, str]) -> str:
    """Find file:line for an anchored quote; exact offset match first, then text search."""
    # ponytail: text-match fallback picks the first file if a quote appears in several
    hits = [n for n, s in sources.items() if s[pos:pos + len(quote)] == quote] or \
           [n for n, s in sources.items() if quote in s]
    if not hits:
        return "?"
    s = sources[hits[0]]
    at = pos if s[pos:pos + len(quote)] == quote else s.index(quote)
    return f"{hits[0]}:{s.count(chr(10), 0, at) + 1}"


def fetch(ref: str, include_resolved: bool) -> None:
    """Fetch threads + anchors headlessly and print them as markdown."""
    if not STATE.exists() and not env("OVERLEAF_SESSION"):
        sys.exit("No session. Put overleaf_session2 cookie in .env as OVERLEAF_SESSION=..., "
                 f"or run: python {Path(__file__).name} --login")
    with sync_playwright() as p:
        ctx = launch(p, headless=True)
        threads: dict = get_json(ctx, "threads")  # type: ignore[assignment]
        try:
            ranges: list = get_json(ctx, "ranges")  # type: ignore[assignment]
        except SystemExit:
            ranges = []  # anchors are optional; threads alone are still useful
        ctx.storage_state(path=STATE)  # keep refreshed cookies

    sources = load_sources(ref)
    anchors = {c["op"]["t"]: (c["op"]["c"], c["op"]["p"])
               for doc in ranges for c in (doc.get("ranges") or {}).get("comments", [])}

    shown = 0
    for tid, t in threads.items():
        if t.get("resolved") and not include_resolved:
            continue
        shown += 1
        quote, pos = anchors.get(tid, ("", 0))
        where = locate(quote, pos, sources) if quote else "(anchor not found)"
        tag = " [resolved]" if t.get("resolved") else ""
        print(f"## {where}{tag} <!-- thread {tid} -->")
        if quote:
            print("> " + quote.replace("\n", "\n> "))
        for m in t.get("messages", []):
            u = m.get("user") or {}
            who = " ".join(filter(None, [u.get("first_name"), u.get("last_name")])) or u.get("email", "?")
            when = datetime.fromtimestamp(m["timestamp"] / 1000, timezone.utc).strftime("%Y-%m-%d")
            print(f"- **{who}** ({when}): {m['content']}")
        print()
    print(f"_{shown} thread(s); {len(threads) - shown} resolved hidden_" if not include_resolved
          else f"_{shown} thread(s)_")


def reply(path: Path) -> None:
    """Post replies from a JSON file {thread_id: message} to their threads."""
    replies: dict[str, str] = json.loads(path.read_text(encoding="utf-8"))
    with sync_playwright() as p:
        ctx = launch(p, headless=True)
        page = ctx.new_page()
        page.goto(f"{BASE}/project/{PROJECT_ID}")
        if "/login" in page.url:
            sys.exit("Not authenticated. Refresh OVERLEAF_SESSION in .env.")
        csrf = page.get_attribute('meta[name="ol-csrfToken"]', "content") or ""
        for tid, text in replies.items():
            r = ctx.request.post(f"{BASE}/project/{PROJECT_ID}/thread/{tid}/messages",
                                 data={"content": text}, headers={"X-Csrf-Token": csrf})
            print(f"{tid}: HTTP {r.status}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--login", action="store_true", help="sign in once in a visible browser")
    ap.add_argument("--ref", default="overleaf/main", help="git ref used to map comments to lines")
    ap.add_argument("--all", action="store_true", help="include resolved threads")
    ap.add_argument("--reply", type=Path, metavar="JSON", help="post replies from {thread_id: text}")
    a = ap.parse_args()
    if a.login:
        login()
    elif a.reply:
        reply(a.reply)
    else:
        fetch(a.ref, a.all)
