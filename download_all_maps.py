#!/usr/bin/env python3
"""
Tasmania Geological Maps Downloader

Downloads all geological map sheets from Mineral Resources Tasmania's
Digital Geological Atlas and organizes them by map type, scale, and file format.

Data Source: https://www.mrt.tas.gov.au/products/geoscience_maps

Usage Examples:
    # Download all PDFs (latest versions only)
    python3 download_all_maps.py --latest-only --file-types pdf

    # Download all file types (PDF, TIF, ECW)
    python3 download_all_maps.py --latest-only --file-types all

    # Download specific series only
    python3 download_all_maps.py --series mrtwfs:Geology25kIndex --latest-only

    # Dry run (scrape links but don't download)
    python3 download_all_maps.py --dry-run --latest-only --file-types all

Output Structure:
    tas_geological_maps/
    ├── Digital_Geological_Atlas/1-25000/{pdf,tif,ecw}/
    ├── Geological_Atlas/1-50000_and_1-63360/{pdf,tif,ecw}/
    ├── Statewide/1-500000/{pdf,tif,ecw}/
    └── all_maps_metadata.json

Author: Created for public use
License: Data from Mineral Resources Tasmania
"""

import requests
import json
import os
import time
import argparse
import re
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

# Configuration
WFS_URL = "http://www.mrt.tas.gov.au/web-services/wfs"
BASE_DOWNLOAD_DIR = Path("tas_geological_maps")

# Map series configuration
# Structure: {layer_name: {category, scale, description}}
MAP_SERIES = {
    'mrtwfs:Geology25kIndex': {
        'category': 'Digital_Geological_Atlas',
        'scale': '1-25000',
        'description': 'Digital Geological Atlas 1:25,000 Scale Series'
    },
    'mrtwfs:Geology50kIndex': {
        'category': 'Geological_Atlas',
        'scale': '1-50000_and_1-63360',
        'description': 'Geological Atlas 1:50,000 and 1:63,360 Series'
    },
    'mrtwfs:Geology250kIndex': {
        'category': 'Digital_Geological_Atlas',
        'scale': '1-250000',
        'description': 'Digital Geological Atlas 1:250,000 Scale Series'
    },
    'mrtwfs:StateWideMapsIndex': {
        'category': 'Statewide',
        'scale': '1-500000',
        'description': 'Statewide 1:500,000 Scale Maps'
    },
    'mrtwfs:MtReadIndex': {
        'category': 'Mount_Read_Volcanics',
        'scale': 'various',
        'description': 'Mount Read Volcanics'
    },
    'mrtwfs:LandslideIndex': {
        'category': 'Tasmanian_Landslide_Maps',
        'scale': 'various',
        'description': 'Tasmanian Landslide Map Series'
    },
}

def fetch_map_index(layer_name):
    """Fetch the complete index of all map sheets from WFS service for a given layer"""
    print(f"\nFetching map index from {layer_name}...")

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

        print(f"  Found {len(features)} map sheets")
        return features

    except Exception as e:
        print(f"  Error fetching {layer_name}: {e}")
        return []

def extract_map_info(features, series_info):
    """Extract relevant information from each map sheet"""
    map_info_list = []

    for feature in features:
        props = feature.get('properties', {})

        # Different layers may have different field names, so we'll be flexible
        map_id = props.get('MAP_ID') or props.get('ID')
        title = props.get('TITLE') or props.get('NAME') or props.get('MAP_NAME')
        map_number = props.get('MAP_NUMBER') or props.get('MAP_NO')
        details = props.get('DETAILS') or props.get('DETAIL_URL')

        if not map_id or not details:
            continue

        info = {
            'id': map_id,
            'name': title,
            'map_number': map_number,
            'series': props.get('MAP_SERIES'),
            'scale': props.get('MAP_SCALE'),
            'num_versions': props.get('NUMBER_OF_VERSIONS'),
            'publication_date': props.get('PUBLICATION_DATE'),
            'detail_url': details,
            'category': series_info['category'],
            'category_scale': series_info['scale'],
        }
        map_info_list.append(info)

    return map_info_list

def scrape_download_links(detail_url):
    """Scrape the detail page to find download links"""
    try:
        response = requests.get(detail_url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        download_links = []

        # Find JavaScript download links
        # Format: viewTOMObjectWithDisclaimer('mrtdoc/map_catalogue/map_public/898152_4', 'blackmansbay25.pdf')
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)

            # Check if it's a JavaScript download link
            if 'viewTOMObjectWithDisclaimer' in href:
                match = re.search(r"viewTOMObjectWithDisclaimer\('([^']+)',\s*'([^']+)'\)", href)

                if match:
                    doc_path = match.group(1)
                    filename = match.group(2)

                    # Construct the actual download URL
                    download_url = f"https://www.mrt.tas.gov.au/{doc_path}/{filename}"

                    # Determine file type
                    file_ext = filename.split('.')[-1].lower()

                    download_links.append({
                        'url': download_url,
                        'text': text,
                        'filename': filename,
                        'type': file_ext,
                        'doc_path': doc_path,
                        'version': doc_path.split('_')[-1] if '_' in doc_path else '1'
                    })

        return download_links

    except Exception as e:
        print(f"  Error scraping {detail_url}: {e}")
        return []

def download_file(url, filepath):
    """Download a file from URL to filepath"""
    try:
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()

        # Create parent directory if it doesn't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)

        total_size = int(response.headers.get('content-length', 0))

        with open(filepath, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

        return True

    except Exception as e:
        print(f"    Error downloading {url}: {e}")
        return False

def main():
    """Main function to orchestrate the download process"""

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Download all geological map sheets from Tasmania'
    )
    parser.add_argument(
        '--file-types',
        nargs='+',
        default=['pdf'],
        choices=['pdf', 'tif', 'ecw', 'all'],
        help='File types to download (default: pdf only)'
    )
    parser.add_argument(
        '--latest-only',
        action='store_true',
        help='Download only the latest version of each map'
    )
    parser.add_argument(
        '--series',
        nargs='+',
        choices=list(MAP_SERIES.keys()) + ['all'],
        default=['all'],
        help='Which map series to download (default: all)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Scrape links but do not download files'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of maps to process per series (for testing)'
    )
    parser.add_argument(
        '--metadata-only',
        action='store_true',
        help='Only fetch metadata and save to JSON, no scraping or downloading'
    )

    args = parser.parse_args()

    # Handle 'all' options
    if 'all' in args.file_types:
        file_types = ['pdf', 'tif', 'ecw']
    else:
        file_types = args.file_types

    if 'all' in args.series:
        series_to_process = list(MAP_SERIES.keys())
    else:
        series_to_process = args.series

    print("="*80)
    print("Tasmania Geological Maps Downloader")
    print("="*80)
    print(f"Series to process: {len(series_to_process)}")
    print(f"File types: {', '.join(file_types)}")
    print(f"Latest only: {args.latest_only}")
    print(f"Dry run: {args.dry_run}")
    print(f"Metadata only: {args.metadata_only}")
    print("="*80)

    # Create base download directory
    BASE_DOWNLOAD_DIR.mkdir(exist_ok=True)

    all_maps_metadata = {}

    # Process each map series
    for layer_name in series_to_process:
        series_info = MAP_SERIES[layer_name]

        print(f"\n{'='*80}")
        print(f"Processing: {series_info['description']}")
        print(f"Category: {series_info['category']} | Scale: {series_info['scale']}")
        print(f"{'='*80}")

        # Step 1: Fetch map index
        features = fetch_map_index(layer_name)
        if not features:
            print("  No features found, skipping...")
            continue

        map_info_list = extract_map_info(features, series_info)

        if args.limit:
            map_info_list = map_info_list[:args.limit]
            print(f"  Limited to {len(map_info_list)} maps for testing")

        # Save metadata for this series
        series_key = layer_name.replace('mrtwfs:', '')
        all_maps_metadata[series_key] = {
            'series_info': series_info,
            'maps': map_info_list
        }

        if args.metadata_only:
            continue

        # Step 2: Scrape download links for each map
        print(f"\n  Scraping download links...")

        for i, info in enumerate(map_info_list, 1):
            if not info['detail_url']:
                print(f"  [{i}/{len(map_info_list)}] Skipping {info['name']} - no detail URL")
                continue

            map_name = info['name'] if info['name'] else f"map_{info['id']}"
            print(f"  [{i}/{len(map_info_list)}] {map_name} (ID: {info['id']})...")

            download_links = scrape_download_links(info['detail_url'])

            # Filter by file type
            filtered_links = [
                link for link in download_links
                if link['type'] in file_types
            ]

            # If latest_only, keep only the most recent version
            if args.latest_only and filtered_links:
                by_type = {}
                for link in filtered_links:
                    ftype = link['type']
                    if ftype not in by_type:
                        by_type[ftype] = []
                    by_type[ftype].append(link)

                # Keep the first one of each type (newest first)
                filtered_links = [links[0] for links in by_type.values()]

            info['download_links'] = filtered_links
            print(f"    Found {len(filtered_links)} download link(s)")

            # Be polite to the server
            time.sleep(1)

    # Save all metadata
    metadata_file = BASE_DOWNLOAD_DIR / "all_maps_metadata.json"
    print(f"\n{'='*80}")
    print(f"Saving metadata to {metadata_file}...")
    with open(metadata_file, 'w') as f:
        json.dump(all_maps_metadata, f, indent=2)

    if args.metadata_only or args.dry_run:
        status = "metadata collection" if args.metadata_only else "dry run"
        print(f"\n{status.title()} complete!")
        print(f"Metadata saved to: {metadata_file}")
        return

    # Step 3: Download all files with proper organization
    print(f"\n{'='*80}")
    print("Starting downloads...")
    print(f"{'='*80}\n")

    total_downloads = 0
    successful_downloads = 0
    stats_by_category = defaultdict(lambda: {'total': 0, 'success': 0})

    for series_key, series_data in all_maps_metadata.items():
        series_info = series_data['series_info']
        maps = series_data['maps']

        for info in maps:
            if not info.get('download_links'):
                continue

            for link in info['download_links']:
                total_downloads += 1

                # Build folder structure: category -> scale -> file_type
                category = series_info['category']
                scale = series_info['scale']
                file_type = link['type']

                download_dir = BASE_DOWNLOAD_DIR / category / scale / file_type

                # Add map name to filename if needed
                map_name = info['name'] if info['name'] else f"map_{info['id']}"
                map_number = info['map_number'] if info['map_number'] else ''

                # Clean filename
                safe_name = map_name.replace('/', '_').replace(' ', '_')
                base_filename = link['filename']

                # If latest_only is false, include version in filename
                if not args.latest_only and 'version' in link:
                    name_parts = base_filename.rsplit('.', 1)
                    if len(name_parts) == 2:
                        base_filename = f"{name_parts[0]}_v{link['version']}.{name_parts[1]}"

                filepath = download_dir / base_filename

                if filepath.exists():
                    print(f"  ✓ Skipping {category}/{scale}/{file_type}/{base_filename} - already exists")
                    successful_downloads += 1
                    stats_by_category[category]['total'] += 1
                    stats_by_category[category]['success'] += 1
                    continue

                print(f"  ⬇ Downloading {category}/{scale}/{file_type}/{base_filename}...")
                if download_file(link['url'], filepath):
                    successful_downloads += 1
                    stats_by_category[category]['success'] += 1

                stats_by_category[category]['total'] += 1

                # Be polite to the server
                time.sleep(1)

    # Print summary
    print(f"\n{'='*80}")
    print("DOWNLOAD COMPLETE!")
    print(f"{'='*80}")
    print(f"Total files: {total_downloads}")
    print(f"Successfully downloaded: {successful_downloads}")
    print(f"Failed: {total_downloads - successful_downloads}")
    print(f"\nBreakdown by category:")
    for category, stats in sorted(stats_by_category.items()):
        print(f"  {category}: {stats['success']}/{stats['total']}")
    print(f"\nAll maps saved to: {BASE_DOWNLOAD_DIR.absolute()}")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
