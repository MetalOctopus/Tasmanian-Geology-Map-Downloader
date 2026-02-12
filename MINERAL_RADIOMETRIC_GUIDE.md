# Mineral Occurrences & Radiometric Data Guide

## Quick Download Commands

### Download Mineral Occurrences
```bash
mkdir -p tas_mineral_data
ogr2ogr -f "ESRI Shapefile" tas_mineral_data/mineral_occurrences.shp \
  "WFS:http://www.mrt.tas.gov.au/web-services/wfs" \
  "mrtwfs:MineralOccurences"
```

### Download Radiometric Data
```bash
source venv/bin/activate
python3 download_radiometric_gdal.py
```

---

## Mineral Occurrences Shapefile

### Overview
**8,295 mineral occurrences** across Tasmania including:
- Active and historic mines
- Mineral prospects
- Mineral deposits
- Exploration sites

### Attributes

| Field | Description | Examples |
|-------|-------------|----------|
| **DEPOSIT_NA** | Deposit/mine name | "Mt Lyell", "Renison Bell" |
| **COMMODITIE** | Minerals present | "Cu, Au, Ag", "Sn, W" |
| **COMMODITY_** | Commodity category | "Base Metals", "Gold" |
| **DEPOSIT_TY** | Deposit type | "VMS", "Skarn", "Orogenic gold" |
| **OPERATIONA** | Current status | "Operating", "Historic", "Prospect" |
| **LITHOSTRAT** | Host stratigraphy | "Mt Read Volcanics" |
| **ORE_GENESI** | Ore genesis | "Hydrothermal", "Magmatic" |
| **LOCATION_A** | Location accuracy | 10, 50, 100 meters |

### Common Commodities in Tasmania

**Base Metals:**
- Copper (Cu) - Mt Lyell, Rosebery
- Lead (Pb) - Rosebery, Mt Zeehan
- Zinc (Zn) - Rosebery, Hellyer
- Tin (Sn) - Renison Bell, Mt Bischoff

**Precious Metals:**
- Gold (Au) - Beaconsfield, Henty
- Silver (Ag) - Often with base metals

**Industrial Minerals:**
- Iron (Fe) - Savage River, Nelson Bay River
- Tungsten (W) - King Island
- Magnetite - Multiple locations

**Other:**
- Coal, limestone, dolomite, gypsum, talc

### Usage in QGIS

**1. Load the shapefile:**
```
Layer → Add Vector Layer → tas_mineral_data/mineral_occurrences.shp
```

**2. Filter by commodity:**
- Right-click layer → Filter
- Expression: `"COMMODITIE" LIKE '%Au%'` (for gold)
- Or: `"COMMODITIE" LIKE '%Cu%'` (for copper)

**3. Symbolize by status:**
- Properties → Symbology → Categorized
- Value: OPERATIONA
- Colors: Green=Operating, Orange=Historic, Blue=Prospect

**4. Label deposits:**
- Properties → Labels → Show labels
- Value: DEPOSIT_NA
- Size: 8-10pt

**5. Identify tool:**
- Click points to see full details
- View commodity, geology, ore description

### Useful Queries

**Major operating mines:**
```sql
"OPERATIONA" = 'Operating' AND "DEPOSIT_SI" IN ('Large', 'Very large')
```

**Gold prospects:**
```sql
"COMMODITIE" LIKE '%Au%' AND "DEPOSIT_TY" LIKE '%gold%'
```

**VMS deposits:**
```sql
"DEPOSIT_TY" LIKE '%VMS%' OR "ORE_GENESI" LIKE '%volcanogenic%'
```

---

## Radiometric Data

### Overview

Airborne gamma-ray spectrometric data at **40m resolution**:
- **Potassium (K)** - % concentration
- **Thorium (Th)** - ppm concentration
- **Uranium (U)** - ppm concentration
- **Total Count** - Total gamma dose
- **RGB Composite** - K=Red, Th=Green, U=Blue

### Coverage

| Region | Files | Notes |
|--------|-------|-------|
| King Island | 5 layers | Complete coverage |
| North West Tasmania | 5 layers | West coast, Mount Read |
| North East Tasmania | 5 layers | NE coast, Fingal |
| Flinders Island | 5 layers | Complete coverage |

**Note:** Mainland Tasmania coverage is partial. For full state coverage, contact MRT or use Geoscience Australia data.

### File Structure

```
tas_radiometric_data/
├── King_Island/
│   ├── potassium_K.tif       ← Potassium concentration
│   ├── thorium_Th.tif        ← Thorium concentration
│   ├── uranium_U.tif         ← Uranium concentration
│   ├── total_count.tif       ← Total gamma dose
│   └── composite_RGB.tif     ← ⭐ Start here!
├── North_West_Tasmania/
├── North_East_Tasmania/
└── Flinders_Island/
```

### Interpreting RGB Composites

**Color** | **Element** | **Common Geology**
----------|-------------|------------------
**Red** | High K | Jurassic dolerite, K-alteration, clays
**Green** | High Th | Granites, felsic volcanics, monazite
**Blue** | High U | Granites (with Th), U mineralization
**Yellow** | K + Th | Altered felsic rocks, potassic alteration
**Cyan** | Th + U | Granites
**Magenta** | K + U | Rare, altered zones
**White** | K + Th + U | Granites with K-alteration
**Dark/Black** | Low all | Mafic/ultramafic rocks, water, quartzite

### Tasmania-Specific Signatures

**Jurassic Dolerite** (Very common in Tasmania):
- **Bright red** in composite
- High K, low Th/U
- Covers ~40% of Tasmania
- Good geomorphic marker

**Mount Read Volcanics:**
- Variable signatures
- **Green** where felsic (Th-rich)
- **Red-yellow** where altered (K-alteration)
- Hosts major VMS deposits

**Granites** (Devonian):
- **Green-cyan-white** tones
- High Th + U, variable K
- Common in NE Tasmania, King Island

**Altered Zones** (Exploration Targets):
- **Yellow-red** - Potassic alteration
- **Green halos** - Chloritic alteration
- **Anomalous U** - Uranium mineralization
- Look for contrasts with host rocks

### Usage in QGIS

**1. Load RGB composite:**
```
Layer → Add Raster → tas_radiometric_data/North_West_Tasmania/composite_RGB.tif
```

**2. Adjust visualization:**
- Right-click → Properties → Symbology
- Render type: Multiband color
- Red: Band 1, Green: Band 2, Blue: Band 3
- Min/Max: Stretch to MinMax or Custom (1-95% clip)

**3. Overlay on geology:**
```
Add geological map mosaic (base)
Add radiometric RGB (50-70% transparency)
Add map sheet index (outlines)
```

**4. Identify signatures:**
- Use Identify tool
- Check individual K, Th, U values
- Compare with geology

**5. Extract single elements:**
Load individual files for detailed analysis:
- `potassium_K.tif` - Best for dolerite mapping
- `thorium_Th.tif` - Best for granites/felsics
- `uranium_U.tif` - Best for mineralization

### Exploration Applications

**1. Lithology Mapping:**
- Distinguish dolerite vs granite vs basalt
- Map alteration zones
- Identify unmapped units

**2. Structural Interpretation:**
- Linear features in radiometrics
- Offsets and breaks
- Anomaly patterns

**3. Alteration Mapping:**
- K-alteration (potassic)
- Sericitization (variable)
- Chlorite (low radiometrics)

**4. Target Generation:**
- **VMS deposits:** Look for Th highs (felsic volcanics) with alteration halos
- **Orogenic gold:** Structurally controlled, often in low-K units
- **Tin/tungsten:** Associated with Th-rich granites
- **Iron oxide deposits:** Often low radiometrics with K halos

**5. Integration with Mineral Occurrences:**
```
1. Load radiometric composite
2. Overlay mineral occurrences
3. Click known deposits
4. Note radiometric signature
5. Search for similar signatures elsewhere
```

### Advanced Analysis

**Ratio Images in QGIS:**

**Th/K Ratio** (Granite vs Dolerite):
```
Raster → Raster Calculator
Expression: "thorium_Th@1" / "potassium_K@1"
High values = Granites, Low values = Dolerite
```

**U/Th Ratio** (Alteration):
```
"uranium_U@1" / "thorium_Th@1"
Anomalous values may indicate alteration
```

### Data Quality Notes

**Resolution:** 40m nominal, actual varies by survey
**Projection:** GDA94 / MGA Zone 55 (EPSG:28355)
**Format:** GeoTIFF, LZW compressed
**Size:** Small (~100-200 KB per file) due to WMS extraction

**Limitations:**
- WMS download has lower resolution than source data
- Edge effects between surveys possible
- Not full Tasmania coverage

**For higher quality:**
- Contact MRT for full resolution grids
- Access via Geoscience Australia GADDS
- Consider Tiers Survey (2021) for recent data

---

## Integrated Workflow

### Complete Exploration Mapping Setup

**Step 1: Base Layers**
```
1. Add geological map mosaic (1:25k or 1:50k)
2. Add radiometric composite (50% transparency)
3. Add map sheet index (outlines, labels)
```

**Step 2: Reference Data**
```
4. Add mineral occurrences (colored by commodity)
5. Add boreholes (optional, from WFS: mrtwfs:Boreholes)
6. Add tenements (optional, from WFS: mrtwfs:Licences_Current)
```

**Step 3: Analysis**
```
7. Click mineral occurrences to see signatures
8. Identify similar radiometric patterns
9. Cross-reference with geology
10. Generate targets
```

**Step 4: Export**
```
11. Create new point layer for targets
12. Add attributes: confidence, commodity, notes
13. Export as KML or shapefile
```

### Example: VMS Exploration in Mount Read Volcanics

1. **Load layers:**
   - NW Tasmania radiometric RGB
   - 1:50k geology mosaic
   - Mineral occurrences (filter: VMS)

2. **Observe known VMS:**
   - Rosebery: Green Th signature (felsic host)
   - Hellyer: Variable, often red-yellow (alteration)
   - Note structural controls

3. **Search for similar:**
   - Scan for green Th highs (felsic volcanics)
   - Look for yellow-red halos (K-alteration)
   - Check linear structures
   - Avoid red (dolerite)

4. **Ground truth:**
   - Check against geological maps
   - Review mineral occurrence database
   - Check exploration licenses
   - Prioritize targets

---

## Additional Data Layers (WFS)

Other useful layers from MRT WFS:

```bash
# Boreholes
ogr2ogr -f GPKG data.gpkg WFS:"http://www.mrt.tas.gov.au/web-services/wfs" "mrtwfs:Boreholes"

# Gravity stations
ogr2ogr -f GPKG data.gpkg WFS:"http://www.mrt.tas.gov.au/web-services/wfs" "mrtwfs:GravityBaseStations"

# Current licenses
ogr2ogr -f GPKG data.gpkg WFS:"http://www.mrt.tas.gov.au/web-services/wfs" "mrtwfs:Licences_Current"

# Strategic resources
ogr2ogr -f GPKG data.gpkg WFS:"http://www.mrt.tas.gov.au/web-services/wfs" "mrtwfs:Strategic_Resources"
```

## References

- MRT WFS: http://www.mrt.tas.gov.au/web-services/wfs
- MRT Database Searches: https://www.mrt.tas.gov.au/products/database_searches
- Contact: info@mrt.tas.gov.au / (03) 6165 4800

## License

Data: Creative Commons Attribution 3.0 Australia (MRT)
Scripts: MIT License (this repository)
