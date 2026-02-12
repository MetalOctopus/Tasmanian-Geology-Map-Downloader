#!/usr/bin/env python3
"""
Find mineral occurrence and mining-related layers in WFS
"""

import requests
import xml.etree.ElementTree as ET

WFS_URL = "http://www.mrt.tas.gov.au/web-services/wfs?SERVICE=WFS&REQUEST=GetCapabilities"

response = requests.get(WFS_URL)
root = ET.fromstring(response.content)

ns = {
    'wfs': 'http://www.opengis.net/wfs',
    'ows': 'http://www.opengis.net/ows'
}

print("Mineral/Mining Related Layers in WFS")
print("="*80)

keywords = ['mineral', 'mine', 'occurrence', 'deposit', 'prospect', 'ore', 'metallogeny']

for feature_type in root.findall('.//wfs:FeatureType', ns):
    name_elem = feature_type.find('wfs:Name', ns)
    title_elem = feature_type.find('wfs:Title', ns)
    abstract_elem = feature_type.find('wfs:Abstract', ns)

    if name_elem is not None:
        name = name_elem.text
        title = title_elem.text if title_elem is not None else ''
        abstract = abstract_elem.text if abstract_elem is not None else ''

        combined = f"{name} {title} {abstract}".lower()
        if any(keyword in combined for keyword in keywords):
            print(f"\nLayer: {name}")
            print(f"Title: {title}")
            if abstract:
                print(f"Description: {abstract}")
