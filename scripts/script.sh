#!/usr/bin/env bash

INSTALL_DIR="$HOME/.sortMe/src"
SCRIPT_NAME=$(basename "$0")
ENV_FILE="$HOME/.zshrc" 

if [ ! -d "$INSTALL_DIR" ]; then
    echo "[INFO] First-time setup..."

    mkdir -p "$INSTALL_DIR"

    mv "$SCRIPT_NAME" "$INSTALL_DIR/"
    mv *.py "$INSTALL_DIR/" 2>/dev/null

    echo "[INFO] Moved scripts to $INSTALL_DIR"

    if ! grep -q "$INSTALL_DIR" "$ENV_FILE"; then
        echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$ENV_FILE"
        echo "[INFO] Added $INSTALL_DIR to PATH in $ENV_FILE"
    fi

    if ! grep -q "SORTME_HOME" "$ENV_FILE"; then
        echo "export SORTME_HOME=\"$INSTALL_DIR\"" >> "$ENV_FILE"
        echo "[INFO] Set SORTME_HOME environment variable in $ENV_FILE"
    fi

    source "$ENV_FILE"

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

python3 "$INSTALL_DIR/sortme.py" "$@"
