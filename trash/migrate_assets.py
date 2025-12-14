#!/usr/bin/env python3
"""
mkdocs-note v2.0.0 资产迁移脚本

此脚本用于将旧版本的集中式资产目录结构迁移到新版本的分布式资产目录结构。

旧版本结构: docs/notes/assets/{category}.assets/{subcategory}/...
新版本结构: docs/notes/{path}/assets/{filename}/...

特性说明:
- mkdocs-note v2.0.0 支持在笔记文件中直接使用文件名引用资产
- 插件会自动在对应的 assets/{filename}/ 目录中查找资产文件
- 迁移后，笔记文件中的引用将被简化为仅包含文件名

使用方法:
    python scripts/migrate_assets.py [--dry-run] [--backup]

参数:
    --dry-run: 仅显示将要执行的操作，不实际执行
    --backup: 在迁移前创建备份
"""

import os
import shutil
import re
import argparse
from pathlib import Path
from typing import List, Tuple, Dict
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AssetMigrator:
    def __init__(self, notes_dir: str = "docs/notes", dry_run: bool = False, backup: bool = False):
        self.notes_dir = Path(notes_dir)
        self.assets_dir = self.notes_dir / "assets"
        self.dry_run = dry_run
        self.backup = backup
        self.migration_map: Dict[str, str] = {}
        
    def find_note_files(self) -> List[Path]:
        """查找所有笔记文件"""
        note_files = []
        for pattern in ["**/*.md"]:
            note_files.extend(self.notes_dir.glob(pattern))
        return note_files
    
    def extract_asset_references(self, note_file: Path) -> List[str]:
        """从笔记文件中提取资产引用"""
        asset_refs = []
        try:
            with open(note_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 匹配图片引用模式
            patterns = [
                r'!\[.*?\]\(([^)]+\.(png|jpg|jpeg|gif|svg|webp))\)',  # Markdown图片
                r'<img[^>]+src=["\']([^"\']+\.(png|jpg|jpeg|gif|svg|webp))["\']',  # HTML img标签
                r'"([^"]+\.(png|jpg|jpeg|gif|svg|webp))"',  # 其他引用
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    asset_refs.append(match[0] if isinstance(match, tuple) else match)
                    
        except Exception as e:
            logger.warning(f"读取文件 {note_file} 时出错: {e}")
            
        return list(set(asset_refs))  # 去重
    
    def find_asset_file(self, asset_ref: str) -> Path:
        """根据引用路径查找实际的资产文件"""
        # 处理相对路径
        if not asset_ref.startswith('/'):
            # 在集中式资产目录中查找
            possible_paths = [
                self.assets_dir / asset_ref,
                self.notes_dir / asset_ref,
            ]
            
            # 在集中式资产目录的子目录中递归查找
            for category_dir in self.assets_dir.iterdir():
                if category_dir.is_dir() and category_dir.name.endswith('.assets'):
                    possible_paths.append(category_dir / asset_ref)
                    # 进一步在子目录中查找
                    for subdir in category_dir.rglob('*'):
                        if subdir.is_dir():
                            possible_paths.append(subdir / asset_ref)
            
            for path in possible_paths:
                if path.exists() and path.is_file():
                    return path
                    
        # 如果找不到，返回原始路径
        return Path(asset_ref)
    
    def determine_target_asset_dir(self, note_file: Path) -> Path:
        """确定目标资产目录"""
        # 获取笔记文件的相对路径（相对于notes_dir）
        rel_path = note_file.relative_to(self.notes_dir)
        # 移除文件扩展名，创建对应的assets目录
        note_stem = rel_path.stem
        note_parent = rel_path.parent
        
        return self.notes_dir / note_parent / "assets" / note_stem
    
    def migrate_assets_for_note(self, note_file: Path) -> Dict[str, str]:
        """为单个笔记文件迁移资产"""
        asset_refs = self.extract_asset_references(note_file)
        if not asset_refs:
            return {}
            
        target_asset_dir = self.determine_target_asset_dir(note_file)
        migration_map = {}
        
        logger.info(f"处理笔记文件: {note_file}")
        logger.info(f"目标资产目录: {target_asset_dir}")
        
        # 创建目标目录
        if not self.dry_run:
            target_asset_dir.mkdir(parents=True, exist_ok=True)
        
        for asset_ref in asset_refs:
            source_file = self.find_asset_file(asset_ref)
            
            if source_file.exists():
                # 确定目标文件名
                target_file = target_asset_dir / source_file.name
                
                # 记录迁移映射
                migration_map[asset_ref] = str(target_file.relative_to(self.notes_dir))
                
                if not self.dry_run:
                    # 复制文件
                    shutil.copy2(source_file, target_file)
                    logger.info(f"  复制: {source_file} -> {target_file}")
                else:
                    logger.info(f"  [DRY-RUN] 将复制: {source_file} -> {target_file}")
            else:
                logger.warning(f"  找不到资产文件: {asset_ref}")
                
        return migration_map
    
    def update_note_file(self, note_file: Path, migration_map: Dict[str, str]):
        """更新笔记文件中的资产引用路径"""
        if not migration_map:
            return
            
        try:
            with open(note_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 更新引用路径 - 只需要文件名，mkdocs-note会自动在对应assets目录中查找
            for old_ref, new_ref in migration_map.items():
                # 提取文件名（不包含路径）
                filename = Path(new_ref).name
                content = content.replace(old_ref, filename)
            
            if content != original_content:
                if not self.dry_run:
                    with open(note_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    logger.info(f"  更新引用路径: {note_file}")
                else:
                    logger.info(f"  [DRY-RUN] 将更新引用路径: {note_file}")
                    
        except Exception as e:
            logger.error(f"更新文件 {note_file} 时出错: {e}")
    
    def create_backup(self):
        """创建备份"""
        if self.backup and not self.dry_run:
            backup_dir = Path(f"{self.notes_dir}_backup_{int(time.time())}")
            logger.info(f"创建备份: {backup_dir}")
            shutil.copytree(self.notes_dir, backup_dir)
    
    def migrate(self):
        """执行完整的迁移过程"""
        logger.info("开始资产迁移...")
        
        if self.backup:
            self.create_backup()
        
        note_files = self.find_note_files()
        logger.info(f"找到 {len(note_files)} 个笔记文件")
        
        total_migrations = 0
        
        for note_file in note_files:
            # 跳过assets目录本身
            if "assets" in note_file.parts:
                continue
                
            migration_map = self.migrate_assets_for_note(note_file)
            if migration_map:
                self.update_note_file(note_file, migration_map)
                total_migrations += len(migration_map)
        
        logger.info(f"迁移完成! 共迁移了 {total_migrations} 个资产文件")
        
        if self.dry_run:
            logger.info("这是预览模式，没有实际执行任何操作")

def main():
    parser = argparse.ArgumentParser(description="mkdocs-note v2.0.0 资产迁移脚本")
    parser.add_argument("--dry-run", action="store_true", help="仅显示将要执行的操作，不实际执行")
    parser.add_argument("--backup", action="store_true", help="在迁移前创建备份")
    parser.add_argument("--notes-dir", default="docs/notes", help="笔记目录路径 (默认: docs/notes)")
    
    args = parser.parse_args()
    
    migrator = AssetMigrator(
        notes_dir=args.notes_dir,
        dry_run=args.dry_run,
        backup=args.backup
    )
    
    try:
        migrator.migrate()
    except Exception as e:
        logger.error(f"迁移过程中出现错误: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    import time
    exit(main())
