#!/bin/bash
# Create VRT (Virtual Raster) mosaics from TIF files
# VRTs are lightweight - they reference the original files without copying data
# Mosaics are saved within the folder structure alongside the original files

# Requires GDAL (install with: apt install gdal-bin)

set -e

echo "Creating VRT mosaics for Tasmania Geological Maps"
echo "=================================================="
echo ""

# Function to create VRT for a specific scale/category
create_vrt() {
    local category=$1
    local scale=$2
    local vrt_name=$3

    local base_dir="tas_geological_maps/${category}/${scale}"
    local tif_dir="${base_dir}/tif"

    if [ ! -d "$tif_dir" ]; then
        echo "⚠ Directory not found: $tif_dir"
        return
    fi

    local tif_count=$(find "$tif_dir" -name "*.tif" 2>/dev/null | wc -l)

    if [ "$tif_count" -eq 0 ]; then
        echo "⚠ No TIF files found in $tif_dir"
        return
    fi

    local output_vrt="${base_dir}/${vrt_name}.vrt"

    echo "Creating ${vrt_name}.vrt from ${tif_count} files..."
    echo "  Location: ${base_dir}/"
    gdalbuildvrt -overwrite "$output_vrt" "$tif_dir"/*.tif
    echo "✓ Created ${vrt_name}.vrt"
    echo ""
}

# Check if GDAL is installed
if ! command -v gdalbuildvrt &> /dev/null; then
    echo "ERROR: GDAL is not installed"
    echo ""
    echo "Install GDAL:"
    echo "  Ubuntu/Debian: sudo apt install gdal-bin"
    echo "  macOS: brew install gdal"
    echo "  Windows: Use OSGeo4W or conda"
    echo ""
    exit 1
fi

# Create VRTs for each series
echo "Creating mosaics by scale and series..."
echo ""

# Digital Geological Atlas - 1:25,000
create_vrt "Digital_Geological_Atlas" "1-25000" "mosaic_geology_1-25k"

# Geological Atlas - 1:50,000 & 1:63,360
create_vrt "Geological_Atlas" "1-50000_and_1-63360" "mosaic_geology_1-50k"

# Digital Geological Atlas - 1:250,000
create_vrt "Digital_Geological_Atlas" "1-250000" "mosaic_geology_1-250k"

# Statewide - 1:500,000
create_vrt "Statewide" "1-500000" "mosaic_statewide_1-500k"

# Mount Read Volcanics
create_vrt "Mount_Read_Volcanics" "various" "mosaic_mount_read_volcanics"

# Tasmanian Landslide Maps
create_vrt "Tasmanian_Landslide_Maps" "various" "mosaic_landslide_maps"

echo "=================================================="
echo "✓ VRT mosaics created within folder structure!"
echo ""
echo "Location:"
echo "  tas_geological_maps/"
echo "    ├── Digital_Geological_Atlas/1-25000/mosaic_geology_1-25k.vrt"
echo "    ├── Geological_Atlas/1-50000_and_1-63360/mosaic_geology_1-50k.vrt"
echo "    ├── Digital_Geological_Atlas/1-250000/mosaic_geology_1-250k.vrt"
echo "    └── etc..."
echo ""
echo "You can now open these VRT files in QGIS as single layers!"
echo ""
echo "To convert a VRT to a single GeoTIFF (warning: large file!):"
echo "  gdal_translate -co COMPRESS=LZW -co TILED=YES \\"
echo "    tas_geological_maps/Digital_Geological_Atlas/1-25000/mosaic_geology_1-25k.vrt \\"
echo "    tas_geological_maps/Digital_Geological_Atlas/1-25000/mosaic_geology_1-25k.tif"
