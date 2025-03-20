# NIST_potentials

In this repo we collected potentials from [NIST potential repository](https://www.ctcms.nist.gov/potentials/) using script `download_potentials.py`, and sorted based on the used model using script `select_model.py`.

Last update of source potentials: 2025-03-20.

## Script Descriptions

### 1. `download_potentials.py`

#### Description
This script automates the download of interatomic potentials from the NIST CTCMS website. It parses the available potentials, organizes them into appropriate subdirectories, and downloads only the missing files.

#### Features
- Downloads the main HTML page containing potential file links.
- Recursively creates necessary subdirectories for file organization.
- Skips downloading files that already exist.
- Maintains a timestamp file (`_last_download.timestamp`) to track the last download session.

#### Usage
Run the script with:
```sh
python download_potentials.py
```

#### Prerequisites
Ensure that `lxml` and `requests` libraries are installed before running:
```sh
pip install lxml requests
```

---

### 2. `select_model.py`

#### Description
This script organizes and selects interatomic potential files based on the model type. It scans through available potential files, structures them into a hierarchical directory format, and saves metadata in a YAML file (to be primarily used with the [wmaee](https://github.com/MUL-CMS/wmaee) module). Modily the line `model = "eam.alloy"` in the script for other models (tested with `eam.alloy` and `eam.fs`).

#### Features
- Scans for directories matching the format `year--<whatever>`.
- Identifies and extracts potential files related to `eam.alloy` and `eam.fs`.
- Organizes potential files into structured subdirectories.
- Copies necessary files to a central directory for easier access.
- Saves metadata about the potentials in a `potentials.yaml` file.

#### Usage
Run the script with:
```sh
python select_model.py
```

#### Prerequisites
Ensure that `pyyaml` is installed before running:
```sh
pip install pyyaml
```
