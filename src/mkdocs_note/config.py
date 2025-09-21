from pathlib import Path
from dataclasses import dataclass, field
from typing import Set

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
