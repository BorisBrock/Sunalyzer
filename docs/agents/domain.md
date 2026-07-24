# Domain docs

Sunalyzer uses a single-context domain-document structure.

## Before exploring

Read these when they exist and are relevant:

- `CONTEXT.md` for domain terminology and the project glossary
- `docs/adr/` for accepted architecture decisions
- `PROJECT_CONTROL.md` for the active roadmap and existing product or technical direction

If `CONTEXT.md` or `docs/adr/` does not exist, proceed silently. Create domain or decision documents only when the active task calls for them and the underlying terminology or decision has been resolved.

## Structure

```text
/
├── CONTEXT.md
└── docs/
    └── adr/
        └── NNNN-short-decision-name.md
```

## Working rules

- Use terminology defined in `CONTEXT.md`; avoid introducing competing synonyms.
- Treat unresolved terminology as a question, not an established domain concept.
- Read ADRs relevant to the area being changed.
- Explicitly identify proposals that contradict an existing ADR.
- Use the domain-modeling workflow when durable vocabulary or an architecture decision needs to be recorded.
