#!/usr/bin/env python3
"""
Show summary of available maps in each series
"""

import json
from pathlib import Path

metadata_file = Path("tas_geological_maps/all_maps_metadata.json")

if not metadata_file.exists():
    print("No metadata file found. Run with --metadata-only first.")
    exit(1)

with open(metadata_file) as f:
    data = json.load(f)

print("="*80)
print("TASMANIA GEOLOGICAL MAPS - SUMMARY")
print("="*80)

total_maps = 0

for series_key, series_data in data.items():
    info = series_data['series_info']
    maps = series_data['maps']

    print(f"\n{info['description']}")
    print(f"  Category: {info['category']}")
    print(f"  Scale: {info['scale']}")
    print(f"  Maps available: {len(maps)}")

    total_maps += len(maps)

print(f"\n{'='*80}")
print(f"TOTAL MAPS ACROSS ALL SERIES: {total_maps}")
print(f"{'='*80}")
