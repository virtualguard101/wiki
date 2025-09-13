import os
import logging
import colorlog
import json
from pathlib import Path
from datetime import datetime

# Configuration
NOTES_DIR = Path(__file__).parent.parent / 'docs' / 'notes'
INDEX_FILE = Path(__file__).parent.parent / 'docs' / 'notes' /'index.md'
START_MARKER = '<!-- recent_notes_start -->'
END_MARKER = '<!-- recent_notes_end -->'
MAX_NOTES = 11
DATE_FORMAT = '%Y-%m-%d'

# Initialize color log
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
))

logger = colorlog.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def get_title_relurl_date(file: Path) -> tuple[str, str, str]:
    """ 提取标题、相对路径（去掉 .md 或 .ipynb 后缀）、修改日期 

    Args:
        file (Path): 笔记文件路径

    Returns:
        title (str): 标题
        relurl (str): 相对路径
        mod_date (str): 修改日期
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
            logger.warning(f"Failed to extract title from {file}: {e}")
            title = None
    else:
        # 从Markdown文件中提取一级标题
        with file.open('r', encoding='utf-8') as f:
            for line in f:
                if line.lstrip().startswith('# '):
                    title = line.lstrip('# ').strip()
                    break
    title = title or file.stem
    mod_time = file.stat().st_mtime
    mod_date = datetime.fromtimestamp(mod_time).strftime(DATE_FORMAT)
    return title, relurl, mod_date

def main():
    """主调函数
    """
    logger.info("Refreshing recent notes at index page...")
    notes = list(NOTES_DIR.rglob('*.md')) + list(NOTES_DIR.rglob('*.ipynb'))
    if not notes:
        print(f"未在 {NOTES_DIR} 找到任何 Markdown 或 Jupyter Notebook 文件。")
        return
    # 按修改时间降序
    notes.sort(key=lambda p: p.stat().st_mtime, reverse=True)
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

    content = INDEX_FILE.read_text(encoding='utf-8')
    before, sep, rest = content.partition(START_MARKER)
    mid, sep2, after = rest.partition(END_MARKER)
    if not sep or not sep2:
        print(f"请在 {INDEX_FILE} 中添加标记 {START_MARKER} 和 {END_MARKER}。")
        return
    updated = before + START_MARKER + '\n' + new_section + '\n' + END_MARKER + after
    INDEX_FILE.write_text(updated, encoding='utf-8')
    print(f"已更新 {INDEX_FILE}，插入了 {len(recent) - 1} 条笔记链接。")
    logger.info("Refresh completed successfully!")



if __name__ == '__main__':
    main()
