#!/bin/bash
set -e

CHROMA_DIR="./volumes/chroma_data"
DOWNLOAD_URL="https://www.kaggle.com/code/svzip/317718978"


# ── Ensure volume directories exist ──
mkdir -p "./volumes"

# ── Codespaces: use larger storage via symlinks ──
if [[ "$(pwd)" == "/workspaces/romi" ]]; then
    rm -rf "$CHROMA_DIR"
    [[ -d "./volumes/ollama_data" && ! -L "./volumes/ollama_data" ]] && rm -rf "./volumes/ollama_data"

    [[ -d "$CHROMA_DIR" ]] || mkdir -p "$CHROMA_DIR"
    [[ -d "/tmp/ollama_data" ]] || mkdir -p "/tmp/ollama_data"

    # [[ -L "$CHROMA_DIR" ]] || ln -s "/vscode/chroma_data" "$CHROMA_DIR"
    [[ -L "./volumes/ollama_data" ]] || ln -s "/tmp/ollama_data" "./volumes/ollama_data"
else
    mkdir -p "$CHROMA_DIR"
    mkdir -p "./volumes/ollama_data"
fi

# ── Download vector DB if not present ──
if [ -d "$CHROMA_DIR/my_vector_db" ]; then
    echo "✅ Vector database already exists at $CHROMA_DIR/my_vector_db"
else
    echo "⬇️  Vector database not found. Downloading..."

    wget -qO "$CHROMA_DIR/db.zip" "$DOWNLOAD_URL"
    unzip -q "$CHROMA_DIR/db.zip" -d "$CHROMA_DIR/extracted"
    mv "$CHROMA_DIR/extracted/"* "$CHROMA_DIR/" 2>/dev/null || true
    rm -rf "$CHROMA_DIR/db.zip" "$CHROMA_DIR/extracted"

    echo "✅ Vector database downloaded to $CHROMA_DIR"
fi

echo ""
echo "Ready! Run 'docker compose up' to start the services."
