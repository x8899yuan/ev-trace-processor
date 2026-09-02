# EV Trace Processor

EV Trace Processor is a modular Python utility for preparing large vehicle trace packages for analysis. The current version discovers split 7-Zip volumes, merges the volumes, validates the resulting archive, extracts its contents, and locates supported trace files.

## Current Features

- Discover sequential archive volumes such as `.7z.001`, `.7z.002`, and `.7z.003`
- Merge archive volumes in the correct order
- Validate the merged archive with 7-Zip
- Extract the validated archive
- Find supported vehicle trace files in the extracted content
- Provide a clear command-line workflow and summary

## Project Structure

```text
evTraceProcessor/
├── main.py
├── archive_discovery.py
├── archive_merger.py
├── archive_validator.py
├── archive_extractor.py
├── trace_detector.py
├── config.py
├── models.py
├── utils.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- 7-Zip installed at the following default location:

```text
C:\Program Files\7-Zip\7z.exe
```

The current archive-processing modules use only the Python standard library. No third-party Python packages are required at this stage.

## Configuration

Open `main.py` and verify these paths:

```python
SEVEN_ZIP = Path(r"C:\Program Files\7-Zip\7z.exe")
INPUT_FOLDER = Path(r"C:\Temp\PnC Testing Traces\test")
OUTPUT_FOLDER = INPUT_FOLDER / "Processed"
```

Change `INPUT_FOLDER` to the folder containing the split archive volumes.

## Expected Input

All archive volumes must be in the same folder and retain their original sequential names:

```text
VehicleTrace.blf.7z.001
VehicleTrace.blf.7z.002
VehicleTrace.blf.7z.003
```

Do not rename, individually extract, or modify the archive volumes before processing.

## Run the Application

Open the project folder in Visual Studio Code, open a terminal, and run:

```powershell
python main.py
```

The application will:

1. Discover the archive volumes.
2. Merge the volumes.
3. Validate the merged archive.
4. Extract the archive.
5. Search for trace files.
6. Print a trace-file summary.

## Output

Generated content is stored under:

```text
Processed/
├── merged archive
└── Extracted/
```

The `Processed` and `Extracted` folders are excluded from Git because they can contain large generated or vehicle-specific files.

## Data and Security

Do not commit vehicle traces, internal project data, credentials, access tokens, private certificates, or confidential configuration. The included `.gitignore` excludes common trace and archive formats, but always review staged files using:

```powershell
git status
git diff --cached
```

## Planned Enhancements

- BLF and ASC trace readers
- PCAP and PCAPNG processing
- DBC-based CAN message decoding
- VW and Audi signal mapping
- Charging-session detection
- Plug & Charge and ISO 15118 event analysis
- CSV, JSON, and Excel reporting
- Automated tests and logging

## Status

The archive discovery, merge, validation, extraction, and trace detection workflow is operational.
