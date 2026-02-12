#!/usr/bin/env python3
"""
Download aeromagnetic data from MRT WMS using GDAL
"""

import subprocess
import os
from pathlib import Path

OUTPUT_DIR = Path("tas_geophysics_data")
WMS_BASE = "https://www.mrt.tas.gov.au/erdas-iws/ogc/wms/?"

# Tasmania bounding box (full state)
TASMANIA_BBOX = '143.5,-43.7,148.6,-39.2'
TASMANIA_SIZE = '10000x8000'

# Regional bounding boxes
REGIONS = {
    'King_Island': {'bbox': '143.7,-40.2,144.2,-39.5', 'size': '2000x3000'},
    'North_West_Tasmania': {'bbox': '144.5,-41.6,146.5,-40.6', 'size': '4000x3000'},
    'North_East_Tasmania': {'bbox': '146.8,-41.7,148.5,-40.7', 'size': '4000x3000'},
    'Flinders_Island': {'bbox': '147.9,-40.5,148.5,-39.9', 'size': '2000x2500'},
}

# State-wide magnetic layers
STATEWIDE_LAYERS = {
    'TMI_100m': 'All_Tasmania_Magnetics.ecw',
    'RTP_tilt': 'All_Tasmania_TasMagTiltRTP.ecw',
    'RTP_1vd': 'All_Tasmania_Tas100mRTP1vd.ecw',
    'TMI_1vd_40m': 'All_Tasmania_Tas40mTMI1vd.ecw',
    'RTP_1vd_40m': 'All_Tasmania_Tas40mRTP1vd.ecw',
}

# Regional magnetic layers
REGIONAL_LAYERS = {
    'King_Island': {
        'TMI': 'King_Island_tmi_nwsun.ecw',
        'TMI_1vd': 'King_Island_tmi_vd1_nwsun.ecw',
    },
    'North_West_Tasmania': {
        'TMI': 'North_West_Tasmania_tmi_nwsun.ecw',
        'TMI_1vd': 'North_West_Tasmania_tmi_vd1_nwsun.ecw',
    },
    'North_East_Tasmania': {
        'TMI': 'North_East_Tasmania_tmi_nwsun.ecw',
        'TMI_1vd': 'North_East_Tasmania_tmi_1vd_nwsun.ecw',
    },
    'Flinders_Island': {
        'TMI': 'Flinders_Island_tmi_nwsun.ecw',
        'TMI_1vd': 'Flinders_Island_tmi_1VD_nwsun.ecw',
    },
}

# Gravity
GRAVITY_LAYERS = {
    'Gravity_Residual': 'All_Tasmania_TasResidualImg.ecw',
}

def download_wms_layer(output_subdir, layer_name, layer_id, bbox, size):
    """Download a WMS layer as GeoTIFF"""

    output_dir = OUTPUT_DIR / output_subdir
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

    xml_file = output_dir / f"{layer_name}_wms.xml"
    with open(xml_file, 'w') as f:
        f.write(wms_xml)

    try:
        cmd = [
            'gdal_translate',
            '-of', 'GTiff',
            '-co', 'COMPRESS=LZW',
            '-co', 'TILED=YES',
            str(xml_file),
            str(output_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
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
    print("Tasmania Magnetic & Gravity Data Downloader")
    print("="*80)
    print()
    print("Downloading:")
    print("  - State-wide magnetic compilations (TMI, RTP, 1VD)")
    print("  - Regional magnetic data (40m resolution)")
    print("  - Gravity residual")
    print()

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Download state-wide layers
    print("="*80)
    print("State-wide Magnetic Compilations")
    print("="*80)
    for layer_name, layer_id in STATEWIDE_LAYERS.items():
        download_wms_layer("Statewide", layer_name, layer_id, TASMANIA_BBOX, TASMANIA_SIZE)

    # Download gravity
    print("\n" + "="*80)
    print("Gravity Data")
    print("="*80)
    for layer_name, layer_id in GRAVITY_LAYERS.items():
        download_wms_layer("Statewide", layer_name, layer_id, TASMANIA_BBOX, TASMANIA_SIZE)

    # Download regional data
    for region_name, layers in REGIONAL_LAYERS.items():
        print(f"\n{'='*80}")
        print(f"{region_name} - High Resolution Magnetics")
        print(f"{'='*80}")

        bbox = REGIONS[region_name]['bbox']
        size = REGIONS[region_name]['size']

        for layer_name, layer_id in layers.items():
            download_wms_layer(f"Regional/{region_name}", layer_name, layer_id, bbox, size)

    print(f"\n{'='*80}")
    print("Download Complete!")
    print(f"{'='*80}")
    print(f"\nData saved to: {OUTPUT_DIR.absolute()}")
    print()
    print("Structure:")
    print("  Statewide/")
    print("    - TMI_100m.tif (Total Magnetic Intensity)")
    print("    - RTP_tilt.tif (Reduced to Pole, tilt derivative)")
    print("    - RTP_1vd.tif (RTP, 1st vertical derivative)")
    print("    - TMI_1vd_40m.tif (High-res 1st vertical derivative)")
    print("    - Gravity_Residual.tif")
    print("  Regional/[region]/")
    print("    - TMI.tif (40m resolution)")
    print("    - TMI_1vd.tif (1st vertical derivative)")
    print()
    print("Magnetic data use:")
    print("  TMI - Raw magnetic intensity")
    print("  1VD - Enhances edges, shows structures/contacts")
    print("  RTP - Removes magnetic inclination effects")
    print("  Tilt - Edge detection, lineament mapping")
    print()

if __name__ == '__main__':
    main()
