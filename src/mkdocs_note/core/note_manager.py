from dataclasses import dataclass
from pathlib import Path

@dataclass
class NoteInfo:
    """笔记信息数据类"""
    file_path: Path
    title: str
    relative_url: str
    modified_date: str
    file_size: int
    modified_time: float
