# KPM Trace Processor

This utility reconstructs and extracts KPM vehicle trace packages.

## Workflow

1. Discover `.7z.001`, `.7z.002`, and later chunks.
2. Verify that volume numbering is continuous.
3. Merge the chunks in numeric order.
4. Validate the merged 7z archive with 7-Zip.
5. Extract the merged archive.
6. Extract nested ZIP archives automatically.
7. Report final BLF, ASC, PCAP, PCAPNG, MF4, MDF, or ESOTRACE files.

## Setup

1. Install Python 3.10 or newer.
2. Install 7-Zip.
3. Put one archive set in the input folder.
4. Update `input_folder` in `config.py`.
5. Run:

```powershell
& "C:\Program Files\Python310\python.exe" ".\main.py"
```

Output is written to the `Processed` folder under the configured input folder.
