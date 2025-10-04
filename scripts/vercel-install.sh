# Install dependencies
python3.12 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# # Use uv instead
# curl -LsSf https://astral.sh/uv/install.sh | sh
# source ~/.bashrc

# # Create virtual environment and install dependencies
# uv venv
# uv lock --upgrade
# uv sync
