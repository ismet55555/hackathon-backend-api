# hackathon-backend-api

## Setup

```bash
# Install Python 3.11 with pip and check version
python -V

# Install Tooling into Python 3.11
python -m pip install --upgrade pip setuptools wheel virtualenv pipenv

# Create the pipoenv python virtual environment
pipenv sync --dev

# Enter the virtual environment shell
pipenv shell

# Start server
# Linux/MacOS
./start-dev.sh

# Windows
uvicorn --reload --port 9500 --log-level debug app.main:app

# CTRL-c to quit
```

