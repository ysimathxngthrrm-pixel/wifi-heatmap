import os
import subprocess
import sys

def run_command(command, cwd=None):
    """Runs a shell command and returns output, raising an exception on failure."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(command)}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, command, result.stdout, result.stderr)
    return result.stdout.strip()

def upload_to_git():
    repo_dir = "/Users/asinay/Desktop/pro"
    remote_url = "https://github.com/ysimathxngthrrm-pixel/wifi-heatmap.git"
    
    if not os.path.exists(repo_dir):
        print(f"Error: Directory {repo_dir} does not exist.")
        sys.exit(1)
        
    print(f"Initializing/checking git repository at {repo_dir}...")
    
    # Check if git is initialized
    git_dir = os.path.join(repo_dir, ".git")
    if not os.path.exists(git_dir):
        run_command(["git", "init"], cwd=repo_dir)
        print("Initialized empty Git repository.")
    
    # Configure remote origin
    try:
        existing_remotes = run_command(["git", "remote"], cwd=repo_dir)
        if "origin" in existing_remotes.split():
            print("Updating existing remote origin...")
            run_command(["git", "remote", "set-url", "origin", remote_url], cwd=repo_dir)
        else:
            print("Adding remote origin...")
            run_command(["git", "remote", "add", "origin", remote_url], cwd=repo_dir)
    except Exception as e:
        print(f"Failed to configure remote: {e}")
        sys.exit(1)
        
    # Stage all files
    print("Staging all files...")
    run_command(["git", "add", "."], cwd=repo_dir)
    
    # Check status to see if there are changes to commit
    status = run_command(["git", "status", "--porcelain"], cwd=repo_dir)
    if not status:
        print("No changes to commit.")
    else:
        # Commit changes
        commit_message = "Upload files using Python script"
        print(f"Committing changes with message: '{commit_message}'...")
        run_command(["git", "commit", "-m", commit_message], cwd=repo_dir)
        
    # Rename branch to main
    print("Setting branch to main...")
    run_command(["git", "branch", "-M", "main"], cwd=repo_dir)
    
    # Push to remote
    print("Pushing to GitHub (main branch)...")
    try:
        push_output = run_command(["git", "push", "-f", "-u", "origin", "main"], cwd=repo_dir)
        print("Upload successful!")
        print(push_output)
    except Exception as e:
        print("\nFailed to push to GitHub.")
        print("Please make sure:")
        print("1. You have internet connection.")
        print("2. You have permission to push to this repository.")
        print("3. Git credentials (SSH key or Personal Access Token) are set up correctly.")
        print(f"Error details: {e}")

if __name__ == "__main__":
    upload_to_git()
