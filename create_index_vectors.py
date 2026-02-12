#!/usr/bin/env python3
"""
Create vector index files (GeoPackage) showing map sheet boundaries and attributes
These allow you to identify which PDF contains the legend for each area
"""

import requests
import json
from pathlib import Path

# Configuration
WFS_URL = "http://www.mrt.tas.gov.au/web-services/wfs"
BASE_DIR = Path("tas_geological_maps")

# Map series configuration
MAP_SERIES = {
    'mrtwfs:Geology25kIndex': {
        'category': 'Digital_Geological_Atlas',
        'scale': '1-25000',
        'output_name': 'index_1-25k_mapsheets.geojson'
    },
    'mrtwfs:Geology50kIndex': {
        'category': 'Geological_Atlas',
        'scale': '1-50000_and_1-63360',
        'output_name': 'index_1-50k_mapsheets.geojson'
    },
    'mrtwfs:Geology250kIndex': {
        'category': 'Digital_Geological_Atlas',
        'scale': '1-250000',
        'output_name': 'index_1-250k_mapsheets.geojson'
    },
    'mrtwfs:StateWideMapsIndex': {
        'category': 'Statewide',
        'scale': '1-500000',
        'output_name': 'index_statewide_mapsheets.geojson'
    },
    'mrtwfs:MtReadIndex': {
        'category': 'Mount_Read_Volcanics',
        'scale': 'various',
        'output_name': 'index_mount_read_mapsheets.geojson'
    },
    'mrtwfs:LandslideIndex': {
        'category': 'Tasmanian_Landslide_Maps',
        'scale': 'various',
        'output_name': 'index_landslide_mapsheets.geojson'
    },
}

def fetch_and_save_index(layer_name, series_info):
    """Fetch map index boundaries from WFS and save as GeoJSON"""

    category = series_info['category']
    scale = series_info['scale']
    output_name = series_info['output_name']

    print(f"\nFetching boundaries for {layer_name}...")

    params = {
        'SERVICE': 'WFS',
        'VERSION': '1.1.0',
        'REQUEST': 'GetFeature',
        'TYPENAME': layer_name,
        'outputFormat': 'application/json'
    }

    try:
        response = requests.get(WFS_URL, params=params, timeout=60)
        response.raise_for_status()

        data = response.json()
        features = data.get('features', [])

        if not features:
            print(f"  ⚠ No features found")
            return

        # Simplify properties to include only useful info
        for feature in features:
            props = feature.get('properties', {})

            # Create clean properties
            clean_props = {
                'map_name': props.get('TITLE') or props.get('NAME'),
                'map_number': props.get('MAP_NUMBER') or props.get('MAP_NO'),
                'scale': props.get('MAP_SCALE'),
                'series': props.get('MAP_SERIES'),
                'pub_date': props.get('PUBLICATION_DATE'),
                'versions': props.get('NUMBER_OF_VERSIONS'),
                'map_id': props.get('MAP_ID'),
                'detail_url': props.get('DETAILS'),
            }

            # Build relative path to PDF
            if clean_props['map_name']:
                # Find matching PDF file
                pdf_dir = BASE_DIR / category / scale / 'pdf'
                clean_props['pdf_path'] = f"{category}/{scale}/pdf/"

            feature['properties'] = clean_props

        # Save to appropriate directory
        output_dir = BASE_DIR / category / scale
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / output_name

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"  ✓ Saved {len(features)} map boundaries to {output_file}")

    except Exception as e:
        print(f"  ✗ Error: {e}")

def main():
    print("="*80)
    print("Creating Map Sheet Index Vectors")
    print("="*80)
    print()
    print("These GeoJSON files show the boundaries of each map sheet")
    print("and can be loaded in QGIS to identify which PDF to reference.")
    print()

    for layer_name, series_info in MAP_SERIES.items():
        fetch_and_save_index(layer_name, series_info)

    print()
    print("="*80)
    print("✓ Map sheet indices created!")
    print("="*80)
    print()
    print("Files saved as GeoJSON in each scale directory:")
    for series_info in MAP_SERIES.values():
        category = series_info['category']
        scale = series_info['scale']
        output = series_info['output_name']
        print(f"  {category}/{scale}/{output}")
    print()
    print("Load these in QGIS to:")
    print("  1. See map sheet boundaries")
    print("  2. Click a map sheet to see its name/number")
    print("  3. Open the corresponding PDF for the legend")
    print()
    print("To convert to Shapefile or GeoPackage in QGIS:")
    print("  Right-click layer → Export → Save Features As → [format]")

if __name__ == '__main__':
    main()
