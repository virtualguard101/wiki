alias s := serve
alias d := deploy
alias jp := jupyter
alias sc := sync
alias ob := obsidian
alias u := update
alias us := usync
alias nb := newblog
alias mi := mv-image
alias ns := notion-sync
alias nsf := notion-sync-full

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
    just ns

usync:
    just u
    just sc
    just ob

newblog title="":
    cp templates/blog.md "docs/blog/posts/{{ title }}.md"

mv-image dest:
    uv run scripts/mv_image.py {{ dest }}

# Incremental Notion sync (git diff). Examples:
#   just notion-sync --dry-run
#   just notion-sync --base HEAD~3 --section obsidian/
#   just notion-sync-full --section obsidian/
notion-sync args="":
    uvx mkdocs-note ns {{ args }}
notion-sync-full:
    uvx mkdocs-note ns --full
