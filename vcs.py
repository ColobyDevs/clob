import os
import shutil
import datetime
import json
import sys

class SimpleVCS:
    def __init__(self, project_path):
        self.project_path = project_path
        self.vcs_path = os.path.join(project_path, ".simplevcs")
        self.history_file = os.path.join(self.vcs_path, ".history.json")

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

def make_hidden(file_path):
    # Set the hidden attribute for the file or directory
    os.system(f"attrib +h {file_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        project_path = os.getcwd()
        vcs = SimpleVCS(project_path)

        if command == "initialize":
            print("Initializing SimpleVCS...")

            # Make the directories and files hidden on Windows
            make_hidden(vcs.vcs_path)
            make_hidden(vcs.history_file)

        elif command == "commit":
            commit_message = input("Enter commit message: ")
            branch_name = input("Enter branch name (press Enter for 'main'): ")
            vcs.commit(commit_message, branch=branch_name or "main")

        elif command == "show_history":
            vcs.show_history()

        elif command == "checkout":
            commit_path = input("Enter commit path (e.g., 'main/2023-01-01_12-34-56'): ")
            vcs.checkout(commit_path)

        else:
            print(f"Unknown command: {command}")

    else:
        print("Usage: python vcs.py <command>")
