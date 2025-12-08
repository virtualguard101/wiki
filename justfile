alias s := serve
alias d := deploy
alias jp := jupyter
alias sc := sync
alias ob := obsidian
alias u := update
alias us := usync

serve:
    uv run mkdocs serve

deploy:
    uv run scripts/deploy.py

jupyter:
    uv run jupyter-lab

sync:
    git checkout main
    git merge obsidian -m "Sync from obsidian"
    just d

obsidian:
    git checkout obsidian

update:
    just ob
    uv run scripts/update.py

usync:
    just u
    just sc
