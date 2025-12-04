alias s := serve
alias d := deploy
alias jp := jupyter
alias sc := sync
alias ob := obsidian

serve:
    uv run mkdocs serve

deploy:
    uv run scripts/deploy.py

jupyter:
    uv run jupyter-lab

sync:
    git checkout main
    git merge obsidian

obsidian:
    git checkout obsidian
