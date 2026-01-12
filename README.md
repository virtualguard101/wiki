# virtualguard101's Wiki

The site used for storing my **documentations** which recorded the process of my self-learning in Computer Science.

The main part except **Home** include **Notebook**, **Blog**, **Projects** 3 sections. The infomation of each section is available at the main page of these sections.

## Read in obsidian

Clone the `obsidian` branch and use [Obsidian](https://docs.obsidian.md/) to read the notebook.

```bash
git clone -b obsidian https://github.com/virtualguard101/note.git
```

Then open the `note/docs` folder in Obsidian.

## Read in localhost

Use [MkDocs](https://github.com/mkdocs/mkdocs) & [Mkdocs for Material](https://github.com/squidfunk/mkdocs-material) to build in localhost.

- Clone the repository

  ```bash
  git clone -b main https://github.com/virtualguard101/note.git
  ```

- Install dependencies by [uv](https://docs.astral.sh/uv/)

  ```bash
  uv sync
  ```

- Deploy by `mkdocs` locally

  ```bash
  uv run mkdocs serve
  ```

Then access [localhost:8000](http://127.0.0.1:8000/) in browser.
