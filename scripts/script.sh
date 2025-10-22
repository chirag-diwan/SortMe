#!/usr/bin/env bash

# --- Variables ---
INSTALL_DIR="$HOME/.sortMe/src"
SCRIPT_NAME=$(basename "$0")
ENV_FILE="$HOME/.bashrc"   # adjust for zsh -> ~/.zshrc

# --- First-time setup check ---
if [ ! -d "$INSTALL_DIR" ]; then
    echo "[INFO] First-time setup..."

    # Create target directory
    mkdir -p "$INSTALL_DIR"

    # Move this script and all Python scripts in the current dir to INSTALL_DIR
    mv "$SCRIPT_NAME" "$INSTALL_DIR/"
    mv *.py "$INSTALL_DIR/" 2>/dev/null

    echo "[INFO] Moved scripts to $INSTALL_DIR"

    # Add INSTALL_DIR to PATH if not already
    if ! grep -q "$INSTALL_DIR" "$ENV_FILE"; then
        echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$ENV_FILE"
        echo "[INFO] Added $INSTALL_DIR to PATH in $ENV_FILE"
    fi

    # Set environment variable for the project (example)
    if ! grep -q "SORTME_HOME" "$ENV_FILE"; then
        echo "export SORTME_HOME=\"$INSTALL_DIR\"" >> "$ENV_FILE"
        echo "[INFO] Set SORTME_HOME environment variable in $ENV_FILE"
    fi

    # Source ENV_FILE so changes take effect immediately
    source "$ENV_FILE"

    # --- Install Python dependencies ---
    if command -v python3 &>/dev/null; then
        echo "[INFO] Installing Python dependencies..."
        python3 -m pip install --upgrade pip
        python3 -m pip install openai
    else
        echo "[ERROR] Python3 is not installed. Please install Python3 first."
    fi

    echo "[INFO] Setup complete! You can now run your scripts from anywhere."
    exit 0
fi

# --- Normal execution (after first-time setup) ---
echo "[INFO] Running $SCRIPT_NAME..."

python3 "$INSTALL_DIR/main.py" "$@"
