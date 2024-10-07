# Makefile for Python project management

# Variables
VENV_NAME := .venv
PYTHON := python
PIP := $(VENV_NAME)/bin/pip
PYTHON_VENV := $(VENV_NAME)/bin/python
BLACK := $(VENV_NAME)/bin/black
FLAKE8 := $(VENV_NAME)/bin/flake8
JUPYTER := $(VENV_NAME)/bin/jupyter
KERNEL_NAME := my_project_kernel

# Check if any Python files exist
PYTHON_FILES := $(shell find . -name "*.py")

# Default target
all: venv install format

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_NAME)
	@$(PIP) install --upgrade pip
	@echo "Virtual environment created successfully in $(VENV_NAME)."

# Install dependencies and development tools
install: venv
	@echo "Installing dependencies and development tools..."
	@$(PIP) install --no-cache-dir -r requirements.txt
	@$(PIP) install black jupyter jupyterlab notebook ipykernel pandas numpy matplotlib seaborn scikit-learn
	@echo "Dependencies and tools installed successfully."

# Format code using Black if Python files exist
format-scripts:
	$(BLACK) ./*.py

# Format Jupyter notebooks using Black
format-notebooks:
	$(BLACK) ./*.ipynb

format: format-scripts format-notebooks
	
lint:
	$(FLAKE8) ./*.py
	
# Install Jupyter kernel
install-kernel: install
	@echo "Installing Jupyter kernel..."
	@$(PYTHON_VENV) -m ipykernel install --user --name=$(KERNEL_NAME)
	@echo "Jupyter kernel '$(KERNEL_NAME)' installed."

# Delete Jupyter kernel
delete-kernel:
	@echo "Deleting Jupyter kernel '$(KERNEL_NAME)'..."
	@-jupyter kernelspec uninstall $(KERNEL_NAME) -f
	@echo "Jupyter kernel deleted."

# Clean virtual environment
clean:
	@echo "Cleaning virtual environment..."
	@rm -rf $(VENV_NAME)
	@echo "Virtual environment removed."

check: lint format
	@echo "Checking Python scripts..."

# Phony targets
.PHONY: all venv install format install-kernel delete-kernel clean
