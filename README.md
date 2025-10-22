# SortMe – Automatic Project Folder Organizer & Import Updater

SortMe is a Python-based tool that intelligently organizes project folders and updates include/import statements for multiple programming languages. It makes your project structure logical, easy to navigate, and keeps dependencies correct after reorganizing files.

## Features

- **Automatic folder organization**  
  Sorts files into a nested, logical folder structure based on their names and purpose.

- **Import & include updater**  
  Updates include/import statements across files to match the new folder structure. Supports multiple languages:
  - Python (`import`, `from ... import`)
  - C / C++ (`#include`)
  - Java (`import`)
  - JavaScript / TypeScript (`import`, `require`)
  - Rust (`use`, `mod`)
  - Go (`import`)
  - PHP (`include`, `require`, `use`)
  - C# (`using`)
  - Shell (`source`)
  - Markdown (`{{ include }}`)
  - SQL (`source`, `\i`)

- **Cross-language support**  
  Works on projects containing multiple programming languages.

- **Terminal-ready command**  
  Can be installed once and run from anywhere in the terminal.

- **Automatic first-time setup**  
  Moves scripts to `~/.sortMe/src`, sets environment variables, and installs Python dependencies.

## Installation

```bash
# Clone the repository
git clone https://github.com/chirag-diwan/SortMe.git
cd SortMe

# Make installer executable
chmod +x script.sh

# Run installer (moves scripts, sets environment, installs Python dependencies)
./script.sh

```
## Using SortMe

```bash
sortme.py arg1 arg2
```
The command takes in two argument .The first argument is a COMPULSORY argument that takes the OPENAI Api Key and the second argument is a OPTIONAL remote directory that you may want to sort 

## Contribution

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/chirag-diwan/SortMe.git
cd SortMe

# Create a new feature branch
git checkout -b feature-name

# Make changes and commit
git add .
git commit -m "Add feature"

# Push your branch to GitHub
git push origin feature-name
```
