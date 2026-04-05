# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a personal wiki built with [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. It uses [uv](https://docs.astral.sh/uv/) for Python dependency management and [just](https://github.com/casey/just) for task automation.

The wiki contains three main content sections:
- **docs/obsidian/** – Learning notes organized by topic (Computer Science, Machine Learning, etc.), designed to be readable in Obsidian.
- **docs/blog/** – Blog posts with RSS feed support.
- **docs/projects/** – Project logs and documentation.

The site is deployed to GitHub Pages via the `main` branch, while the `obsidian` branch holds a clone of the notes optimized for Obsidian.

## Common Commands

All development tasks are run through `just`. The most frequently used commands are:

| Command               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `just serve` (or `s`) | Start the local MkDocs development server at http://127.0.0.1:8000         |
| `just deploy` (or `d`)| Deploy the site to GitHub Pages (runs `scripts/deploy.py`)                 |
| `just sync` (or `sc`) | Merge changes from the `obsidian` branch into `main` and deploy            |
| `just obsidian` (or `ob`)| Switch to the `obsidian` branch for editing notes                         |
| `just update` (or `u`) | Update the `obsidian` branch and run `scripts/update.py`                  |
| `just usync`          | Run `update`, `sync`, and switch back to `obsidian`                       |
| `just newblog title="..."` | Create a new blog post from a template                                 |
| `just jupyter` (or `jp`)| Launch Jupyter Lab for working with notebooks                           |

Under the hood:
- `uv sync` – Install or update Python dependencies from `pyproject.toml`.
- `uv run mkdocs serve` – Start the MkDocs server (same as `just serve`).
- `uv run mkdocs build` – Build the static site to the `site/` directory.

## Branch Strategy

- **`main`** – The deployed branch. Contains the fully built MkDocs site (HTML, CSS, JS). Never edit content directly here; use `just sync` to merge from `obsidian`.
- **`obsidian`** – The content branch. All notes, blog posts, and project logs are edited here. The `docs/obsidian/` directory is structured for optimal viewing in Obsidian.

To make changes:
1. `just obsidian` – switch to the content branch.
2. Edit files in `docs/obsidian/`, `docs/blog/`, or `docs/projects/`.
3. `just sync` – merge into `main` and deploy.

## Architecture

### MkDocs Configuration
The site is configured in `mkdocs.yml`. Key plugins include:
- `mkdocs-material` – Theming and UI features.
- `mkdocs-jupyter` – Render Jupyter notebooks (`.ipynb`) inline.
- `mkdocs-note` – Provides recent‑notes and graph views.
- `mkdocs-rss-plugin` – Generates an RSS feed for the blog.
- `mkdocs-minify-plugin` – Minifies HTML, CSS, and JavaScript.
- `mkdocs-git-revision-date-localized-plugin` – Adds last‑updated dates.
- `mkdocs-awesome-nav` – Improved navigation rendering.

### Customizations
- **`overrides/`** – Custom HTML templates that override Material theme components.
- **`docs/assets/`** – Custom CSS, JavaScript, and webfonts.
- **`scripts/hooks/`** – MkDocs hooks that run during the build process (e.g., adding copyright notices, modifying links, enabling fancybox for images).
- **`scripts/deploy.py`** – Handles the GitHub Pages deployment (builds the site, commits to `main`, and pushes).
- **`scripts/update.py`** – Updates the `obsidian` branch with external changes (e.g., pulling from upstream templates).

### Content Structure
- **`docs/obsidian/`** – Notes are grouped by topic (`MachineLearning/`, `Math/`, `OperatingSystem/`, etc.). Each topic folder contains Markdown files and optionally notebooks.
- **`docs/blog/posts/`** – Blog posts in Markdown, with front‑matter for dates, categories, and tags.
- **`docs/projects/`** – Project logs and related assets.

### Styling and Extensions
- Custom CSS files in `docs/assets/stylesheets/` (theme.css, feature.css, temp-patch.css, home.css, admonitions.css).
- Custom JavaScript in `docs/assets/javascripts/` (mathjax.js, sakana-widget.js, home.js, links.js).
- Math rendering via MathJax (configured in `mkdocs.yml`).
- Extended Markdown syntax through `pymdown-extensions` (admonitions, tabs, superfences, arithmetic, emoji, etc.).

## Development Workflow

1. **Setup** – Run `uv sync` to install dependencies.
2. **Edit content** – Navigate to `docs/obsidian/` or `docs/blog/` and modify Markdown/notebook files.
3. **Preview** – Run `just serve` and open http://127.0.0.1:8000.
4. **Deploy** – After testing, run `just sync` to merge changes into `main` and deploy.
5. **Blogging** – Use `just newblog title="My Post"` to create a new blog post template.

## Cursor AI Rules

The project includes a Cursor rule (`.cursor/rules/learning-agent.mdc`) that configures the AI assistant to act as a CS learning mentor. Key points:
- The AI should explain concepts concisely, using analogies for abstract ideas.
- When expanding a concept, follow the “Where does it come from? – What is it? – Where does it go?” framework.
- Assess user understanding on a 1–10 depth scale (surface knowledge to cutting‑edge research).
- Do not modify files unless the user explicitly asks for improvements.

## CI/CD

A GitHub Actions workflow (`.github/workflows/ci.yml`) automatically deploys the site on pushes to `main`/`master`. It caches dependencies and runs `mkdocs gh-deploy --force`.

## Notes

- Python 3.12 is required (specified in `.python-version` and `pyproject.toml`). Use `uv sync` to install dependencies.
- The `requirements.txt` file is maintained for compatibility with the CI workflow, but primary dependency management is via `uv` and `pyproject.toml`.
- Jupyter notebooks are supported and rendered inline; they are not executed during build (`execute: false` in `mkdocs.yml`).
- The site uses Google Analytics (property G‑3JKT1BJEB6) and includes social links (GitHub, Twitter).
