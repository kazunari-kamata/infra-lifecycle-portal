# AGENTS.md

## Project

This repository is `infra-lifecycle-portal`.

It is a portfolio-grade infrastructure lifecycle management tool for small and mid-sized operation teams.

The project should demonstrate:

- infrastructure operation knowledge
- EOL risk detection
- OS and middleware migration planning
- reproducible runbooks
- verification checklists
- rollback planning
- CLI implementation
- API implementation
- frontend dashboard
- Docker-based local execution
- GitHub Actions CI

## Main concept

This is not a simple demo app.

It should look like a realistic tool created by an infrastructure / DevOps engineer who has experience with:

- CentOS to RHEL / Rocky Linux migration
- Linux server operation
- middleware lifecycle management
- operational automation
- migration validation
- incident prevention
- service continuity

## Technical stack

Use the following stack:

- Backend: Python 3.12 + FastAPI
- CLI: Python + Typer
- Frontend: React + TypeScript + Vite
- Data format: YAML
- Tests: pytest
- Container: Docker / Docker Compose
- CI: GitHub Actions

## Important rules

- Create practical, readable, maintainable code.
- Keep the first version small but complete.
- Do not over-engineer.
- Include sample data.
- Include documentation.
- Include tests.
- Include commands in README that can be copied and executed.
- Prefer clear directory structure over clever abstractions.
- All generated text should be professional and suitable for public GitHub.
- Avoid fake claims, fake companies, fake production users, or exaggerated metrics.

## MVP scope

Implement the following minimum features:

1. Read `examples/inventory.yml`
2. Detect lifecycle risks for OS / middleware / language runtimes
3. Calculate risk level: HIGH / MEDIUM / LOW / INFO
4. Generate Markdown report
5. Provide CLI command:
   - `ilp scan examples/inventory.yml`
   - `ilp report examples/inventory.yml --output examples/report-sample.md`
6. Provide FastAPI endpoint:
   - `GET /health`
   - `POST /scan`
7. Provide simple frontend dashboard:
   - upload or load sample inventory
   - show risk summary
   - show server list
   - show detected risks
8. Provide Docker Compose startup:
   - backend
   - frontend
9. Provide GitHub Actions:
   - backend tests
   - CLI tests

## Documentation required

Create:

- README.md
- docs/architecture.md
- docs/service-concept.md
- docs/migration-policy.md
- runbooks/centos-to-rocky.md
- runbooks/rollback-template.md
- runbooks/verification-checklist.md

## Tone

The project should look useful for real-world infrastructure operation and also suitable as a professional portfolio.

## Language policy

- README, docs, runbooks, generated reports, frontend UI labels, and code comments should be written in Japanese.
- Keep command names, file paths, function names, API paths, package names, and risk levels in English.
- Use clear and practical Japanese suitable for infrastructure operation documentation.
- Avoid exaggerated claims or fake adoption records.
