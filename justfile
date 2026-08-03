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
# Uses scripts/notion_sync.py (not `uvx mkdocs-note ns`): mkdocs-note 3.2.0's
# convert_inline_math still rewrites $0/$@/$# inside code and link labels.
notion-sync *args:
    #!/usr/bin/env bash
    set -euo pipefail
    args=( {{args}} )
    if [[ ${#args[@]} -gt 0 && ${args[0]} == -- ]]; then
      args=( "${args[@]:1}" )
    fi
    uv run scripts/notion_sync.py "${args[@]}"

notion-sync-full *args:
    #!/usr/bin/env bash
    set -euo pipefail
    args=( {{args}} )
    if [[ ${#args[@]} -gt 0 && ${args[0]} == -- ]]; then
      args=( "${args[@]:1}" )
    fi
    uv run scripts/notion_sync.py --full "${args[@]}"
