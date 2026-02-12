# Utility Scripts

This directory contains development and testing utilities.

## Scripts

### `find_all_layers.py`
Lists all available WFS layers from the Mineral Resources Tasmania service.

```bash
python3 utils/find_all_layers.py
```

### `download_maps_25k_only.py`
Legacy script for downloading only 1:25,000 scale maps.
Use `download_all_maps.py` with `--series` instead.

### Test Scripts

The following scripts were used during development:
- `test_scraper.py` - Tests download link scraping
- `test_download_url.py` - Tests URL construction
- `inspect_geojson.py` - Inspects WFS GeoJSON responses

These are kept for reference but not needed for normal use.
