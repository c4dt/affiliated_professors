# C4DT Affiliated Professors Tracker

An agentic tracker that follows the research of C4DT's ~40 affiliated professors.

Every weekday a GitHub Actions job picks the **least-recently-updated** professor
(so each is revisited roughly every two months), reads their websites, code
repositories, and publication feed, updates that professor's file under
[`professors/`](professors/), regenerates the index, commits, and announces
significant updates to a Matrix channel.

👉 **The generated index of all professors is [PROFESSORS.md](PROFESSORS.md).**

## Updating

`professors.yaml` is the source of truth. After editing it (adding URLs, fixing an
ORCID, flipping `reviewed: true`, …), rebuild the index:

```bash
devbox run regen-professors     # rebuild PROFESSORS.md from professors.yaml
```

Do not hand-edit `PROFESSORS.md` — it is generated and will be overwritten.

Other commands:

```bash
devbox run update                    # update the least-recently-updated professor
devbox run update -- --slug <slug>   # update one specific professor
devbox run announce                  # post the last update to Matrix
devbox run resolve-orcids            # fill candidate ORCIDs for review
devbox run bootstrap                 # (re)build the registry from the C4DT labs listing
devbox run retire <slug>             # freeze a profile and drop it from rotation
devbox run unretire <slug>           # resume tracking a retired professor
devbox run test                      # run the unit tests
```

### Retiring a professor

When a professor leaves EPFL or should no longer be tracked, retire them:

```bash
devbox run retire <slug>
```

This sets `retired: true` in `professors.yaml`, so the daily rotation skips
them and their `professors/<SLUG>.md` profile is left frozen as-is. They stay
listed in `PROFESSORS.md` with a 🏁 retired badge. A manual
`devbox run update -- --slug <slug>` on a retired professor is refused unless
you pass `--force`. Reverse it with `devbox run unretire <slug>`.

### Recording meeting notes

Use `notes` to add a dated Notes section to a professor's profile from
free-form notes (the LLM extracts the professor name and date automatically):

> **Privacy:** notes are stored in a public repository. Do **not** include
> personal information — names of third parties, private contact details,
> off-the-record remarks, or any sensitive organisational context. Stick to
> publicly shareable research topics and outcomes.

```bash
# Pass text directly — avoid special shell characters (!, backticks) this way:
devbox run notes -- --file - <<'EOF'
Met with Alice Example on 2026-07-10.  She mentioned a new paper on X.
EOF

# Or pipe from another command:
cat notes.txt | devbox run notes -- --file -

# Or read from a file:
devbox run notes -- --file notes.txt

# Override the extracted slug/date if needed:
devbox run notes -- --file - --slug alice-example --date 2026-07-10 <<'EOF'
...
EOF
```

Local runs that hit the LLM / Firecrawl / Matrix need credentials: copy
`.env.example` to `.env` and fill it in (`.env` is gitignored). In CI these come
from GitHub Actions secrets and variables.

## Identifiers: ORCID and OpenAlex

Publications are tracked via [OpenAlex](https://openalex.org), anchored on each
professor's **ORCID** when available. ORCID is a stable, researcher-curated id;
OpenAlex's own author ids are name-clustered and prone to collisions (two people
sharing a name, or one person split across records). The daily job falls back to
a human-verified OpenAlex author id when there is no ORCID:

| `orcid` | `openalex_id` | Publication tracking |
|---------|---------------|----------------------|
| set     | (ignored)     | filter by ORCID — preferred; aggregates OpenAlex's duplicate author records |
| null    | set           | filter by OpenAlex author id — works, but may miss papers if OpenAlex split the author |
| null    | null          | skipped — the professor is still tracked from websites + code |

A **wrong** id is worse than none: it produces confidently-wrong publication
feeds. When you can't confirm an id, set it to `null`. The links in
[PROFESSORS.md](PROFESSORS.md) — rendered even for `reviewed: false` entries — let
you click through and verify each ORCID / OpenAlex record quickly.

## How it fits together

| File / dir | Role |
|------------|------|
| `professors.yaml` | Registry & rotation source of truth (one entry per professor) |
| `professors/<SLUG>.md` | Per-professor profile with a dated changelog |
| `PROFESSORS.md` | Generated index (one entry per professor + verification links) |
| `src/prof_tracker/` | The updater: registry, sources, agent, render, matrix, CLI |
| `.github/workflows/update.yml` | The daily scheduled run |

The updater is a plain CLI (`devbox run …`), so it runs identically locally and in
CI, and could move to a server cron unchanged.
