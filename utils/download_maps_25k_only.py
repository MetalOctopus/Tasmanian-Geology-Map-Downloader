#!/usr/bin/env python3
"""
Download all geological map sheets from Tasmania's Digital Geological Atlas
"""

import requests
import json
import os
import time
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configuration
WFS_URL = "http://www.mrt.tas.gov.au/web-services/wfs"
DETAIL_URL_TEMPLATE = "https://www.mrt.tas.gov.au/webdoc2/app/default/map_detail?id={}"
DOWNLOAD_DIR = Path("map_sheets")
METADATA_FILE = "map_metadata.json"

def fetch_map_index():
    """Fetch the complete index of all map sheets from WFS service"""
    print("Fetching map index from WFS service...")

    params = {
        'SERVICE': 'WFS',
        'VERSION': '1.1.0',
        'REQUEST': 'GetFeature',
        'TYPENAME': 'mrtwfs:Geology25kIndex',
        'outputFormat': 'application/json'
    }

    response = requests.get(WFS_URL, params=params)
    response.raise_for_status()

    data = response.json()
    features = data.get('features', [])

    print(f"Found {len(features)} map sheets")
    return features

def extract_map_info(features):
    """Extract relevant information from each map sheet"""
    map_info = []

    for feature in features:
        props = feature.get('properties', {})
        info = {
            'id': props.get('MAP_ID'),
            'name': props.get('TITLE'),
            'map_number': props.get('MAP_NUMBER'),
            'series': props.get('MAP_SERIES'),
            'scale': props.get('MAP_SCALE'),
            'num_versions': props.get('NUMBER_OF_VERSIONS'),
            'publication_date': props.get('PUBLICATION_DATE'),
            'detail_url': props.get('DETAILS')
        }
        map_info.append(info)

    return map_info

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
                # Parse the JavaScript call to extract doc_path and filename
                import re
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
                        'doc_path': doc_path
                    })

        return download_links

    except Exception as e:
        print(f"Error scraping {detail_url}: {e}")
        return []

def download_file(url, filepath):
    """Download a file from URL to filepath"""
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        # Create parent directory if it doesn't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Download with progress
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
        print(f"Error downloading {url}: {e}")
        return False

def main():
    """Main function to orchestrate the download process"""

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Download geological map sheets from Tasmania Digital Geological Atlas'
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
        '--dry-run',
        action='store_true',
        help='Scrape links but do not download files'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of maps to process (for testing)'
    )

    args = parser.parse_args()

    # Handle 'all' file types
    if 'all' in args.file_types:
        file_types = ['pdf', 'tif', 'ecw']
    else:
        file_types = args.file_types

    print(f"File types to download: {', '.join(file_types)}")
    print(f"Latest only: {args.latest_only}")
    print(f"Dry run: {args.dry_run}")

    # Create download directory
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    # Step 1: Fetch map index
    features = fetch_map_index()
    map_info = extract_map_info(features)

    if args.limit:
        map_info = map_info[:args.limit]
        print(f"Limited to {len(map_info)} maps for testing")

    # Save metadata
    print(f"\nSaving metadata to {METADATA_FILE}...")
    with open(METADATA_FILE, 'w') as f:
        json.dump(map_info, f, indent=2)

    # Step 2: Scrape download links for each map
    print("\nScraping download links from detail pages...")

    for i, info in enumerate(map_info, 1):
        if not info['detail_url']:
            print(f"[{i}/{len(map_info)}] Skipping {info['name']} - no detail URL")
            continue

        print(f"[{i}/{len(map_info)}] Processing {info['name']} (ID: {info['id']})...")

        download_links = scrape_download_links(info['detail_url'])

        # Filter by file type
        filtered_links = [
            link for link in download_links
            if link['type'] in file_types
        ]

        # If latest_only, keep only the most recent version
        if args.latest_only and filtered_links:
            # Group by file type
            by_type = {}
            for link in filtered_links:
                ftype = link['type']
                if ftype not in by_type:
                    by_type[ftype] = []
                by_type[ftype].append(link)

            # Keep the first one of each type (they're usually ordered newest first)
            filtered_links = [links[0] for links in by_type.values()]

        info['download_links'] = filtered_links

        print(f"  Found {len(filtered_links)} download link(s) matching criteria")

        # Be polite to the server
        time.sleep(1)

    # Save updated metadata with download links
    print(f"\nSaving updated metadata with download links...")
    with open(METADATA_FILE, 'w') as f:
        json.dump(map_info, f, indent=2)

    if args.dry_run:
        print("\nDry run complete - no files downloaded")
        print(f"Metadata saved to {METADATA_FILE}")
        return

    # Step 3: Download all files
    print("\nStarting downloads...")

    total_downloads = 0
    successful_downloads = 0

    for info in map_info:
        if not info.get('download_links'):
            continue

        # Create subdirectory for this map
        map_name = info['name'] if info['name'] else f"map_{info['id']}"
        map_number = info['map_number'] if info['map_number'] else ''
        dir_name = f"{map_number}_{map_name}".replace('/', '_').replace(' ', '_')
        map_dir = DOWNLOAD_DIR / dir_name

        for link in info['download_links']:
            total_downloads += 1
            filepath = map_dir / link['filename']

            if filepath.exists():
                print(f"  Skipping {link['filename']} - already exists")
                successful_downloads += 1
                continue

            print(f"  Downloading {link['filename']} ({link['text']})...")
            if download_file(link['url'], filepath):
                successful_downloads += 1

            # Be polite to the server
            time.sleep(1)

    print(f"\n{'='*60}")
    print(f"Download complete!")
    print(f"Total files: {total_downloads}")
    print(f"Successfully downloaded: {successful_downloads}")
    print(f"Failed: {total_downloads - successful_downloads}")
    print(f"Maps saved to: {DOWNLOAD_DIR.absolute()}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
