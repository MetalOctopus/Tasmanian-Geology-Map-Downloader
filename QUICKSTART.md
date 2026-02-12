# Quick Start Guide

## 1. Setup (One-time)

```bash
# Clone the repository
git clone https://github.com/MetalOctopus/Tasmanian-Geology-Map-Downloader.git
cd Tasmanian-Geology-Map-Downloader

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Choose Your Download

### Option A: Just PDFs (Recommended for Most Users)
**Size:** ~2-5 GB | **Time:** 10-20 minutes

```bash
python3 download_all_maps.py --latest-only --file-types pdf
```

### Option B: All File Types (GIS Users)
**Size:** ~20-50 GB | **Time:** 1-2 hours

```bash
python3 download_all_maps.py --latest-only --file-types all
```

### Option C: Specific Map Series
**Example:** Download only 1:25,000 scale maps (PDFs)

```bash
python3 download_all_maps.py \
  --series mrtwfs:Geology25kIndex \
  --latest-only \
  --file-types pdf
```

### Option D: Test First (Smart Choice!)
**Downloads:** 3 maps per series for testing

```bash
python3 download_all_maps.py --limit 3 --latest-only --file-types pdf
```

## 3. Monitor Progress

### Live Monitor
```bash
./monitor_download.sh
```

### Quick Check
```bash
# Count files
find tas_geological_maps -name "*.pdf" | wc -l

# Check size
du -sh tas_geological_maps
```

## 4. Find Your Maps

Maps are organized by type and scale:

```bash
# Browse structure
ls tas_geological_maps/

# Example: 1:25,000 PDFs
ls tas_geological_maps/Digital_Geological_Atlas/1-25000/pdf/

# Example: Landslide maps
ls tas_geological_maps/Tasmanian_Landslide_Maps/various/pdf/
```

## Available Map Series

| ID | Series | Maps | Scale |
|----|--------|------|-------|
| `mrtwfs:Geology25kIndex` | Digital Geological Atlas | 245 | 1:25,000 |
| `mrtwfs:Geology50kIndex` | Geological Atlas | 50 | 1:50,000 & 1:63,360 |
| `mrtwfs:Geology250kIndex` | Digital Geological Atlas | 5 | 1:250,000 |
| `mrtwfs:StateWideMapsIndex` | Statewide Maps | 15 | 1:500,000 |
| `mrtwfs:MtReadIndex` | Mount Read Volcanics | 17 | Various |
| `mrtwfs:LandslideIndex` | Landslide Maps | 58 | Various |

## Tips

- ✅ Start with `--limit 3` to test
- ✅ Use `--latest-only` to save space
- ✅ PDFs are best for viewing, TIFs for GIS work
- ✅ Downloads can be safely interrupted (Ctrl+C) and resumed
- ✅ The script skips files that already exist

## Need Help?

```bash
python3 download_all_maps.py --help
```

See [README.md](README.md) for full documentation.
