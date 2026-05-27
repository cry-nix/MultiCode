#!/bin/bash
set -e

echo "Installing MultiCode..."

INSTALL_DIR="$HOME/.local/share/multicode"
BIN_DIR="$HOME/.local/bin"
WRAPPER="$BIN_DIR/multicode"

if [ -d "$INSTALL_DIR" ]; then
    echo "Backing up statuses.txt..."
    mkdir -p "$HOME/multicode"
    if [ -f "$INSTALL_DIR/statuses.txt" ]; then
        cp "$INSTALL_DIR/statuses.txt" "$HOME/multicode/statuses.txt"
        echo "Copied statuses.txt to ~/multicode"
    else
        echo "Warning: statuses.txt not found in install dir, skipping backup."
    fi

    echo "Removing existing installation..."
    rm -rf "$INSTALL_DIR"
fi

echo "Cloning repository..."
git clone https://github.com/cry-nix/MultiCode.git "$INSTALL_DIR"

cd "$INSTALL_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

pip install -e .

mkdir -p "$BIN_DIR"
cat > "$WRAPPER" << 'EOF'
#!/bin/bash
exec "$HOME/.local/share/multicode/venv/bin/multicode" "$@"
EOF
chmod +x "$WRAPPER"

if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
    echo "Added $HOME/.local/bin to PATH. Please restart your terminal or run: source ~/.bashrc"
fi

echo "MultiCode installed! Run 'multicode' from anywhere."