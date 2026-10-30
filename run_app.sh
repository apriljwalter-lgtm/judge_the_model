#!/usr/bin/env bash
# Start the Judge the Model Streamlit app on this computer only (publishing is separate: see SETUP.md).
#
#     bash run_app.sh        # then open http://localhost:8501 ; stop with Ctrl+C
#
# Run it in a Bash terminal (on Windows: Git Bash or WSL, not PowerShell or Command Prompt).
# It installs nothing, never runs git and never publishes anything.

set -euo pipefail

PORT=8501

# Work from this script's folder, wherever it is run from.
cd "$(dirname "${BASH_SOURCE[0]}")"

stop() {
    echo "Can't start the app: $1" >&2
    exit 1
}

# The project's Python environment (macOS/Linux/WSL, then Windows), else the active python.
if [ -x ".venv/bin/python" ]; then
    PY=".venv/bin/python"
elif [ -x ".venv/Scripts/python.exe" ]; then
    PY=".venv/Scripts/python.exe"
elif command -v python >/dev/null 2>&1; then
    PY="python"
    echo "Note: no .venv in this folder; using the active python ($(command -v python))."
elif command -v python3 >/dev/null 2>&1; then
    PY="python3"
    echo "Note: no .venv in this folder; using the active python3 ($(command -v python3))."
else
    stop "no Python found. Create the environment first: uv venv, then uv pip install -r requirements.txt."
fi

"$PY" -c 'import sys; sys.exit(sys.version_info < (3, 11))' \
    || stop "$PY is older than Python 3.11. Recreate the environment with uv and Python 3.11 or newer."
"$PY" -c 'import streamlit' 2>/dev/null \
    || stop "Streamlit is not installed for $PY. Run: uv pip install -r requirements.txt"
[ -f streamlit_app.py ] || stop "streamlit_app.py is missing from $(pwd)."
[ -d results ] || stop "the results/ folder is missing; restore it from the starter or run: python -m analysis"

echo "Starting the Streamlit app with $PY"
echo "Open http://localhost:$PORT in your browser. Stop the app with Ctrl+C."
exec "$PY" -m streamlit run streamlit_app.py --server.port "$PORT" --server.headless true
