#!/usr/bin/env python3

import subprocess
import sys
import os
import logging
import colorlog
from pathlib import Path

# init color log
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

def main():
    try:
        ##
        # Pre-hooks
        ##
        # Update recent notes at index
        logger.info("Refresh recent notes at index page...")
        result = subprocess.run(["uv", "run", "src/recent_notes.py"], check=True)
        logger.info("Refresh successfully!")

        hexo_path = Path('../blog/source/_posts')
        wiki_path = Path('docs/blog/posts')
        logger.info("Sync blog posts to hexo blog")
        for file in wiki_path.glob('*.md'):
            wiki_post = file.name
            check = hexo_path / wiki_post

            # Check whether the post file is exist in hexo blog or not
            if check.is_file():
                subprocess.run(f"cp {file} {str(hexo_path)}", shell=True, check=True)
            else :
                subprocess.run(f"cp {file} {str(hexo_path)}", shell=True, check=True)
        subprocess.run("cd ../blog && uv run build.py", shell=True, check=True)
        logger.info("Sync successfully!")
        
        ##
        # Sync
        ##
        # Get commit path & message
        path = input("Commit path: ").strip()
        if not path:
            raise ValueError("Choose at least a file to commit!")
            
        message = input("Commit message: ").strip()
        if not message:
            raise ValueError("Can't commit without message!")
            
        # Git operations
        logger.info(f"Add path: {path}")
        subprocess.run(["git", "add", f"{path}"], check=True)
        
        logger.info(f"Commit message: \"{message}\"")
        subprocess.run(["git", "commit", "-m", f"{message}"], check=True)
        
        logger.info("Push to origin/main...")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        logger.info("Complete!")
        
    except KeyboardInterrupt:
        user = os.getlogin()
        logger.warning(f"Interrupted by {user}")
        return 1
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Process failed with {e.returncode}: {e.cmd}")
        if e.stdout:
            logger.info(f"OUT: {e.stdout}")
        if e.stderr:
            logger.error(f"ERROR: {e.stderr}")
        if "git push" in str(e.cmd):
            logger.info("Git push error!")
        elif "git add" in str(e.cmd):
            logger.info("Git add error!")
        return 2
        
    except ValueError as e:
        logger.error(f"Input error: {str(e)}")
        return 3
        
    except Exception as e:
        logger.exception(f"Other errors: {str(e)}")
        return 4
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
