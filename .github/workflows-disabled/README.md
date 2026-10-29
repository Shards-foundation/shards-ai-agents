# Disabled workflows

These workflows were inherited from upstream crewAI and are intentionally parked here
(GitHub only runs files directly under `.github/workflows/`):

- `publish.yml`, `nightly.yml` - publish packages to PyPI with upstream credentials/trusted-publisher setup.
- `docs-broken-links.yml` - Mintlify docs link checker tied to the upstream docs site.
- `agents-md-eval.yml` - LLM-backed eval that needs upstream API-key secrets.

Move a file back into `.github/workflows/` and adapt secrets/environments once you are ready to use it.
Nothing here is published automatically.
