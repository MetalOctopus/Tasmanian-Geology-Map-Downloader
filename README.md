# Tasmania Geological Maps Downloader

A Python tool to download all geological map sheets from [Mineral Resources Tasmania's Digital Geological Atlas](https://www.mrt.tas.gov.au/products/geoscience_maps).

*This was written by Claude, so don't expect any interesting comments. Making it public in case someone else wants an easy way to get the data from MRT.*

## Overview

This tool automatically downloads geological maps from Tasmania's comprehensive geoscience collection, including:
- Digital Geological Atlas (1:25,000 and 1:250,000 scales)
- Geological Atlas (1:50,000 and 1:63,360 scales)
- Statewide Maps (1:500,000 scale)
- Mount Read Volcanics
- Tasmanian Landslide Map Series
- **Radiometric data** (K, Th, U) via WMS - see [RADIOMETRIC_GUIDE.md](RADIOMETRIC_GUIDE.md)

**Total: 390 map sheets** available in multiple formats (PDF, TIF, ECW).

## Features

- ✅ Downloads all 6 map series automatically
- ✅ Organized folder structure: `map_type/scale/file_type/`
- ✅ Multiple file format support (PDF, TIF, ECW)
- ✅ Option to download latest versions only or all historical versions
- ✅ Respects server with 1-second delays between requests
- ✅ Resumes interrupted downloads (skips existing files)
- ✅ Metadata export to JSON
- ✅ Dry-run mode for testing
- ✅ **Create VRT mosaics** - Stitch all maps into seamless layers
- ✅ **Generate index vectors** - Map sheet boundaries with names for finding PDFs

## Project Structure

```
TAS_Maps/
├── download_all_maps.py        # Main download script
├── create_mosaics.sh           # Create VRT mosaics from TIFs
├── create_index_vectors.py     # Generate map sheet boundary vectors
├── show_summary.py             # Display map counts by series
├── monitor_download.sh         # Real-time download monitor
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── QUICKSTART.md              # Quick start guide
├── MOSAIC_GUIDE.md            # Guide for creating/using mosaics
├── LICENSE                     # MIT License
├── DATA_ATTRIBUTION.md        # How to cite the map data
├── CITATION.cff               # Software citation
└── utils/                      # Development utilities
    ├── find_all_layers.py     # List all WFS layers
    ├── download_maps_25k_only.py  # Legacy 1:25k downloader
    └── test_*.py              # Test scripts
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Internet connection

### Setup

1. Clone this repository:
```bash
git clone https://github.com/MetalOctopus/Tasmanian-Geology-Map-Downloader.git
cd Tasmanian-Geology-Map-Downloader
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Download all maps (PDFs only, latest versions):
```bash
python3 download_all_maps.py --latest-only --file-types pdf
```

### Download All File Types

Download PDFs, TIFs, and ECW files (latest versions):
```bash
python3 download_all_maps.py --latest-only --file-types all
```
⚠️ **Warning:** This downloads ~1,170 files (20-50 GB). TIF files are very large!

### Command-Line Options

```
--file-types {pdf,tif,ecw,all} [...]
    File types to download (default: pdf)
    Examples:
      --file-types pdf              # PDFs only
      --file-types pdf tif          # PDFs and TIFs
      --file-types all              # All formats

--latest-only
    Download only the latest version of each map
    (some maps have 3-5 historical versions)

--series {SERIES_NAME} [...]
    Download specific map series only
    Available series:
      mrtwfs:Geology25kIndex        # 1:25,000 scale (245 maps)
      mrtwfs:Geology50kIndex        # 1:50,000/1:63,360 scale (50 maps)
      mrtwfs:Geology250kIndex       # 1:250,000 scale (5 maps)
      mrtwfs:StateWideMapsIndex     # 1:500,000 scale (15 maps)
      mrtwfs:MtReadIndex            # Mount Read Volcanics (17 maps)
      mrtwfs:LandslideIndex         # Landslide maps (58 maps)
      all                           # All series (default)

--dry-run
    Scrape download links but don't download files
    Useful for testing or seeing what would be downloaded

--metadata-only
    Only fetch map metadata and save to JSON
    No link scraping or downloads

--limit N
    Limit number of maps to process per series
    Useful for testing (e.g., --limit 5)
```

### Examples

**Download only 1:25,000 scale maps (PDFs):**
```bash
python3 download_all_maps.py --series mrtwfs:Geology25kIndex --latest-only --file-types pdf
```

**Download all landslide maps (all formats):**
```bash
python3 download_all_maps.py --series mrtwfs:LandslideIndex --latest-only --file-types all
```

**Test with 3 maps per series:**
```bash
python3 download_all_maps.py --limit 3 --latest-only --file-types pdf
```

**Dry run to see what would be downloaded:**
```bash
python3 download_all_maps.py --dry-run --latest-only --file-types all
```

**Download everything (all versions, all formats):**
```bash
python3 download_all_maps.py --file-types all
```
⚠️ **Warning:** This will download a VERY large amount of data!

## Output Structure

Maps are organized in a logical folder hierarchy:

```
tas_geological_maps/
├── Digital_Geological_Atlas/
│   ├── 1-25000/
│   │   ├── pdf/
│   │   ├── tif/
│   │   └── ecw/
│   └── 1-250000/
│       ├── pdf/
│       ├── tif/
│       └── ecw/
├── Geological_Atlas/
│   └── 1-50000_and_1-63360/
│       ├── pdf/
│       ├── tif/
│       └── ecw/
├── Statewide/
│   └── 1-500000/
│       ├── pdf/
│       ├── tif/
│       └── ecw/
├── Mount_Read_Volcanics/
│   └── various/
│       ├── pdf/
│       ├── tif/
│       └── ecw/
├── Tasmanian_Landslide_Maps/
│   └── various/
│       ├── pdf/
│       ├── tif/
│       └── ecw/
└── all_maps_metadata.json
```

## Monitoring Progress

### Real-time Monitor

Run the monitoring script to see live progress:
```bash
./monitor_download.sh
```

### Manual Checks

Check number of downloaded files:
```bash
find tas_geological_maps -name "*.pdf" | wc -l
```

Check total size:
```bash
du -sh tas_geological_maps
```

View recent downloads:
```bash
ls -lt tas_geological_maps/*/*/*/ | head -20
```

## Map Series Details

| Series | Scale | Count | Description |
|--------|-------|-------|-------------|
| Digital Geological Atlas | 1:25,000 | 245 | Detailed geological maps |
| Geological Atlas | 1:50,000 & 1:63,360 | 50 | Regional geological maps |
| Digital Geological Atlas | 1:250,000 | 5 | Large-scale regional maps |
| Statewide | 1:500,000 | 15 | State-wide coverage maps |
| Mount Read Volcanics | Various | 17 | Specialized volcanic mapping |
| Tasmanian Landslide Maps | Various | 58 | Landslide hazard maps |
| **Total** | | **390** | |

## File Format Details

- **PDF** (1-20 MB): Map images, suitable for viewing and printing
- **TIF** (4-127 MB): High-resolution georeferenced rasters, GIS-ready
- **ECW** (4-10 MB): Compressed geospatial imagery, efficient for GIS

## Utilities

### View Map Summary

See counts for each series:
```bash
python3 show_summary.py
```

### List Available Layers

View all WFS layers:
```bash
python3 find_all_layers.py
```

## Estimated Download Times & Sizes

| Configuration | Files | Size | Time (est.) |
|--------------|-------|------|-------------|
| PDFs only, latest | ~390 | 2-5 GB | 10-20 min |
| All formats, latest | ~1,170 | 20-50 GB | 1-2 hours |
| All versions, all formats | ~3,000+ | 100+ GB | 4-6 hours |

*Times assume good connection and 1-second delays between requests.*

## Resuming Interrupted Downloads

The script automatically skips files that already exist, so you can safely:
1. Stop a download (Ctrl+C)
2. Re-run the same command
3. It will resume where it left off

## Creating Mosaics and Index Layers

### VRT Mosaics (Recommended!)

Stitch all TIF files into seamless virtual rasters:

```bash
./create_mosaics.sh
```

This creates VRT files in each scale directory:
- `Digital_Geological_Atlas/1-25000/mosaic_geology_1-25k.vrt`
- `Geological_Atlas/1-50000_and_1-63360/mosaic_geology_1-50k.vrt`
- And more...

**Benefits:**
- Tiny file size (few hundred KB)
- Instant creation
- Displays all maps as single layer in QGIS
- No data duplication

### Map Sheet Index Vectors

Create GeoJSON files showing map sheet boundaries:

```bash
source venv/bin/activate
python3 create_index_vectors.py
```

This creates index files with map sheet boundaries and attributes:
- Map name and number
- Publication date
- Path to corresponding PDF (for legends)

**Use in QGIS:**
1. Load the VRT mosaic as base layer
2. Load the index GeoJSON as overlay
3. Style with transparent fill and bright outline
4. Label with map names
5. Click polygons to identify which PDF to open for legends

See [MOSAIC_GUIDE.md](MOSAIC_GUIDE.md) for detailed instructions.

## Radiometric Data (Airborne Gamma-Ray)

Access airborne radiometric data showing potassium (K), thorium (Th), and uranium (U) concentrations:

**Coverage:**
- King Island
- North West Tasmania
- North East Tasmania
- Flinders Island

**Resolution:** 40m cell size

**Quick Start:**
1. Open QGIS
2. Layer → Add WMS/WMTS Layer
3. New connection:
   - Name: `MRT Radiometric`
   - URL: `https://www.mrt.tas.gov.au/erdas-iws/ogc/wms/?`
4. Add RGB composite layers (Red=K, Green=Th, Blue=U)

See [RADIOMETRIC_GUIDE.md](RADIOMETRIC_GUIDE.md) for complete instructions, including:
- How to interpret radiometric signatures
- Accessing data via Geoscience Australia
- Requesting full-resolution grids from MRT

## Metadata

All map metadata is saved to `tas_geological_maps/all_maps_metadata.json`, including:
- Map names and IDs
- Publication dates
- Number of versions
- Download links
- Map scales and series information

## License & Attribution

### Software License
This tool is released under the MIT License. See [LICENSE](LICENSE) for details.

### Data Attribution
**Data Source:** [Mineral Resources Tasmania](https://www.mrt.tas.gov.au/)

When using these maps, please cite:
> Mineral Resources Tasmania, Department of State Growth, Tasmania, Australia

For detailed attribution guidelines, see [DATA_ATTRIBUTION.md](DATA_ATTRIBUTION.md)

### Software Citation
If you use this tool in your research, please cite it using the information in [CITATION.cff](CITATION.cff)

## Troubleshooting

**Problem:** Download stops or hangs
- **Solution:** Press Ctrl+C and re-run the same command. It will skip existing files and continue.

**Problem:** "Connection timeout" errors
- **Solution:** Check your internet connection. The script will skip failed files and continue.

**Problem:** Running out of disk space
- **Solution:** Use `--file-types pdf` to download only PDFs, or `--series` to download specific series.

**Problem:** Want to start over
- **Solution:** Delete the `tas_geological_maps/` directory and re-run.

## Contributing

Contributions welcome! Please open an issue or pull request.

## Contact

For questions about the geological data itself, contact:
- **Mineral Resources Tasmania**
- Phone: (03) 6165 4719 or (03) 6165 4713
- Email: info@mrt.tas.gov.au

## Acknowledgments

Data provided by Mineral Resources Tasmania (MRT), Department of State Growth, Tasmania, Australia.
