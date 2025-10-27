# Amazon B2CS - GST Return Implementation (P0)

## Overview
This feature allows Indian sellers to upload Amazon Seller Central "Ready to File" reports and automatically generate GSTR-1 B2C Small CSV files for GST returns.

## Current Scope (P0)
- **Supported Portal**: Amazon Seller Central only
- **Report Type**: "Ready to File" Excel report
- **Report Frequency**: Quarterly (Amazon specific)
- **File Format**: Excel (.xlsx) with multiple sheets
- **Target Sheet**: "B2C Small" tab
- **Output**: GST-compliant aggregated B2CS CSV

## Portal-Specific Report Frequencies
Different portals provide reports at different frequencies:
- **Amazon**: Quarterly reports (Q1, Q2, Q3, Q4)
- **Flipkart**: Monthly reports (each month separately)
- **Pepperfry**: Monthly reports (each month separately)

The system automatically detects and labels the report frequency based on the portal selected.

## How It Works

### 1. Amazon File Structure
Amazon's "Ready to File" Excel file contains:
- Multiple sheets: GSTIN, B2B, B2C Large, **B2C Small**, HSN Summary, etc.
- The **B2C Small** sheet contains aggregated sales data by state and tax rate
- Header row is at index 2 (third row) with columns:
  - Type, Place Of Supply, Rate, Applicable % of Tax Rate, Taxable Value, Cess Amount, E-Commerce GSTIN

### 2. Processing Logic
```python
# backend/app.py:parse_amazon_file()
1. Read Excel file and find 'B2C Small' sheet (case-insensitive)
2. Skip first 2 rows and read header row
3. Parse each data row by position:
   - Column 1: Place Of Supply (e.g., "06-Haryana")
   - Column 3: Rate (e.g., 0.18 → converted to 18)
   - Column 4: Taxable Value
4. Convert rate from decimal (0.18) to percentage (18)
5. Return array of {place_of_supply, rate, taxable_value}
```

### 3. CSV Generation
```python
# backend/app.py:generate_aggregated_b2cs()
1. Group data by state_code and tax_rate
2. Sum taxable values for each group
3. Map state codes to full state names
4. Generate CSV with columns:
   - Type: 'OE'
   - Place Of Supply: "06-Haryana" format
   - Rate: 5, 12, 18, or 28
   - Applicable % of Tax Rate: (blank)
   - Taxable Value: aggregated sum
   - Cess Amount: (blank)
   - E-Commerce GSTIN: (blank)
```

### 4. Output Format
The generated CSV matches the GST portal's B2CS format:
```csv
Type,Place Of Supply,Rate,Applicable % of Tax Rate,Taxable Value,Cess Amount,E-Commerce GSTIN
OE,06-Haryana,18,,965.25,,
OE,29-Karnataka,18,,1930.52,,
...
```

## Architecture - Scalable Design

### Portal Parsers Pattern
Each portal has its own parser function:
```python
def parse_amazon_file(file_path):    # ✅ Implemented
def parse_flipkart_file(file_path):  # 🔄 Coming Soon
def parse_pepperfry_file(file_path): # 🔄 Coming Soon
def parse_custom_file(file_path):    # 🔄 Coming Soon
```

### Adding New Portals (Future)
1. Add parser function following the pattern
2. Add portal to `SUPPORTED_PORTALS` list in `backend/app.py`
3. Update UI dropdown in `frontend/src/components/B2CSales.js`
4. Test with sample files

Example for Flipkart:
```python
def parse_flipkart_file(file_path):
    """Parse Flipkart seller reports"""
    try:
        df = pd.read_excel(file_path)
        # Map Flipkart-specific columns
        data = []
        for _, row in df.iterrows():
            data.append({
                'place_of_supply': row['state_code'],
                'rate': row['gst_rate'],
                'taxable_value': row['selling_price'],
                'portal': 'Flipkart'
            })
        return data
    except Exception as e:
        print(f"Error parsing Flipkart file: {str(e)}")
        return None
```

## User Workflow

### Step 1: Download Report from Amazon
1. Login to Amazon Seller Central
2. Navigate to: Reports → Tax Documents → GST Returns
3. Select period (monthly/quarterly)
4. Click "Ready to File" and download Excel file

### Step 2: Upload to Our Application
1. Open app at http://localhost:3000
2. Navigate to "B2C Sales" section
3. Select "Amazon - Ready to File Report" (only option currently)
4. Drag & drop the downloaded Excel file
5. Wait for processing confirmation

### Step 3: Generate & Download CSV
1. Review data preview (first 5 rows)
2. Click "Generate CSV"
3. Click "Download CSV" to get the final file
4. Upload the CSV to GST portal for filing

## Configuration

### State Code Mapping
Located in `backend/app.py`:
```python
STATE_MAPPING = {
    '01': 'Jammu & Kashmir',
    '06': 'Haryana',
    '29': 'Karnataka',
    # ... all 38 states
}
```

### Supported Portals
Located in `backend/app.py:upload_file()`:
```python
SUPPORTED_PORTALS = ['amazon']  # P0 scope
```

## Error Handling

### Common Issues
1. **Wrong sheet selected**: Automatically detects 'B2C Small' sheet
2. **Missing data**: Skips empty rows and zero taxable values
3. **Rate conversion**: Automatically converts 0.18 → 18
4. **Unsupported portal**: Clear error message with supported options

### Debug Output
Backend prints:
- Available sheets found
- Sheet being read
- Columns detected
- Number of rows processed
- Sample data (first 3 rows)

## Testing

### Sample Data
- Location: `C:\Users\vkakk\Downloads\GSTR-1_Quarterly_July-September_2025\sample.xlsx`
- Contains 4 states with tax rates 5%, 12%, 18%
- Expected output: 10 rows aggregated by state+rate

### Verification
1. Check row count matches Amazon file
2. Verify state codes are correct format (e.g., "06-Haryana")
3. Verify tax rates are percentages (5, 12, 18, 28)
4. Verify sums match original values

## Future Enhancements (P1+)

### Additional Portals
- [ ] Flipkart Seller Portal
- [ ] Pepperfry Seller Reports
- [ ] Generic CSV upload with column mapping

### Additional Report Types
- [ ] Amazon B2B Large customer reports
- [ ] HSN Summary reports
- [ ] GSTR-3B reconciliation

### Advanced Features
- [ ] Multi-file upload and merge
- [ ] Date range filtering
- [ ] Preview and edit before download
- [ ] Save templates for recurring reports
- [ ] Email notifications on completion

## Technical Stack
- **Backend**: Python Flask + pandas + openpyxl
- **Frontend**: React + Material-UI
- **Data Processing**: Pandas for Excel/CSV manipulation
- **File Formats**: Excel (.xlsx, .xls) → CSV

## Contributing
When adding support for a new portal:
1. Study the portal's Excel/CSV format
2. Create parser function matching existing pattern
3. Add comprehensive error handling
4. Add to SUPPORTED_PORTALS list
5. Update UI dropdown
6. Document in this file

## Support
For issues or questions:
- Check terminal logs for debug output
- Verify Amazon file format matches expected structure
- Ensure 'B2C Small' sheet exists in uploaded file
