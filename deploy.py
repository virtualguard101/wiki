#!/usr/bin/env python3

import subprocess
import sys
import os
import logging
import colorlog
import yaml
from pathlib import Path

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
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Configuration file path
CONFIG_PATH = Path(__file__).parent / 'deploy_config.yml'

def load_config():
    """Load configuration file"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {CONFIG_PATH}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Invalid config format: {e}")
        return None

def run_hooks(hooks, hook_type):
    """Execute hooks of specified type"""
    for hook in hooks.get(hook_type, []):
        hook_path = Path(hook)
        if not hook_path.exists():
            logger.warning(f"Hook not found: {hook_path}")
            continue
        
        try:
            logger.info(f"Running hook: {hook_path}")
            result = subprocess.run([sys.executable, str(hook_path)], check=True)
            if result.returncode != 0:
                logger.error(f"Hook failed with code {result.returncode}: {hook_path}")
        except Exception as e:
            logger.error(f"Error running hook {hook_path}: {e}")

def main():
    try:

        config = load_config()
        if not config:
            return 1
        
        # Execute pre-commit hooks with user's input
        run_hooks(config['hooks'], 'pre_commit')

        while True:
            sync_choice = input("Would you want to sync posts to hexo blog? (y/N): ").strip().lower()
            if sync_choice == 'n' or sync_choice == '':
                break
            elif sync_choice == 'y':
                # Sync blog posts
                hexo_path = Path(config['paths']['hexo'])
                wiki_path = Path(config['paths']['wiki'])
                logger.info("Syncing blog posts to hexo blog")
                for file in wiki_path.glob('*.md'):
                    wiki_post = file.name
                    dest_path = hexo_path / wiki_post
                    
                    # Copy file regardless of existence in hexo blog
                    subprocess.run(f"cp {file} {str(hexo_path)}", shell=True, check=True)
                    logger.debug(f"Copied: {file} -> {dest_path}")
                
                # Build hexo blog
                subprocess.run("cd ../blog && uv run build.py", shell=True, check=True)
                logger.info("Blog build completed successfully!")
                break
            else:
                logger.error("Invalid choice")
        
        # Git operations
        commit_paths = input("Enter commit paths: ").strip()
        if not commit_paths:
            raise ValueError("Please specify at least one file to commit")
            
        commit_message = input("Enter commit message: ").strip()
        if not commit_message:
            raise ValueError("Commit message cannot be empty")
        
        # Stage files
        logger.info(f"Staging files: {commit_paths}")
        subprocess.run(["git", "add"] + commit_paths.split(), check=True)
        
        # Commit changes
        logger.info(f"Committing with message: \"{commit_message}\"")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Push changes
        logger.info("Pushing to origin/main...")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        logger.info("Process completed successfully!")
        
    except KeyboardInterrupt:
        user = os.getlogin()
        logger.warning(f"Operation interrupted by user: {user}")
        return 1
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with code {e.returncode}: {e.cmd}")
        if e.stdout:
            logger.info(f"Output: {e.stdout.decode().strip()}")
        if e.stderr:
            logger.error(f"Error: {e.stderr.decode().strip()}")
        return 2
        
    except ValueError as e:
        logger.error(f"Input error: {str(e)}")
        return 3
        
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return 4
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
