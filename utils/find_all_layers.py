#!/usr/bin/env python3
"""
Find all available map index layers in the WFS service
"""

import requests
import xml.etree.ElementTree as ET

WFS_URL = "http://www.mrt.tas.gov.au/web-services/wms?SERVICE=WMS&REQUEST=GetCapabilities"

response = requests.get(WFS_URL)
root = ET.fromstring(response.content)

# Find all Layer elements
ns = {
    'wms': 'http://www.opengis.net/wms',
    '': 'http://www.opengis.net/wms'
}

print("Available Index Layers:")
print("="*80)

for layer in root.findall('.//Layer/Layer', ns):
    name_elem = layer.find('Name', ns)
    title_elem = layer.find('Title', ns)
    abstract_elem = layer.find('Abstract', ns)

    if name_elem is not None:
        name = name_elem.text
        # Only show index layers
        if 'index' in name.lower() or 'indx' in name.lower():
            title = title_elem.text if title_elem is not None else 'N/A'
            abstract = abstract_elem.text if abstract_elem is not None else 'N/A'

            print(f"\nLayer: {name}")
            print(f"Title: {title}")
            if abstract != 'N/A':
                print(f"Description: {abstract}")
