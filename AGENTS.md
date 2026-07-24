# Repository guidance

Sunalyzer is a local-first solar monitoring application with a Python/Flask backend, SQLite storage, and a static JavaScript frontend.

- `backend/`: acquisition, devices, database, configuration, and HTTP server
- `site/`: frontend; treat `site/lib/` as vendored code
- `pytest/`: automated tests
- `templates/`: deployment and configuration examples
- `doc/`: installation and research documentation

## Commands

- Install: `python -m pip install -r requirements.txt`
- Test: `pytest`
- Check Python errors: `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
- Full advisory lint: `flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics`
- Build container: `docker build -t sunalyzer .`

## Documentation

- `README.md`: project and installation overview
- `PROJECT_CONTROL.md`, when present: active roadmap, product direction, and technical decisions
- `docs/agents/`: engineering-skill configuration
- Future domain vocabulary belongs in `CONTEXT.md`; future architecture decisions belong in `docs/adr/`.

## Agent working rules

- Inspect the working tree and preserve unrelated changes.
- Read `PROJECT_CONTROL.md`, when present, before significant product or architecture work.
- Keep changes scoped and add or update tests for changed behavior.
- Do not modify vendored files under `site/lib/` unless explicitly requested.
- Do not create GitHub issues or new decision documents unless the task requests them.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues for `hothman7/Sunalyzer`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default Matt Pocock triage-label vocabulary. See `docs/agents/triage-labels.md`.

### Domain docs

Use the single-context domain-document layout. See `docs/agents/domain.md`.
