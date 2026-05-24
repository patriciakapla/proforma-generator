# Proforma Generator

Proforma Generator is a command-line tool for creating formatted proforma invoice PDFs from structured contract data.

It reads contract JSON files, calculates billable milestone values, applies CPI-based adjustment data, renders a PDF with the bundled template assets, and can update each milestone's billing status in the source contract file.

## Requirements

- Python 3.14 or later
- Windows, for the built-in `progen set` command, which uses `setx`
- Internet access when generating PDFs, because CPI data is fetched from the Argly API

## Installation

Install the project as a CLI tool from the repository root:

```powershell
uv tool install --reinstall .
```

After installation, the CLI is available as:

```powershell
progen
```

## Setup

_Configure the directory that contains your contract JSON files:_

```powershell
progen set "C:\path\to\contracts" -d contract
```

_Configure the directory where generated PDFs should be saved:_

```powershell
progen set "C:\path\to\pdf-output" -d pdf
```

Close and reopen your terminal after running these commands so Windows can load the updated environment variables.

## Usage

Contract file names are passed without the `.json` extension. For example, `contract_data` refers to `contract_data.json` in the configured contracts directory.

_Display the milestones for a contract:_

```powershell
progen mile contract_data
```

_Generate proforma PDF for selected milestones:_

```powershell
progen gen contract_data 2 3
```

_Update milestone billing status:_

```powershell
progen update contract_data 2 3
```

When prompted, enter:

- `b` to mark the selected milestones as billed
- `n` to mark the selected milestones as not billed
- `q` to quit without updating
