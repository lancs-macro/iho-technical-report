---
name: overleaf-comments
description: Retrieve review comments from the IHO technical report's Overleaf project (id 6a13188773f44487d10a0a75) and map them to file:line in this repo. Use when the user asks for Overleaf comments, reviewer feedback, or "what did people comment on the report".
---

# Overleaf comments

Overleaf review comments are not in git. `fetch_comments.py` reads them through
Overleaf's internal JSON routes in a headless Playwright session.

## Steps

1. **Refresh the `overleaf` remote** so comment offsets line up with the latest text
   (token comes from `.env`, passed per-command, never stored or echoed):
   ```bash
   T=$(grep -E '^OVERLEAF_GIT_AUTH=' .env | cut -d= -f2- | tr -d '"'"'"'\r ') && \
   git -c credential.helper= -c http.extraHeader="Authorization: Basic $(printf 'git:%s' "$T" | base64 -w0)" fetch overleaf
   ```
   If the `overleaf` remote is missing: `git remote add overleaf https://git.overleaf.com/6a13188773f44487d10a0a75`.

2. **Fetch comments** (from the repo root):
   ```bash
   python .claude/skills/overleaf-comments/fetch_comments.py        # open threads
   python .claude/skills/overleaf-comments/fetch_comments.py --all  # include resolved
   ```

3. **If it exits with "No session" / "Not authenticated"**: ask the user to refresh the
   cookie — overleaf.com → F12 → Application → Cookies → `www.overleaf.com` → copy
   `overleaf_session2` → save in `.env` as `OVERLEAF_SESSION=...`. Then rerun step 2.
   (`--login` opens a headed browser instead, but Google SSO blocks it; only works
   with email/password accounts.) Never print the cookie value.

4. **Report**: group comments by file, quote the anchored text, give clickable
   `file:line` links, and summarise what each comment asks for. Do not edit the
   `.tex` files unless the user asks.

## Replying to threads

Each heading carries `<!-- thread <id> -->`. Write `{ "<id>": "reply text" }` to a
JSON file in the scratchpad and run `fetch_comments.py --reply <file>` (HTTP 204 =
posted). Replies are visible to collaborators: only post what the user asked for.

## Pushing edits back to Overleaf

The GitHub `main` and `overleaf/main` share no history. After re-fetching, check
that `overleaf/main^{tree}` still equals the tree the edits were based on, then
`git commit-tree HEAD^{tree} -p overleaf/main -m "..."` and push that commit to
`overleaf main` (same token header as step 1). Never force-push.

## Notes
- The routes are undocumented; if the JSON shape changes, inspect the raw
  response (`ctx.request.get(...).text()`) and adjust `fetch()`.
- Lines are resolved against `overleaf/main`; pass `--ref HEAD` to use local.
