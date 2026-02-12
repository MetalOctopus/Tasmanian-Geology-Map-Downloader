#!/usr/bin/env python3
"""
List ALL available WFS layers from MRT
"""

import requests
import xml.etree.ElementTree as ET

WFS_URL = "http://www.mrt.tas.gov.au/web-services/wfs?SERVICE=WFS&REQUEST=GetCapabilities"

print("Fetching WFS capabilities...")
response = requests.get(WFS_URL, timeout=30)
root = ET.fromstring(response.content)

# Try multiple namespace variations
namespaces = [
    {'wfs': 'http://www.opengis.net/wfs', 'ows': 'http://www.opengis.net/ows'},
    {'wfs': 'http://www.opengis.net/wfs/2.0', 'ows': 'http://www.opengis.net/ows/1.1'},
]

print("All Available WFS Layers:")
print("="*80)

found = False
for ns in namespaces:
    for feature_type in root.findall('.//wfs:FeatureType', ns):
        found = True
        name_elem = feature_type.find('wfs:Name', ns)
        title_elem = feature_type.find('wfs:Title', ns)

        if name_elem is not None:
            name = name_elem.text
            title = title_elem.text if title_elem is not None else 'N/A'
            print(f"{name}")
            print(f"  {title}")
            print()

if not found:
    # Try without namespace
    for elem in root.iter():
        if 'Name' in elem.tag and elem.text and 'mrtwfs:' in elem.text:
            print(elem.text)
