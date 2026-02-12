#!/usr/bin/env python3
"""
Download radiometric data from MRT WMS using GDAL
"""

import subprocess
import os
from pathlib import Path

OUTPUT_DIR = Path("tas_radiometric_data")
WMS_BASE = "https://www.mrt.tas.gov.au/erdas-iws/ogc/wms/?"

# Tasmania bounding boxes (approximate, in EPSG:4283 lat/lon)
REGIONS = {
    'King_Island': {
        'bbox': '143.7,-40.2,144.2,-39.5',
        'size': '2000x3000'
    },
    'North_West_Tasmania': {
        'bbox': '144.5,-41.6,146.5,-40.6',
        'size': '4000x3000'
    },
    'North_East_Tasmania': {
        'bbox': '146.8,-41.7,148.5,-40.7',
        'size': '4000x3000'
    },
    'Flinders_Island': {
        'bbox': '147.9,-40.5,148.5,-39.9',
        'size': '2000x2500'
    },
}

# Layer definitions
LAYERS = {
    'King_Island': {
        'potassium_K': 'King_Island_k_nwsun.ecw',
        'thorium_Th': 'King_Island_th_nwsun.ecw',
        'uranium_U': 'King_Island_u_nwsun.ecw',
        'total_count': 'King_Island_tc_nwsun.ecw',
        'composite_RGB': 'King_Island_k_th_u_r_g_b.ecw',
    },
    'North_West_Tasmania': {
        'potassium_K': 'North_West_Tasmania_k_nwsun.ecw',
        'thorium_Th': 'North_West_Tasmania_th_nwsun.ecw',
        'uranium_U': 'North_West_Tasmania_u_nwsun.ecw',
        'total_count': 'North_West_Tasmania_tc_nwsun.ecw',
        'composite_RGB': 'North_West_Tasmania_k_th_u_r_g_b.ecw',
    },
    'North_East_Tasmania': {
        'potassium_K': 'North_East_Tasmania_k_nwsun.ecw',
        'thorium_Th': 'North_East_Tasmania_th_nwsun.ecw',
        'uranium_U': 'North_East_Tasmania_u_nwsun.ecw',
        'total_count': 'North_East_Tasmania_totaldose_nwsun.ecw',
        'composite_RGB': 'North_East_Tasmania_k_th_u_rgb.ecw',
    },
    'Flinders_Island': {
        'potassium_K': 'Flinders_Island_k_nwsun.ecw',
        'thorium_Th': 'Flinders_Island_th_nwsun.ecw',
        'uranium_U': 'Flinders_Island_u_nwsun.ecw',
        'total_count': 'Flinders_Island_totaldose_nwsun.ecw',
        'composite_RGB': 'Flinders_Island_k_th_u_rgb.ecw',
    },
}

def download_wms_layer(region_name, layer_name, layer_id, bbox, size):
    """Download a WMS layer as GeoTIFF"""

    output_dir = OUTPUT_DIR / region_name
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{layer_name}.tif"

    if output_file.exists():
        print(f"  ✓ Skipping {layer_name} - already exists")
        return True

    print(f"  Downloading {layer_name}...")

    # Build GDAL WMS XML
    wms_xml = f"""<GDAL_WMS>
    <Service name="WMS">
        <Version>1.3.0</Version>
        <ServerUrl>{WMS_BASE}</ServerUrl>
        <Layers>{layer_id}</Layers>
        <CRS>EPSG:4283</CRS>
        <ImageFormat>image/tiff</ImageFormat>
    </Service>
    <DataWindow>
        <UpperLeftX>{bbox.split(',')[0]}</UpperLeftX>
        <UpperLeftY>{bbox.split(',')[3]}</UpperLeftY>
        <LowerRightX>{bbox.split(',')[2]}</LowerRightX>
        <LowerRightY>{bbox.split(',')[1]}</LowerRightY>
        <SizeX>{size.split('x')[0]}</SizeX>
        <SizeY>{size.split('x')[1]}</SizeY>
    </DataWindow>
    <BandsCount>3</BandsCount>
    <BlockSizeX>1024</BlockSizeX>
    <BlockSizeY>1024</BlockSizeY>
</GDAL_WMS>"""

    # Save XML temporarily
    xml_file = output_dir / f"{layer_name}_wms.xml"
    with open(xml_file, 'w') as f:
        f.write(wms_xml)

    # Download using gdal_translate
    try:
        cmd = [
            'gdal_translate',
            '-of', 'GTiff',
            '-co', 'COMPRESS=LZW',
            '-co', 'TILED=YES',
            str(xml_file),
            str(output_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        # Remove XML file
        xml_file.unlink()

        if result.returncode == 0 and output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"    ✓ Downloaded {layer_name} ({size_mb:.1f} MB)")
            return True
        else:
            print(f"    ✗ Failed: {result.stderr[:200]}")
            return False

    except Exception as e:
        print(f"    ✗ Error: {str(e)[:100]}")
        if xml_file.exists():
            xml_file.unlink()
        return False

def main():
    print("="*80)
    print("Tasmania Radiometric Data Downloader")
    print("="*80)
    print()
    print("Downloading K, Th, U, Total Count, and RGB composite")
    print("Resolution: 40m cell size")
    print()

    OUTPUT_DIR.mkdir(exist_ok=True)

    total_layers = sum(len(layers) for layers in LAYERS.values())
    current = 0

    for region_name, region_layers in LAYERS.items():
        print(f"\n{'='*80}")
        print(f"{region_name}")
        print(f"{'='*80}")

        bbox = REGIONS[region_name]['bbox']
        size = REGIONS[region_name]['size']

        for layer_name, layer_id in region_layers.items():
            current += 1
            print(f"[{current}/{total_layers}] ", end='')
            download_wms_layer(region_name, layer_name, layer_id, bbox, size)

    print(f"\n{'='*80}")
    print("Download Complete!")
    print(f"{'='*80}")
    print(f"\nRadiometric data saved to: {OUTPUT_DIR.absolute()}")
    print()
    print("Layers per region:")
    print("  - potassium_K.tif")
    print("  - thorium_Th.tif")
    print("  - uranium_U.tif")
    print("  - total_count.tif")
    print("  - composite_RGB.tif (Red=K, Green=Th, Blue=U)")
    print()

if __name__ == '__main__':
    main()
