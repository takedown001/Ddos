mkdir -p .devcontainer
cat <<EOL > .devcontainer/devcontainer.json
{
    "name": "My Codespace",
    "customizations": {
        "vscode": {
            "settings": {
            },
            "extensions": [
        
            ]
        }
    },
    "onCreateCommand": "pip install flask requests",
    "postCreateCommand": "python3 child.py"
}
EOL

git add .devcontainer/devcontainer.json
git commit -m "Add postStartCommand to run Python script automatically"
git push origin main