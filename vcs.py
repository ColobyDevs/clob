import os
import shutil
import datetime
import json
import sys

class SimpleVCS:
    def __init__(self, project_path):
        self.project_path = project_path
        self.vcs_path = os.path.join(project_path, ".simplevcs")
        self.history_file = os.path.join(self.vcs_path, "history.json")

        # Initialize VCS directory and history file
        if not os.path.exists(self.vcs_path):
            os.makedirs(self.vcs_path)
            self._initialize_history()

    def _initialize_history(self):
        # Initialize history with a main branch
        history = [{"timestamp": str(datetime.datetime.now()), "branch": "main", "changes": "Initial commit"}]
        with open(self.history_file, "w") as file:
            json.dump(history, file)

    def commit(self, commit_message, branch="main"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        history_entry = {"timestamp": timestamp, "branch": branch, "changes": commit_message}

        # Save changes to history
        with open(self.history_file, "r") as file:
            history = json.load(file)
            history.append(history_entry)

        with open(self.history_file, "w") as file:
            json.dump(history, file)

        # Create a copy of the project in the VCS directory
        commit_folder = os.path.join(self.vcs_path, branch, timestamp)
        shutil.copytree(self.project_path, commit_folder)

    def merge(self, target_branch):
        current_branch = self.get_current_branch()
        source_branch = current_branch

        source_path = os.path.join(self.vcs_path, source_branch)
        target_path = os.path.join(self.vcs_path, target_branch)

        if not os.path.exists(source_path):
            print(f"Source branch '{source_branch}' not found.")
            return

        if not os.path.exists(target_path):
            print(f"Target branch '{target_branch}' not found.")
            return

        # Perform the merge by copying changes from the source to the target
        for root, dirs, files in os.walk(source_path):
            relative_path = os.path.relpath(root, source_path)
            target_root = os.path.join(target_path, relative_path)

            for file in files:
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_root, file)

                if not os.path.exists(target_file_path):
                    shutil.copy2(source_file_path, target_file_path)
                    print(f"Added {file} to {target_branch}")
                else:
                    print(f"Skipping {file} (conflict)")

    def show_history(self):
        with open(self.history_file, "r") as file:
            history = json.load(file)

        for entry in history:
            print(f"{entry['timestamp']} ({entry['branch']}): {entry['changes']}")

    def checkout(self, commit_path):
        commit_folder = os.path.join(self.vcs_path, commit_path)
        if os.path.exists(commit_folder):
            shutil.rmtree(self.project_path)
            shutil.copytree(commit_folder, self.project_path)
            print(f"Checked out to {commit_path}")
        else:
            print(f"Commit {commit_path} not found")

    def get_current_branch(self):
        # Assuming the current branch is the one with the latest commit
        with open(self.history_file, "r") as file:
            history = json.load(file)
            return history[-1]["branch"]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        project_path = os.getcwd()
        vcs = SimpleVCS(project_path)

        if command == "initialize":
            print("Initializing SimpleVCS...")

        elif command == "commit":
            commit_message = input("Enter commit message: ")
            branch_name = input("Enter branch name (press Enter for 'main'): ")
            vcs.commit(commit_message, branch=branch_name or "main")

        elif command == 'merge':
            target_branch = input("Enter target branch name: ")
            vcs.merge(target_branch)

        elif command == "show_history":
            vcs.show_history()

        elif command == "checkout":
            commit_path = input("Enter commit path (e.g., 'main/2023-01-01_12-34-56'): ")
            vcs.checkout(commit_path)

        elif command == "branch":
            current_branch = vcs.get_current_branch()
            print(f"Current branch: {current_branch}")

        else:
            print(f"Unknown command: {command}")

    else:
        print("Usage: python vcs.py <command>")
