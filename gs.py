"""
gs.py

Generates a snapshot of your project by iterating over your manually created files
and writing their filenames and content to a file called gs.txt.

Only files with specific extensions (like .py, .txt, .md) or specific names (e.g. requirements.txt)
are included. Directories known to be auto-generated (such as __pycache__, .git, venv, etc.)
are skipped.

Usage: Run this file in your project root with "python gs.py"
"""

import os

# Directories to ignore (commonly auto-generated or not manually created)
IGNORE_DIRS = {"__pycache__", ".git", "venv", "env", "node_modules", "build", "dist"}

# Allowed file extensions and specific allowed filenames
ALLOWED_EXTENSIONS = {'.py', '.txt', '.md'}
ALLOWED_FILES = {"requirements.txt", "README"}  # 'README' with no extension

# Output file name (this file itself will be skipped)
OUTPUT_FILENAME = "gs.txt"

def is_allowed_file(filename):
    # Check if filename exactly matches an allowed file (e.g. requirements.txt)
    if filename in ALLOWED_FILES:
        return True

    # Check extension: if it has one and is in our allowed list
    _, ext = os.path.splitext(filename)
    if ext in ALLOWED_EXTENSIONS:
        return True

    return False

def main():
    snapshot_lines = []

    # Walk through the current directory recursively
    for root, dirs, files in os.walk("."):
        # Skip ignored directories by modifying dirs in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            # Skip the output file itself to avoid recursion issues
            if file == OUTPUT_FILENAME:
                continue

            if is_allowed_file(file):
                filepath = os.path.join(root, file)
                # Add header for the file
                snapshot_lines.append("=" * 80)
                snapshot_lines.append(f"FILE: {os.path.relpath(filepath)}")
                snapshot_lines.append("=" * 80)
                snapshot_lines.append("")

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    content = f"Error reading file: {e}"

                snapshot_lines.append(content)
                snapshot_lines.append("\n" + "-" * 80 + "\n")

    # Write the snapshot to gs.txt in the current directory
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as out_file:
        out_file.write("\n".join(snapshot_lines))

    print(f"Snapshot generated and saved to {OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()