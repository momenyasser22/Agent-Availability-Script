# Agent Availability System

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

A production-ready Python application that calculates and reports agent availability per Domain and Operating System using CSV inputs and SQLite database.

## Features

- **Interactive Terminal Interface** - Easy-to-use menu-driven application
- **Persistent Database Storage** - Baseline data persists across sessions in `data/` directory
- **SQLite Database** - Stores baseline agent data for Windows and Linux agents
- **Smart Availability Calculation** - Determines agent availability based on three rules:
  1. Agent exists in the baseline database
  2. Agent exists in the availability CSV
  3. Available Date is within the last 24 hours
- **Dual Report Generation** - Creates both XLSX and DOCX reports in `reports/` directory
- **Excel Report** - Windows and Linux sheets with RED highlighting for unavailable hosts
- **Word Report** - Formal document with tables and color-coded percentages
- **Flexible Date Parsing** - Supports multiple date formats including:
  - `2026-01-31 12:38:00`
  - `Jan 31, 2026 @ 12:38:00.504`
  - And many more...
- **Case-Insensitive Headers** - Robust CSV parsing with case-insensitive column matching
- **Docker Support** - Containerized deployment with Docker and Docker Compose
- **Comprehensive Error Handling** - Clear validation messages for all edge cases
- **Database Info View** - View current database status anytime with option [4]

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [CSV File Formats](#csv-file-formats)
- [Report Formats](#report-formats)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Option 1: Local Installation

```bash
# Clone the repository
git clone https://github.com/momenyasser22/agent-availability-system.git
cd agent-availability-system

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/momenyasser22/agent-availability-system.git
cd agent-availability-system

# Build and run with Docker Compose
docker-compose run --rm agent-availability
```

## Quick Start

### Running Locally

```bash
python agent_availability.py
```

### Running with Docker

```bash
# Using Make
make up

# Or using docker-compose
docker-compose run --rm agent-availability
```

### Interactive Menu

```
============================================================
                AGENT AVAILABILITY SYSTEM
============================================================

Main Menu:
    [1] Load Windows Baseline
    [2] Load Linux Baseline
    [3] Check Availability & Generate Report
    [4] View Database Info
    [5] Exit
------------------------------------------------------------
```

## Docker Deployment

### Docker Commands

```bash
# Build the Docker image
make build

# Run the application
make up

# Stop containers
make down

# View logs
make logs

# Open a shell in the container
make shell

# View database info
make info

# Clean generated files
make clean

# Clean database only
make clean-data

# Clean reports only
make clean-reports

# Full cleanup including Docker images
make clean-all
```

### File Paths in Docker

| Location | Path in Container |
|----------|-------------------|
| **Sample files** (built into image) | `/app/sample_data/windows_baseline.csv` |
| **Your local files** (via mount) | `/app/workspace/your_file.csv` |
| **Database** (persistent) | `/app/.data/agent_baseline.db` |
| **Reports** (persistent) | `/app/reports/` |

### Using CSV Files with Docker

**Option 1: Use sample files (built into image)**
```
Load Windows Baseline → Enter: /app/sample_data/windows_baseline.csv
```

**Option 2: Use your own files**
```bash
# Place CSV files in current directory
cp /path/to/your.csv .

# In Docker, use:
/app/workspace/your.csv
```

## CSV File Formats

### Baseline CSV Files (Windows/Linux)

Used to populate the baseline database with all expected agents.

**Columns:** `Domain`, `Agent Name`

**Example:**
```csv
Domain,Agent Name
Domain1,WIN-HOST01
Domain1,WIN-HOST02
Domain2,WIN-HOST03
```

### Availability CSV Files (Windows/Linux)

Contains current availability data for agents.

**Columns:** `Domain`, `Agent Name`, `Last Available Date`

**Supported Date Formats:**
- `2026-01-31 12:38:00`
- `Jan 31, 2026 @ 12:38:00.504`
- `31-01-2026 12:38:00`
- `01/31/2026 12:38:00`

**Example:**
```csv
Domain,Agent Name,Last Available Date
Domain1,WIN-HOST01,Jan 31, 2026 @ 12:38:00.504
Domain1,WIN-HOST02,Jan 30, 2026 @ 10:00:00
```

## Report Formats

### XLSX Report

One Excel file with:
- **Windows Sheet** - All Windows agents
- **Linux Sheet** - All Linux agents

**Columns:**
| OS | Domain | Agent Name | Status | Last Available Date |

**Features:**
- Blue header row
- Rows with "Not Available" status are highlighted **RED**
- Auto-adjusted column widths

### DOCX Report

For EACH Operating System and Domain combination:

```
Windows - Domain1
Unavailable Hosts:
┌─────────────────┬──────────────────────┐
│ Agent Name      │ Last Available Date  │
├─────────────────┼──────────────────────┤
│ WIN-HOST02      │ 2026-01-30 10:00:00  │
│ WIN-HOST03      │ N/A                  │
└─────────────────┴──────────────────────┘

Availability: 33.3%
```

**Features:**
- Title and timestamp centered at top
- Section headers for each OS-Domain combination
- Formatted table of unavailable hosts
- Color-coded availability percentage (green >=75%, red <75%)

## Usage Examples

### Complete Workflow

```bash
# Step 1: Start the application
python agent_availability.py

# Step 2: View initial database info
# (shown automatically on startup)

# Step 3: Load Windows Baseline
# Select [1], then enter: sample_data/windows_baseline.csv

# Step 4: Load Linux Baseline
# Select [2], then enter: sample_data/linux_baseline.csv

# Step 5: View database info (optional)
# Select [4] to see current database status

# Step 6: Check Availability
# Select [3], enter your availability CSVs
# Reports will be generated in reports/ directory
```

### Sample Data

The `sample_data/` directory contains example CSV files for testing:

- `windows_baseline.csv` - 6 Windows agents across 3 domains
- `linux_baseline.csv` - 5 Linux agents across 2 domains
- `windows_availability.csv` - Mixed availability scenarios
- `linux_availability.csv` - Mixed availability scenarios

## Project Structure

```
agent-availability-system/
├── agent_availability.py       # Main application script
├── test_agent_availability.py  # Unit tests
├── requirements.txt              # Python dependencies
├── Dockerfile                     # Docker image definition
├── docker-compose.yml             # Docker Compose configuration
├── Makefile                       # Convenient commands
├── .dockerignore                  # Docker build exclusions
├── .gitignore                     # Git exclusions
├── LICENSE                        # MIT License
├── README.md                      # This file
├── sample_data/                   # Sample CSV files
│   ├── windows_baseline.csv
│   ├── linux_baseline.csv
│   ├── windows_availability.csv
│   └── linux_availability.csv
├── data/                          # Persistent database (gitignored)
│   └── agent_baseline.db
└── reports/                       # Generated reports (gitignored)
    ├── report.xlsx
    └── report.docx
```

## Availability Rules

An agent is considered **AVAILABLE** only if ALL of the following conditions are met:

1. **Exists in baseline database** - The agent was loaded via Options 1 or 2
2. **Exists in availability CSV** - The agent appears in the availability CSV
3. **Date within last 24 hours** - The `Last Available Date` is within 24 hours of execution time

If ANY condition fails, the agent is **NOT AVAILABLE**.

## Persistent Storage

### Database
- **Location:** `data/agent_baseline.db`
- **Persists across** script runs and Docker container restarts
- **Cleared when:** You load new baseline data (options 1 or 2)

### Reports
- **Location:** `reports/` directory
- **All reports saved:** Both XLSX and DOCX formats
- **Naming:** `[filename].xlsx` and `[filename].docx`

### Database Info Display

When you start the script, you see:
```
==================================================
PERSISTENT DATABASE INFO
==================================================
Location: /path/to/data/agent_baseline.db
Size: 20.00 KB
Last Modified: 2026-01-31 14:07:40
Windows Agents: 6
Linux Agents: 5
==================================================
```

Use option **[4]** anytime to view current database status.

## Error Handling

The script provides clear error messages for:
- Invalid CSV headers (case-insensitive matching)
- Missing columns
- Empty CSV files
- Invalid date formats (with supported formats listed)
- Missing files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Running Tests

```bash
python test_agent_availability.py
```

## Test Cases

The test suite includes 11 test cases covering:
1. 100% availability
2. Missing agents
3. Availability older than 24 hours
4. Multiple domains and operating systems
5. Invalid CSV headers
6. Empty availability CSV
7. Database overwrite validation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python 3.7+
- Uses [openpyxl](https://openpyxl.readthedocs.io/) for Excel generation
- Uses [python-docx](https://python-docx.readthedocs.io/) for Word document generation
- Containerized with Docker

---

**Made with ❤️ for monitoring agent availability**
