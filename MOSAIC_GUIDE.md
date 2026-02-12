# Creating Map Mosaics - Guide

## Problem: ECW Files Crashing QGIS

ECW format has licensing restrictions and often causes issues in QGIS. **Use the TIF files instead!**

## Solution 1: Use TIF Files Directly (Easiest)

The TIF files you downloaded work perfectly in QGIS:

```
tas_geological_maps/
├── Digital_Geological_Atlas/1-25000/tif/
├── Geological_Atlas/1-50000_and_1-63360/tif/
└── Statewide/1-500000/tif/
```

Just drag multiple TIF files into QGIS and they'll display together.

## Solution 2: Create VRT Mosaics in QGIS (Recommended!)

A VRT (Virtual Raster) stitches files together without copying data - it's lightweight and fast.

### Method A: Using QGIS GUI

1. **Open QGIS**

2. **Raster → Miscellaneous → Build Virtual Raster**

3. **Input layers:** Click `...` and select all TIF files you want to mosaic
   - For example, select all files in `tas_geological_maps/Digital_Geological_Atlas/1-25000/tif/`

4. **Resolution:** Choose "Highest" or "Average"

5. **Output file:** Save as `geology_25k.vrt`

6. **Click Run**

The VRT file is tiny (just a few KB) but displays all your maps as one seamless layer!

### Method B: Using Command Line

Install GDAL first:
```bash
# Ubuntu/WSL
sudo apt install gdal-bin

# macOS
brew install gdal
```

Then run the script:
```bash
chmod +x create_mosaics.sh
./create_mosaics.sh
```

This creates VRT files in the `mosaics/` directory:
- `geology_25k.vrt` - All 1:25,000 scale maps
- `geology_50k.vrt` - All 1:50,000 scale maps
- `geology_250k.vrt` - All 1:250,000 scale maps
- `geology_500k_statewide.vrt` - Statewide maps
- `mount_read_volcanics.vrt`
- `landslide_maps.vrt`

### Method C: GDAL Command (Manual)

For a specific scale, e.g., 1:25,000:

```bash
gdalbuildvrt mosaics/geology_25k.vrt \
  tas_geological_maps/Digital_Geological_Atlas/1-25000/tif/*.tif
```

## Solution 3: Convert to Single GeoTIFF (If Needed)

If you need a single file instead of a VRT:

### In QGIS:
1. Load the VRT into QGIS
2. Right-click layer → Export → Save As
3. Format: GeoTIFF
4. Compression: LZW
5. Tiled: Yes

### Command Line:
```bash
gdal_translate -co COMPRESS=LZW -co TILED=YES \
  mosaics/geology_25k.vrt mosaics/geology_25k.tif
```

⚠️ **Warning:** Single merged GeoTIFFs are HUGE! A 1:25,000 mosaic could be 50-100+ GB.

## Solution 4: Delete ECW Files (Save Space)

If you're using TIF files, you can delete the ECW files to save space:

```bash
# Check how much space ECW files use
du -sh tas_geological_maps/*/*/ecw

# Delete ECW files (careful!)
rm -rf tas_geological_maps/*/*/ecw
```

## Recommended Workflow

**For viewing/analysis:**
1. Use TIF files or create VRT mosaics
2. Load VRT in QGIS - works like a single layer but stays lightweight

**For sharing/publishing:**
1. Create VRT first
2. Export only the area you need as GeoTIFF using QGIS clip/export tools

## File Size Comparison

| Format | Size | Speed | Compatibility |
|--------|------|-------|---------------|
| ECW | Small (5-10 MB) | Fast | ⚠️ Licensing issues |
| TIF | Large (50-150 MB) | Medium | ✅ Universal |
| PDF | Small (1-5 MB) | N/A | Print only |
| VRT | Tiny (few KB) | Fast | ✅ QGIS/GDAL only |

## Tips

1. **Performance:** VRT files are faster than loading hundreds of individual files
2. **Organization:** Create separate VRTs for different scales
3. **Analysis:** Use VRTs for viewing, export to GeoTIFF only for final deliverables
4. **Storage:** Keep TIFs, delete ECWs if you don't need them

## Troubleshooting

**VRT shows gaps/seams:**
- This is normal - geological maps have distinct boundaries
- The maps don't overlap, they're adjacent sheets

**QGIS crashes with TIF files:**
- Your TIFs might be very large. Try:
  - Load fewer files at once
  - Increase QGIS cache: Settings → Options → Rendering
  - Build pyramids: Right-click layer → Properties → Pyramids

**Need help?**
- See QGIS documentation: https://docs.qgis.org/
- GDAL VRT info: https://gdal.org/drivers/raster/vrt.html
