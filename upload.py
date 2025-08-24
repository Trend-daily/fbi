import os
import subprocess
from datetime import datetime

USERNAME = "Trend-daily"
REPO = "fbi"
BRANCH = "main"
UPLOADS_DIR = "uploads"
SOURCE_DIR = "to_upload"
OUTPUT_FILE = "uploaded_links.txt"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.stdout.strip()

def ensure_dirs():
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)

def batch_upload():
    ensure_dirs()
    files = os.listdir(SOURCE_DIR)
    if not files:
        print("No files to upload. Place images in 'to_upload/' and re-run.")
        return

    uploaded_links = []
    for filename in files:
        src_path = os.path.join(SOURCE_DIR, filename)
        dest_path = os.path.join(UPLOADS_DIR, filename)
        os.rename(src_path, dest_path)
        cdn_link = f"https://cdn.jsdelivr.net/gh/{USERNAME}/{REPO}@{BRANCH}/{UPLOADS_DIR}/{filename}"
        uploaded_links.append(cdn_link)
        print(f"Prepared: {cdn_link}")

    run_cmd("git add .")
    commit_msg = f"Batch upload on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    run_cmd(f'git commit -m "{commit_msg}"')
    run_cmd(f"git push origin {BRANCH}")

    with open(OUTPUT_FILE, "a") as f:
        for link in uploaded_links:
            f.write(link + "\n")

    print(f"\n✅ Uploaded {len(uploaded_links)} files.")
    print(f"Links saved in {OUTPUT_FILE}")

if __name__ == "__main__":
    batch_upload()