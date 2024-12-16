# Azure Blob Existence Checker

## Overview
A Python tool to efficiently check the existence of files in Azure Blob Storage using a CSV input file.

## Prerequisites
- Python 3.7+
- Azure Storage account connection string
- CSV file with a 'FILENAME' column

## Installation

### Option 1: Install from GitHub (Recommended)
```bash
# Clone the repository
git clone https://github.com/dannotes/azure-blob-existence-checker.git

# Navigate to the project directory
cd azure-blob-existence-checker

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the package
pip install .
```

### Option 2: Direct pip install
```bash
pip install git+https://github.com/dannotes/azure-blob-existence-checker.git
```

## Usage

### Basic Usage
```bash
azure-blob-checker "YOUR_CONNECTION_STRING" "CONTAINER_NAME" "path/to/input.csv"
```

### Export Results to CSV
```bash
azure-blob-checker "YOUR_CONNECTION_STRING" "CONTAINER_NAME" "path/to/input.csv" -export csv
```

## Input CSV Format
Your input CSV must have a column named 'FILENAME' containing the blob names to check.

Example:
```csv
FILENAME,OtherColumn1,OtherColumn2
file1.txt,Data1,Value1
file2.jpg,Data2,Value2
```

## Features
- Concurrent blob existence checking
- Colorful terminal output
- Detailed summary of existing and non-existing blobs
- Optional CSV export of results
- Progress tracking

## Requirements
- azure-storage-blob
- tabulate
- colorama

## Troubleshooting
- Ensure your connection string is correct
- Verify container name matches exactly
- Check that the CSV file is properly formatted

## License
MIT License

## Contributing
Contributions are welcome! Please submit a pull request or open an issue.