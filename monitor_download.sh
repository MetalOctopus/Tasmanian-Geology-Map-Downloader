#!/bin/bash
# Monitor download progress

echo "=== Tasmania Geological Maps Download Monitor ==="
echo ""
echo "Download directory: tas_geological_maps/"
echo ""

while true; do
    clear
    echo "=== Download Progress (refreshing every 10 seconds) ==="
    echo "Current time: $(date '+%H:%M:%S')"
    echo ""

    # Count files by type
    pdf_count=$(find tas_geological_maps -name "*.pdf" 2>/dev/null | wc -l)
    tif_count=$(find tas_geological_maps -name "*.tif" 2>/dev/null | wc -l)
    ecw_count=$(find tas_geological_maps -name "*.ecw" 2>/dev/null | wc -l)
    total=$((pdf_count + tif_count + ecw_count))

    echo "Files downloaded:"
    echo "  PDF: $pdf_count"
    echo "  TIF: $tif_count"
    echo "  ECW: $ecw_count"
    echo "  Total: $total / ~1170"
    echo ""

    # Show total size
    size=$(du -sh tas_geological_maps 2>/dev/null | cut -f1)
    echo "Total size: $size"
    echo ""

    # Show most recent files
    echo "Most recent downloads:"
    find tas_geological_maps -type f \( -name "*.pdf" -o -name "*.tif" -o -name "*.ecw" \) -printf '%T+ %p\n' 2>/dev/null | sort -r | head -5 | cut -d' ' -f2- | sed 's/^/  /'
    echo ""

    # Check if process is still running
    if ! pgrep -f "download_all_maps.py" > /dev/null; then
        echo "✓ Download process completed!"
        break
    fi

    echo "Press Ctrl+C to stop monitoring (download continues in background)"
    sleep 10
done
