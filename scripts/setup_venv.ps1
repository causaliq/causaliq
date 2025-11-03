# Create Python 3.11 venv in venv/py311 folder
py -3.11 -m venv venv/py311

# Activate the venv
. ./venv/py311/Scripts/Activate.ps1

# Upgrade pip, wheel, and setuptools
python -m pip install --upgrade pip wheel setuptools

# Install requirements if requirements.txt exists
if (Test-Path requirements.txt) {
    pip install -r requirements.txt
}

Write-Host "Virtual environment setup complete."