import os
import subprocess
import sys
from datetime import datetime

def run_command(command, cwd=None, ignore_errors=False):
    """Runs a shell command and returns output."""
    print(f"➜ Running: {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0 and not ignore_errors:
        print(f"❌ Error running command: {' '.join(command)}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, command, result.stdout, result.stderr)
    return result.stdout.strip()

def ensure_git_config(repo_dir):
    """Ensures git user.name and user.email are set locally if not configured globally."""
    try:
        user_name = run_command(["git", "config", "user.name"], cwd=repo_dir, ignore_errors=True)
        user_email = run_command(["git", "config", "user.email"], cwd=repo_dir, ignore_errors=True)
        
        if not user_name:
            print("Configuring default git user.name...")
            run_command(["git", "config", "user.name", "Wi-Fi Heatmap Developer"], cwd=repo_dir)
        if not user_email:
            print("Configuring default git user.email...")
            run_command(["git", "config", "user.email", "developer@wifi-heatmap.local"], cwd=repo_dir)
    except Exception as e:
        print(f"Warning checking git config: {e}")

def upload_to_git():
    # Dynamically determine project directory from script location
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    remote_url = "https://github.com/ysimathxngthrrm-pixel/wifi-heatmap.git"
    
    # Custom commit message from CLI argument if provided
    if len(sys.argv) > 1:
        commit_message = " ".join(sys.argv[1:])
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Update Wi-Fi Heatmap Dashboard & Profile System ({timestamp})"
    
    print(f"🚀 Initializing/checking Git repository at: {repo_dir}")
    
    # Check if git repository is initialized
    git_dir = os.path.join(repo_dir, ".git")
    if not os.path.exists(git_dir):
        run_command(["git", "init"], cwd=repo_dir)
        print("✅ Initialized empty Git repository.")
    
    # Ensure git user config is set
    ensure_git_config(repo_dir)
    
    # Configure remote origin
    try:
        existing_remotes = run_command(["git", "remote"], cwd=repo_dir, ignore_errors=True)
        if "origin" in existing_remotes.split():
            print("🔄 Updating existing remote origin URL...")
            run_command(["git", "remote", "set-url", "origin", remote_url], cwd=repo_dir)
        else:
            print("➕ Adding remote origin...")
            run_command(["git", "remote", "add", "origin", remote_url], cwd=repo_dir)
    except Exception as e:
        print(f"❌ Failed to configure remote: {e}")
        sys.exit(1)
        
    # Stage all files
    print("📦 Staging all files...")
    run_command(["git", "add", "."], cwd=repo_dir)
    
    # Check status to see if there are changes to commit
    status = run_command(["git", "status", "--porcelain"], cwd=repo_dir, ignore_errors=True)
    if not status:
        print("ℹ️ No new changes to commit.")
    else:
        # Commit changes
        print(f"📝 Committing changes with message: '{commit_message}'...")
        run_command(["git", "commit", "-m", commit_message], cwd=repo_dir)
        
    # Rename branch to main
    print("🌿 Setting main branch...")
    run_command(["git", "branch", "-M", "main"], cwd=repo_dir, ignore_errors=True)
    
    # Push to remote
    print("⬆️ Pushing to GitHub (main branch)...")
    try:
        push_output = run_command(["git", "push", "-f", "-u", "origin", "main"], cwd=repo_dir)
        print("\n" + "="*50)
        print("🎉 SUCCESS: All project files uploaded to GitHub!")
        print(f"🔗 Repository URL: {remote_url}")
        print("="*50 + "\n")
    except Exception as e:
        print("\n❌ Failed to push to GitHub.")
        print("Troubleshooting tips:")
        print("1. Check your internet connection.")
        print("2. Verify repository access permissions for 'ysimathxngthrrm-pixel/wifi-heatmap'.")
        print("3. Ensure Git credentials (SSH key or Personal Access Token) are set up in your system.")
        print(f"Details: {e}")

if __name__ == "__main__":
    upload_to_git()
