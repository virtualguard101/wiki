import os
import subprocess
import logging
import json
import hashlib
from pathlib import Path
from datetime import datetime
from mkdocs.config.defaults import MkDocsConfig

# Configuration
NOTES_DIR = Path(__file__).parent.parent.parent / 'docs' / 'notes'
INDEX_FILE = Path(__file__).parent.parent.parent / 'docs' / 'notes' / 'index.md'
START_MARKER = '<!-- recent_notes_start -->'
END_MARKER = '<!-- recent_notes_end -->'
MAX_NOTES = 11
# Git日期格式：Sun Sep 14 22:40:00 2025 +0800
GIT_DATE_FORMAT = '%a %b %d %H:%M:%S %Y %z'
# 输出日期格式：2025-09-15 08:30:12
OUTPUT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

log = logging.getLogger('mkdocs.plugins')

# 全局缓存变量
_last_update_hash = None
_last_notes_hash = None


def get_notes_hash(notes):
    """计算笔记列表的哈希值，用于检测变化
    
    Args:
        notes (list): 笔记列表

    Returns:
        hash (str): 笔记列表的哈希值
    """
    notes_info = []
    for note in notes:
        try:
            stat = note.stat()
            notes_info.append(f"{note.name}:{stat.st_mtime}:{stat.st_size}")
        except OSError:
            notes_info.append(f"{note.name}:0:0")
    return hashlib.md5('|'.join(notes_info).encode()).hexdigest()


def get_commit_date(file_path: Path) -> str:
    """获取最新的提交日期

    Args:
        file_path (Path): 笔记文件路径

    Returns:
        commit_date (str): 提交日期字符串
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ad", file_path],
            check=True,
            capture_output=True,
            text=True,
        )

        commit_date_str = result.stdout.strip()
        
        # 检查是否为空字符串
        if not commit_date_str:
            log.warning(f"No commit history for {file_path}, use modified date instead")
            mod_time = file_path.stat().st_mtime
            mod_date = datetime.fromtimestamp(mod_time).strftime(OUTPUT_DATE_FORMAT)
            return mod_date
        
        commit_date = datetime.strptime(commit_date_str, GIT_DATE_FORMAT)
        return commit_date.strftime(OUTPUT_DATE_FORMAT)

    except subprocess.CalledProcessError as e:
        log.warning(f"Failed to get commit date for {file_path}: {e}, use modified date instead")
        mod_time = file_path.stat().st_mtime
        mod_date = datetime.fromtimestamp(mod_time).strftime(OUTPUT_DATE_FORMAT)
        return mod_date
    except ValueError as e:
        log.warning(f"Failed to parse commit date for {file_path}: {e}, use modified date instead")
        mod_time = file_path.stat().st_mtime
        mod_date = datetime.fromtimestamp(mod_time).strftime(OUTPUT_DATE_FORMAT)
        return mod_date


def get_title_relurl_date(file: Path) -> tuple[str, str, str]:
    """ 提取标题、相对路径（去掉 .md 或 .ipynb 后缀）、修改日期 

    Args:
        file (Path): 笔记文件路径

    Returns:
        title (str): 标题
        relurl (str): 相对路径
        commit_date (str): 提交日期
    """
    relpath = file.relative_to(INDEX_FILE.parent)
    relurl = relpath.with_suffix('').as_posix() + '/'  # MkDocs URL 格式

    if 'index' in relurl:
        # 如果文件名是index，则去掉index/
        relurl = relurl.replace('index/', '')

    title = None
    if file.suffix == '.ipynb':
        # 从Jupyter notebook中提取第一个markdown cell的一级标题
        try:
            with file.open('r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'markdown':
                    source = cell.get('source', [])
                    if isinstance(source, list):
                        content = ''.join(source)
                    else:
                        content = source
                    
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('# '):
                            title = line[2:].strip()
                            break
                    if title:
                        break
        except Exception as e:
            log.warning(f"Failed to extract title from {file}: {e}")
            title = None
    else:
        # 从Markdown文件中提取一级标题
        with file.open('r', encoding='utf-8') as f:
            for line in f:
                if line.lstrip().startswith('# '):
                    title = line.lstrip('# ').strip()
                    break
    title = title or file.stem

    commit_date = get_commit_date(file)

    return title, relurl, commit_date


def update_recent_notes():
    """更新最近笔记列表
    """
    global _last_update_hash, _last_notes_hash
    
    # 检查目录是否存在
    if not NOTES_DIR.exists():
        log.warning(f"Notes directory {NOTES_DIR} does not exist")
        return
    
    notes = list(NOTES_DIR.rglob('*.md')) + list(NOTES_DIR.rglob('*.ipynb'))
    if not notes:
        log.warning(f"未在 {NOTES_DIR} 找到任何 Markdown 或 Jupyter Notebook 文件。")
        return
    
    # 计算当前笔记列表的哈希值
    current_notes_hash = get_notes_hash(notes)
    
    # 如果笔记没有变化，跳过更新
    if _last_notes_hash == current_notes_hash:
        return
    
    log.info("Refreshing recent notes at index page...")
    
    # 按提交时间降序排序
    notes.sort(key=lambda p: get_commit_date(p), reverse=True)
    recent = notes[:MAX_NOTES]

    # 生成 HTML 列表，标题和日期左右对齐，日期字体缩小
    items = []
    for md in recent:
        title, url, date = get_title_relurl_date(md)
        if title == "Notebook":
            continue
        items.append(
            f'<li><div style="display:flex; justify-content:space-between; align-items:center;">'
            f'<a href="{url}">{title}</a>'
            f'<span style="font-size:0.8em;">{date}</span>'
            '</div></li>'
        )
    new_section = '<ul>\n' + '\n'.join(items) + '\n</ul>'

    # 读取并更新索引文件
    if not INDEX_FILE.exists():
        log.warning(f"Index file {INDEX_FILE} does not exist")
        return
        
    content = INDEX_FILE.read_text(encoding='utf-8')
    before, sep, rest = content.partition(START_MARKER)
    mid, sep2, after = rest.partition(END_MARKER)
    if not sep or not sep2:
        log.warning(f"Please add markers {START_MARKER} and {END_MARKER} in {INDEX_FILE}.")
        return
    
    updated = before + START_MARKER + '\n' + new_section + '\n' + END_MARKER + after
    
    # 计算更新内容的哈希值
    update_hash = hashlib.md5(updated.encode()).hexdigest()
    
    # 如果内容没有变化，跳过写入
    if _last_update_hash == update_hash:
        _last_notes_hash = current_notes_hash
        return
    
    INDEX_FILE.write_text(updated, encoding='utf-8')
    log.info(f"Updated {INDEX_FILE}, inserted {len(recent) - 1} note links.")
    
    # 更新缓存
    _last_update_hash = update_hash
    _last_notes_hash = current_notes_hash


def on_pre_build(config):
    """MkDocs 构建前钩子 - 在构建前更新最近笔记
    """
    update_recent_notes()
    return config
