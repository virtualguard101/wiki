alias s := serve
alias d := deploy

serve:
    uv run mkdocs serve

deploy:
    uv run scripts/deploy.py
