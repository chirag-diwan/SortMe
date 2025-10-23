#!/usr/bin/env bash

INSTALL_DIR="$HOME/.sortMe/src"
SCRIPT_NAME=$(basename "$0")
ENV_FILE="$HOME/.zshrc" 
ZSHDIR="$HOME/.zshrc"
BASHDIR="$HOME/.bashrc"

if [ -d "$ZSHDIR" ]; then
    echo "ZSH deteced"
    ENV_FILE=ZSHDIR
else if [ -d "$BASHDIR" ]; then
    echo "BASH deteced"
    ENV_FILE=BASHDIR
fi


if [ ! -d "$INSTALL_DIR" ]; then
    echo "[INFO] First-time setup..."

    mkdir -p "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR/src"

    echo "[INFO] Made $INSTALL_DIR"

    mv "$SCRIPT_NAME" "$INSTALL_DIR/src"
    mv ../src "$INSTALL_DIR/" 2>/dev/null
    mv ../data "$INSTALL_DIR/" 2>/dev/null

    
    echo "[INFO] Moved scripts to $INSTALL_DIR"

    if ! grep -q "$INSTALL_DIR" "$ENV_FILE"; then
        echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$ENV_FILE"
        echo "[INFO] Added $INSTALL_DIR to PATH in $ENV_FILE"
    fi

    if ! grep -q "SORTME_HOME" "$ENV_FILE"; then
        echo "export SORTME_HOME=\"$INSTALL_DIR\"" >> "$ENV_FILE"
        echo "[INFO] Set SORTME_HOME environment variable in $ENV_FILE"
    fi

    if command -v python3 &>/dev/null; then
        echo "[INFO] Installing Python dependencies..."
        python3 -m pip install --upgrade pip
        python3 -m pip install openai
    else
        echo "[ERROR] Python3 is not installed. Please install Python3 first."
    fi

    echo "[INFO] Setup complete! Please Restart Your Terminal Or run 'source ~/.$ENV_FILE'."
    exit 0
fi

python3 "$INSTALL_DIR/sortme.py" "$@"
