import os
import subprocess

# Path to your local GitHub repo
repo_path = "/path/to/your/repo"
folder_name = "docs"
file_name = "readme.md"

# Navigate to repo
os.chdir(repo_path)

# Create folder and a file inside
os.makedirs(folder_name, exist_ok=True)
with open(os.path.join(folder_name, file_name), "w") as f:
    f.write("# Docs folder\nThis is a placeholder file.")

# Stage, commit, and push changes
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", f"Add {folder_name} folder with {file_name}"])
subprocess.run(["git", "push", "origin", "main"])
