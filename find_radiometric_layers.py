#!/usr/bin/env python3
"""
Find all available radiometric layers from MRT WMS
"""

import requests
import xml.etree.ElementTree as ET

WMS_URL = "https://www.mrt.tas.gov.au/erdas-iws/ogc/wms/?service=WMS&request=getcapabilities"

response = requests.get(WMS_URL)
root = ET.fromstring(response.content)

# WMS 1.3.0 namespace
ns = {'wms': 'http://www.opengis.net/wms'}

print("Available Radiometric Layers from MRT WMS")
print("="*80)

radiometric_keywords = ['radiometric', 'potassium', 'uranium', 'thorium', 'gamma', ' k ', ' u ', ' th ']

for layer in root.findall('.//wms:Layer/wms:Layer', ns):
    name_elem = layer.find('wms:Name', ns)
    title_elem = layer.find('wms:Title', ns)
    abstract_elem = layer.find('wms:Abstract', ns)

    if name_elem is not None and title_elem is not None:
        name = name_elem.text
        title = title_elem.text
        abstract = abstract_elem.text if abstract_elem is not None else ''

        # Check if radiometric related
        combined = f"{name} {title} {abstract}".lower()
        if any(keyword in combined for keyword in radiometric_keywords):
            print(f"\nLayer: {name}")
            print(f"Title: {title}")
            if abstract:
                print(f"Description: {abstract}")
