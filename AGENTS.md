# AGENTS.md — horizon-incubator

Experimental verticals R&D for Horizon Protocol (ridesDAO, BuildDAO specs). Prototypes, not production. Public repo.

## Stack
- Static HTML spec documents under `Verticals/` + Python verification scripts (`test_*.py`). No build system or package manager.
- Rendered specs use inline CSS/JS with CSP hashes — after editing any inline `<script>`, recompute its CSP hash (see `test_csp.py`).

## Git rules
- Branch FROM `staging`, PR against `staging`; promotion to `main` is manual. Never push branches directly.
- Conventional commits. `.jules/` lowercase only. Keep experiments free of secrets and internal endpoints.
