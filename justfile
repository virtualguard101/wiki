alias s := serve
alias d := deploy
alias jp := jupyter

serve:
    uv run mkdocs serve

deploy:
    uv run scripts/deploy.py

jupyter:
    uv run jupyter-lab
