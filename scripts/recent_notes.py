#!/usr/bin/env python3
"""
Recent Notes Updater

自动更新笔记索引页面中的最近笔记列表。
支持 Markdown 和 Jupyter Notebook 文件。
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, Set
from functools import lru_cache

import colorlog


@dataclass
class Config:
    """配置类，集中管理所有配置参数"""
    # 路径配置
    project_root: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    notes_dir: Path = field(init=False)
    index_file: Path = field(init=False)
    
    # 文件标记
    start_marker: str = '<!-- recent_notes_start -->'
    end_marker: str = '<!-- recent_notes_end -->'
    
    # 数量限制
    max_notes: int = 11
    
    # 日期格式
    git_date_format: str = '%a %b %d %H:%M:%S %Y %z'
    output_date_format: str = '%Y-%m-%d %H:%M:%S'
    
    # 文件过滤
    supported_extensions: Set[str] = field(default_factory=lambda: {'.md', '.ipynb'})
    exclude_patterns: Set[str] = field(default_factory=lambda: {'index.md', 'README.md'})
    exclude_dirs: Set[str] = field(default_factory=lambda: {'__pycache__', '.git', 'node_modules'})
    
    # 缓存配置
    cache_size: int = 128
    
    def __post_init__(self):
        self.notes_dir = self.project_root / 'docs' / 'notes'
        self.index_file = self.notes_dir / 'index.md'


@dataclass
class NoteInfo:
    """笔记信息数据类"""
    file_path: Path
    title: str
    relative_url: str
    modified_date: str
    file_size: int
    modified_time: float


class Logger:
    """日志管理器"""
    
    def __init__(self, name: str = __name__):
        self.logger = colorlog.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """设置彩色日志格式"""
        if not self.logger.handlers:
            handler = colorlog.StreamHandler()
            formatter = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                }
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)
    
    def debug(self, msg: str):
        self.logger.debug(msg)
    
    def info(self, msg: str):
        self.logger.info(msg)
    
    def warning(self, msg: str):
        self.logger.warning(msg)
    
    def error(self, msg: str):
        self.logger.error(msg)


class FileScanner:
    """文件扫描器"""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
    
    def scan_notes(self) -> List[Path]:
        """扫描笔记目录，返回所有支持的笔记文件"""
        if not self.config.notes_dir.exists():
            self.logger.warning(f"Notes directory does not exist: {self.config.notes_dir}")
            return []
        
        notes = []
        
        try:
            for file_path in self.config.notes_dir.rglob('*'):
                if self._is_valid_note_file(file_path):
                    notes.append(file_path)
        except PermissionError as e:
            self.logger.error(f"Permission denied while scanning {self.config.notes_dir}: {e}")
            return []
        
        self.logger.info(f"Found {len(notes)} note files")
        return notes
    
    def _is_valid_note_file(self, file_path: Path) -> bool:
        """检查文件是否为有效的笔记文件"""
        if not file_path.is_file():
            return False
        
        # 检查扩展名
        if file_path.suffix.lower() not in self.config.supported_extensions:
            return False
        
        # 检查排除模式
        if file_path.name in self.config.exclude_patterns:
            return False
        
        # 检查排除目录
        for part in file_path.parts:
            if part in self.config.exclude_dirs:
                return False
        
        return True


class NoteProcessor:
    """笔记处理器"""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
    
    def process_note(self, file_path: Path) -> Optional[NoteInfo]:
        """处理单个笔记文件，提取信息"""
        try:
            # 获取基本信息
            stat = file_path.stat()
            
            # 提取标题
            title = self._extract_title(file_path)
            if not title or title == "Notebook":
                return None
            
            # 生成相对URL
            relative_url = self._generate_relative_url(file_path)
            
            # 获取修改时间
            modified_date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            return NoteInfo(
                file_path=file_path,
                title=title,
                relative_url=relative_url,
                modified_date=modified_date,
                file_size=stat.st_size,
                modified_time=stat.st_mtime
            )
            
        except Exception as e:
            self.logger.error(f"Failed to process note {file_path}: {e}")
            return None
    
    def _extract_title(self, file_path: Path) -> Optional[str]:
        """从文件中提取标题"""
        if file_path.suffix == '.ipynb':
            return self._extract_title_from_notebook(file_path)
        else:
            return self._extract_title_from_markdown(file_path)
    
    def _extract_title_from_notebook(self, file_path: Path) -> Optional[str]:
        """从Jupyter Notebook中提取标题"""
        try:
            with file_path.open('r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'markdown':
                    source = cell.get('source', [])
                    if isinstance(source, list):
                        content = ''.join(source)
                    else:
                        content = source
                    
                    # 查找第一个一级标题
                    for line in content.split('\n'):
                        line = line.strip()
                        if line.startswith('# '):
                            return line[2:].strip()
                            
        except Exception as e:
            self.logger.warning(f"Failed to extract title from notebook {file_path}: {e}")
        
        return file_path.stem
    
    def _extract_title_from_markdown(self, file_path: Path) -> Optional[str]:
        """从Markdown文件中提取标题"""
        try:
            with file_path.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('# '):
                        return line[2:].strip()
        except Exception as e:
            self.logger.warning(f"Failed to extract title from markdown {file_path}: {e}")
        
        return file_path.stem
    
    def _generate_relative_url(self, file_path: Path) -> str:
        """生成MkDocs格式的相对URL"""
        relpath = file_path.relative_to(self.config.index_file.parent)
        relurl = relpath.with_suffix('').as_posix() + '/'
        
        # 处理index文件
        if 'index' in relurl:
            relurl = relurl.replace('index/', '')
        
        return relurl


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self._last_notes_hash: Optional[str] = None
        self._last_content_hash: Optional[str] = None
    
    def should_update_notes(self, notes: List[NoteInfo]) -> bool:
        """检查是否需要更新笔记列表"""
        current_hash = self._calculate_notes_hash(notes)
        if self._last_notes_hash != current_hash:
            self._last_notes_hash = current_hash
            return True
        return False
    
    def should_update_content(self, content: str) -> bool:
        """检查是否需要更新文件内容"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        if self._last_content_hash != content_hash:
            self._last_content_hash = content_hash
            return True
        return False
    
    def _calculate_notes_hash(self, notes: List[NoteInfo]) -> str:
        """计算笔记列表的哈希值"""
        notes_info = []
        for note in notes:
            notes_info.append(f"{note.file_path.name}:{note.modified_time}:{note.file_size}")
        return hashlib.md5('|'.join(notes_info).encode()).hexdigest()


class IndexUpdater:
    """索引文件更新器"""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
    
    def update_index(self, notes: List[NoteInfo]) -> bool:
        """更新索引文件"""
        if not self.config.index_file.exists():
            self.logger.error(f"Index file does not exist: {self.config.index_file}")
            return False
        
        try:
            # 读取现有内容
            content = self.config.index_file.read_text(encoding='utf-8')
            
            # 生成新的笔记列表HTML
            new_section = self._generate_html_list(notes)
            
            # 替换内容
            updated_content = self._replace_section(content, new_section)
            if updated_content is None:
                return False
            
            # 写入文件
            self.config.index_file.write_text(updated_content, encoding='utf-8')
            self.logger.info(f"Updated index file with {len(notes) - 1} notes")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update index file: {e}")
            return False
    
    def _generate_html_list(self, notes: List[NoteInfo]) -> str:
        """生成HTML列表"""
        items = []
        for note in notes:
            items.append(
                f'<li><div style="display:flex; justify-content:space-between; align-items:center;">'
                f'<a href="{note.relative_url}">{note.title}</a>'
                f'<span style="font-size:0.8em;">{note.modified_date}</span>'
                '</div></li>'
            )
        
        return '<ul>\n' + '\n'.join(items) + '\n</ul>'
    
    def _replace_section(self, content: str, new_section: str) -> Optional[str]:
        """替换指定标记之间的内容"""
        start_idx = content.find(self.config.start_marker)
        end_idx = content.find(self.config.end_marker)
        
        if start_idx == -1 or end_idx == -1:
            self.logger.error(
                f"Markers not found. Please add {self.config.start_marker} "
                f"and {self.config.end_marker} to the index file."
            )
            return None
        
        # 确保结束标记在开始标记之后
        if end_idx <= start_idx:
            self.logger.error("End marker found before start marker")
            return None
        
        start_pos = start_idx + len(self.config.start_marker)
        end_pos = end_idx
        
        return (
            content[:start_pos] + 
            '\n' + new_section + '\n' + 
            content[end_pos:]
        )


class RecentNotesUpdater:
    """最近笔记更新器主类"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.logger = Logger()
        
        # 初始化组件
        self.file_scanner = FileScanner(self.config, self.logger)
        self.note_processor = NoteProcessor(self.config, self.logger)
        self.cache_manager = CacheManager(self.logger)
        self.index_updater = IndexUpdater(self.config, self.logger)
    
    def update(self) -> bool:
        """执行更新操作"""
        self.logger.info("Starting recent notes update...")
        
        try:
            # 扫描笔记文件
            note_files = self.file_scanner.scan_notes()
            if not note_files:
                self.logger.warning("No note files found")
                return False
            
            # 处理笔记文件
            notes = []
            for file_path in note_files:
                note_info = self.note_processor.process_note(file_path)
                if note_info:
                    notes.append(note_info)
            
            if not notes:
                self.logger.warning("No valid notes found")
                return False
            
            # 检查缓存
            if not self.cache_manager.should_update_notes(notes):
                self.logger.info("Notes unchanged, skipping update")
                return True
            
            # 按修改时间排序
            notes.sort(key=lambda n: n.modified_time, reverse=True)
            recent_notes = notes[:self.config.max_notes]
            
            # 更新索引文件
            success = self.index_updater.update_index(recent_notes)
            if success:
                self.logger.info(f"Successfully updated recent notes ({len(recent_notes) - 1} notes)")
            else:
                self.logger.error("Failed to update index file")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Unexpected error during update: {e}")
            return False


def main():
    """主函数"""
    updater = RecentNotesUpdater()
    success = updater.update()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())