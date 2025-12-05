import sys
import subprocess

def update_obsidian() -> int:
    commit_msg = input("Enter the commit message: ")
    subprocess.run("git add .", shell=True)
    subprocess.run(f"git commit -m '{commit_msg}'", shell=True)
    subprocess.run("git push origin", shell=True)
    
    return 0

if __name__ == "__main__":
    sys.exit(update_obsidian())
