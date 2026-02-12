#!/bin/bash
# Download radiometric data from MRT WMS service
# Creates GeoTIFF files for K, Th, U, Total Count, and RGB composite

set -e

OUTPUT_DIR="tas_radiometric_data"
WMS_URL="https://www.mrt.tas.gov.au/erdas-iws/ogc/wms/?"

# EPSG:28355 = GDA94 / MGA zone 55 (Tasmania)
CRS="EPSG:28355"

echo "=================================================="
echo "Tasmania Radiometric Data Downloader"
echo "=================================================="
echo ""
echo "Downloading radiometric layers from MRT WMS"
echo "Output directory: ${OUTPUT_DIR}"
echo ""

# Check if GDAL is installed
if ! command -v gdal_translate &> /dev/null; then
    echo "ERROR: GDAL is not installed"
    echo ""
    echo "Install GDAL:"
    echo "  Ubuntu/Debian: sudo apt install gdal-bin"
    echo "  macOS: brew install gdal"
    echo ""
    exit 1
fi

# Create output directories
mkdir -p "${OUTPUT_DIR}/King_Island"
mkdir -p "${OUTPUT_DIR}/North_West_Tasmania"
mkdir -p "${OUTPUT_DIR}/North_East_Tasmania"
mkdir -p "${OUTPUT_DIR}/Flinders_Island"

# Function to download WMS layer
download_layer() {
    local region=$1
    local layer_name=$2
    local output_file=$3
    local description=$4

    echo "Downloading: ${description}"
    echo "  Region: ${region}"
    echo "  Layer: ${layer_name}"

    # Build WMS URL for GDAL
    local wms_layer="WMS:${WMS_URL}SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=${layer_name}&CRS=${CRS}&FORMAT=image/tiff"

    # Download using gdal_translate
    gdal_translate -of GTiff -co COMPRESS=LZW -co TILED=YES \
        "${wms_layer}" \
        "${OUTPUT_DIR}/${region}/${output_file}" 2>&1 | grep -v "Warning"

    if [ -f "${OUTPUT_DIR}/${region}/${output_file}" ]; then
        local size=$(du -h "${OUTPUT_DIR}/${region}/${output_file}" | cut -f1)
        echo "  ✓ Saved: ${output_file} (${size})"
    else
        echo "  ✗ Failed to download"
    fi
    echo ""
}

# Download King Island radiometric data
echo "==================================================
"
echo "King Island Radiometric Data"
echo "=================================================="
echo ""

download_layer "King_Island" "King_Island_k_nwsun.ecw" "potassium_K_NW.tif" "Potassium (K) - NW sun"
download_layer "King_Island" "King_Island_th_nwsun.ecw" "thorium_Th_NW.tif" "Thorium (Th) - NW sun"
download_layer "King_Island" "King_Island_u_nwsun.ecw" "uranium_U_NW.tif" "Uranium (U) - NW sun"
download_layer "King_Island" "King_Island_tc_nwsun.ecw" "total_count_NW.tif" "Total Count - NW sun"
download_layer "King_Island" "King_Island_k_th_u_r_g_b.ecw" "composite_KThU_RGB.tif" "Composite K-Th-U RGB"

# Download North West Tasmania
echo "=================================================="
echo "North West Tasmania Radiometric Data"
echo "=================================================="
echo ""

download_layer "North_West_Tasmania" "North_West_Tasmania_k_nwsun.ecw" "potassium_K_NW.tif" "Potassium (K) - NW sun"
download_layer "North_West_Tasmania" "North_West_Tasmania_th_nwsun.ecw" "thorium_Th_NW.tif" "Thorium (Th) - NW sun"
download_layer "North_West_Tasmania" "North_West_Tasmania_u_nwsun.ecw" "uranium_U_NW.tif" "Uranium (U) - NW sun"
download_layer "North_West_Tasmania" "North_West_Tasmania_tc_nwsun.ecw" "total_count_NW.tif" "Total Count - NW sun"
download_layer "North_West_Tasmania" "North_West_Tasmania_k_th_u_r_g_b.ecw" "composite_KThU_RGB.tif" "Composite K-Th-U RGB"

# Download North East Tasmania
echo "=================================================="
echo "North East Tasmania Radiometric Data"
echo "=================================================="
echo ""

download_layer "North_East_Tasmania" "North_East_Tasmania_k_nwsun.ecw" "potassium_K_NW.tif" "Potassium (K) - NW sun"
download_layer "North_East_Tasmania" "North_East_Tasmania_th_nwsun.ecw" "thorium_Th_NW.tif" "Thorium (Th) - NW sun"
download_layer "North_East_Tasmania" "North_East_Tasmania_u_nwsun.ecw" "uranium_U_NW.tif" "Uranium (U) - NW sun"
download_layer "North_East_Tasmania" "North_East_Tasmania_totaldose_nwsun.ecw" "total_count_NW.tif" "Total Count - NW sun"
download_layer "North_East_Tasmania" "North_East_Tasmania_k_th_u_rgb.ecw" "composite_KThU_RGB.tif" "Composite K-Th-U RGB"

# Download Flinders Island
echo "=================================================="
echo "Flinders Island Radiometric Data"
echo "=================================================="
echo ""

download_layer "Flinders_Island" "Flinders_Island_k_nwsun.ecw" "potassium_K_NW.tif" "Potassium (K) - NW sun"
download_layer "Flinders_Island" "Flinders_Island_th_nwsun.ecw" "thorium_Th_NW.tif" "Thorium (Th) - NW sun"
download_layer "Flinders_Island" "Flinders_Island_u_nwsun.ecw" "uranium_U_NW.tif" "Uranium (U) - NW sun"
download_layer "Flinders_Island" "Flinders_Island_totaldose_nwsun.ecw" "total_count_NW.tif" "Total Count - NW sun"
download_layer "Flinders_Island" "Flinders_Island_k_th_u_rgb.ecw" "composite_KThU_RGB.tif" "Composite K-Th-U RGB"

echo "=================================================="
echo "Download Complete!"
echo "=================================================="
echo ""
echo "Radiometric data saved to: ${OUTPUT_DIR}/"
echo ""
echo "Data includes:"
echo "  - Potassium (K) concentration"
echo "  - Thorium (Th) concentration"
echo "  - Uranium (U) concentration"
echo "  - Total gamma dose"
echo "  - Composite RGB (Red=K, Green=Th, Blue=U)"
echo ""
echo "Resolution: 40m cell size"
echo "Coverage: King Island, NW Tasmania, NE Tasmania, Flinders Island"
echo ""
echo "Note: WMS downloads may have size/resolution limits."
echo "For full resolution data, contact MRT: info@mrt.tas.gov.au"
