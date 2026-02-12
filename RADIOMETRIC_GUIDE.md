# Tasmania Radiometric Data Guide

## Available Radiometric Data

Mineral Resources Tasmania provides airborne gamma-ray spectrometric data at **40m resolution** covering:

- **King Island**
- **North West Tasmania**
- **North East Tasmania**
- **Flinders Island**

### Data Types Available:

| Element | Description | Color in RGB Composite |
|---------|-------------|----------------------|
| **Potassium (K)** | Concentration in % | Red |
| **Thorium (Th)** | Concentration in ppm | Green |
| **Uranium (U)** | Concentration in ppm | Blue |
| **Total Count** | Total gamma dose | N/A |
| **RGB Composite** | K-Th-U ternary image | Combined |

## Method 1: Add WMS Layers Directly in QGIS (Recommended)

### Step-by-Step:

1. **Open QGIS**

2. **Layer → Add Layer → Add WMS/WMTS Layer**

3. **Click "New"** to create a new connection:
   - **Name:** `MRT Radiometric Data`
   - **URL:** `https://www.mrt.tas.gov.au/erdas-iws/ogc/wms/?`
   - Click **OK**

4. **Click "Connect"**

5. **Browse available layers:**
   - Expand folders to find radiometric layers
   - Look for layers containing: `K`, `Th`, `U`, `Radiometric Total`, `rgb`

6. **Select layers to add:**

   **For King Island:**
   - `King Is. K NW sun` - Potassium
   - `King Is. Th NW sun` - Thorium
   - `King Is. U NW sun` - Uranium
   - `King Is. K Th U rgb` - Composite (recommended!)

   **For North West Tasmania:**
   - `North West K NW sun` - Potassium
   - `North West Th NW sun` - Thorium
   - `North West U NW sun` - Uranium
   - `North West K Th U rgb` - Composite

   **Similar for North East and Flinders Island**

7. **Click "Add"**

### Understanding the Composite (RGB) Image:

- **Red areas** = High potassium (often Jurassic dolerite in Tasmania)
- **Green areas** = High thorium (granites, felsic rocks)
- **Blue areas** = High uranium (often associated with granites)
- **Yellow** (Red + Green) = High K + Th
- **White** = High K + Th + U

## Method 2: Download Radiometric Layers as GeoTIFF

Unfortunately, MRT doesn't provide direct download links for radiometric grids. However, you can:

### Option A: Export from QGIS

1. Add WMS layer as above
2. Right-click layer → Export → Save As
3. Format: GeoTIFF
4. Set CRS: EPSG:28355 (GDA94 / MGA Zone 55)
5. Specify extent (use layer extent or draw custom)
6. Click OK

**Note:** This may have resolution limits depending on zoom level.

### Option B: Request Data from MRT

For full-resolution radiometric grids:

**Contact MRT:**
- Email: info@mrt.tas.gov.au
- Phone: (03) 6165 4800

Request:
- Airborne radiometric survey data
- Potassium, thorium, uranium grids
- Specific regions needed
- Format: GeoTIFF or ASCII grid

They may provide:
- Full resolution grids (40m cell size)
- Complete coverage
- Additional derived products

## Method 3: Access via Geoscience Australia

Tasmania radiometric data is also available through Geoscience Australia:

### GADDS (Geophysical Archive Data Delivery System)

1. Visit: https://geoscience-au.maps.arcgis.com/home/index.html
2. Search for: "Tasmania radiometric"
3. Look for surveys:
   - **Tiers Survey (2021)** - Recent airborne magnetic & radiometric
   - **South West Tasmania (2001)** - Potassium grids, 40m resolution
   - Other regional surveys

### National Radiometric Map

The **Radiometric Map of Australia** includes Tasmania at 100m resolution:
- Access via Geoscience Australia portal
- Lower resolution than regional surveys
- State-wide coverage

## Available Radiometric Layers (WMS)

### King Island
```
King_Island_k_nwsun.ecw          - Potassium NW sun
King_Island_k_nesun.ecw          - Potassium NE sun
King_Island_th_nwsun.ecw         - Thorium NW sun
King_Island_th_nesun.ecw         - Thorium NE sun
King_Island_u_nwsun.ecw          - Uranium NW sun
King_Island_u_nesun.ecw          - Uranium NE sun
King_Island_tc_nwsun.ecw         - Total Count NW sun
King_Island_tc_nesun.ecw         - Total Count NE sun
King_Island_k_th_u_r_g_b.ecw     - RGB Composite ⭐
```

### North West Tasmania
```
North_West_Tasmania_k_nwsun.ecw      - Potassium NW sun
North_West_Tasmania_th_nwsun.ecw     - Thorium NW sun
North_West_Tasmania_u_nwsun.ecw      - Uranium NW sun
North_West_Tasmania_tc_nwsun.ecw     - Total Count NW sun
North_West_Tasmania_k_th_u_r_g_b.ecw - RGB Composite ⭐
```

### North East Tasmania
```
North_East_Tasmania_k_nwsun.ecw          - Potassium NW sun
North_East_Tasmania_th_nwsun.ecw         - Thorium NW sun
North_East_Tasmania_u_nwsun.ecw          - Uranium NW sun
North_East_Tasmania_totaldose_nwsun.ecw  - Total Count NW sun
North_East_Tasmania_k_th_u_rgb.ecw       - RGB Composite ⭐
```

### Flinders Island
```
Flinders_Island_k_nwsun.ecw          - Potassium NW sun
Flinders_Island_th_nwsun.ecw         - Thorium NW sun
Flinders_Island_u_nwsun.ecw          - Uranium NW sun
Flinders_Island_totaldose_nwsun.ecw  - Total Count NW sun
Flinders_Island_k_th_u_rgb.ecw       - RGB Composite ⭐
```

## Interpretation Tips

### Geology-Radiometric Relationships in Tasmania:

**High Potassium (K) - Red in composite:**
- Jurassic dolerite (widespread in Tasmania)
- Younger volcanic rocks
- Potassic alteration zones
- Clay-rich sediments

**High Thorium (Th) - Green in composite:**
- Granites and felsic intrusions
- Heavy mineral sands (monazite)
- Mature sediments
- Mount Read Volcanics

**High Uranium (U) - Blue in composite:**
- Granites (often with Th)
- Some volcanic rocks
- Uranium mineralization
- Altered zones

**Low response (dark in composite):**
- Mafic rocks (basalt, gabbro when not dolerite)
- Ultramafic rocks
- Quartzite
- Water bodies

### Using with Geological Maps:

1. Load radiometric composite as base layer
2. Add geological map mosaic with transparency (50-70%)
3. Add map sheet index as overlay
4. Compare radiometric signatures with mapped units

This helps:
- Verify geological boundaries
- Identify unmapped units
- Locate alteration zones
- Understand rock distribution

## Script for Future Enhancement

A download script is in progress but requires:
- Bounding box definitions for each region
- WMS to GeoTIFF conversion
- Proper georeferencing

For now, use QGIS WMS connection (Method 1) or contact MRT for full datasets.

## References

- MRT WMS Service: https://www.mrt.tas.gov.au/erdas-iws/ogc/wms/?
- MRT Digital Data: https://www.mrt.tas.gov.au/products/digital_data
- Contact: info@mrt.tas.gov.au / (03) 6165 4800

## Tips

1. **Start with RGB composite** - easiest to interpret
2. **Use NW sun angle** - generally provides good detail
3. **Compare with geology** - overlay on geological maps
4. **Check metadata** - note survey dates and parameters
5. **Mind the gaps** - not all of Tasmania is covered yet

For full state coverage, consider Geoscience Australia's national products.
