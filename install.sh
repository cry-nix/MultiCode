#!/bin/bash
set -e

echo "Installing MultiCode..."

INSTALL_DIR="$HOME/.local/share/multicode"
BIN_DIR="$HOME/.local/bin"
WRAPPER="$BIN_DIR/multicode"

if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "Cloning repository..."
    git clone https://github.com/cry-nix/MultiCode.git "$INSTALL_DIR"
fi

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
