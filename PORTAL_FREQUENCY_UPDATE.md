# Portal Report Frequency Update

## Overview
Updated the GST Seller Application to support different report frequencies based on the selling portal. This ensures proper labeling and handling of monthly vs quarterly reports.

## Key Changes

### 1. Backend Changes (`backend/app.py`)

#### Added Portal Frequency Mapping
```python
PORTAL_FREQUENCY = {
    'amazon': 'quarterly',      # Amazon provides quarterly reports
    'flipkart': 'monthly',      # Flipkart provides monthly reports
    'pepperfry': 'monthly',     # Pepperfry provides monthly reports
    'custom': 'monthly'         # Default to monthly
}
```

#### Updated Upload Endpoint
- Now accepts `report_period` parameter
- Automatically detects report frequency based on portal
- Returns report frequency in response

#### Updated CSV Generation
- Accepts `report_frequency` parameter
- Includes report frequency in output filename
- Format: `b2cs_quarterly_20251026_151511.csv` or `b2cs_monthly_20251026_151511.csv`

### 2. Frontend Changes (`frontend/src/components/B2CSales.js`)

#### Upload Handler
- Stores report frequency from backend response
- Displays report frequency in success message
- Shows frequency in uploaded files list

#### CSV Generation
- Sends report frequency to backend
- Ensures output file is properly labeled

#### UI Display
- Shows report frequency alongside portal name
- Format: "Portal: Amazon | quarterly report | Rows: 10"

## Report Frequencies by Portal

### Amazon
- **Frequency**: Quarterly
- **Report Type**: "Ready to File" Excel report
- **Output**: `b2cs_quarterly_YYYYMMDD_HHMMSS.csv`
- **GST Filing**: Quarterly GSTR-1

### Flipkart (Coming Soon)
- **Frequency**: Monthly
- **Report Type**: Monthly seller report
- **Output**: `b2cs_monthly_YYYYMMDD_HHMMSS.csv`
- **GST Filing**: Monthly GSTR-1

### Pepperfry (Coming Soon)
- **Frequency**: Monthly
- **Report Type**: Monthly seller report
- **Output**: `b2cs_monthly_YYYYMMDD_HHMMSS.csv`
- **GST Filing**: Monthly GSTR-1

## How It Works

### 1. File Upload
1. User selects portal (Amazon, Flipkart, etc.)
2. System looks up portal's report frequency
3. User uploads file
4. Backend returns `report_frequency` in response

### 2. CSV Generation
1. Frontend sends data + report frequency to backend
2. Backend generates CSV with appropriate filename suffix
3. Output file clearly indicates report period

### 3. GST Filing
1. User knows if CSV is for monthly or quarterly filing
2. Can properly label and organize GST returns
3. Avoids confusion between different report types

## Example Flow

### Amazon (Quarterly)
```
User uploads: Amazon_July-Sept_2025.xlsx
Backend detects: quarterly report
Output file: b2cs_quarterly_20251026_151511.csv
GST filing: Quarterly GSTR-1 for Q2 FY2026
```

### Flipkart (Monthly - Coming Soon)
```
User uploads: Flipkart_August_2025.xlsx
Backend detects: monthly report
Output file: b2cs_monthly_20251026_151511.csv
GST filing: Monthly GSTR-1 for August 2025
```

## Benefits

1. **Clear Labeling**: Files clearly indicate report period
2. **Proper Organization**: Users can easily identify quarterly vs monthly reports
3. **Scalable Design**: Easy to add new portals with their specific frequencies
4. **GST Compliance**: Proper filing based on report type
5. **User Clarity**: No confusion about report period

## Future Enhancements

- [ ] Add date range selection for monthly reports
- [ ] Add quarter selection for quarterly reports
- [ ] Multi-file upload with automatic merging by period
- [ ] Report period validation against GST filing calendar
- [ ] Auto-suggest file names based on portal and period

## Testing

Test scenarios:
1. Upload Amazon quarterly report → Should generate `b2cs_quarterly_*.csv`
2. Upload Flipkart monthly report → Should generate `b2cs_monthly_*.csv`
3. Upload Pepperfry monthly report → Should generate `b2cs_monthly_*.csv`
4. Verify report frequency displayed in UI
5. Verify success message includes report type

## Configuration

To add a new portal:
1. Add entry to `PORTAL_FREQUENCY` in `backend/app.py`
2. Add portal option in frontend dropdown
3. Add parser function for portal format
4. Test with sample files
