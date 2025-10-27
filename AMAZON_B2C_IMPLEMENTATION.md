# Amazon B2C Small Implementation

## Overview
The application now supports parsing Amazon's "Ready to File" format for B2C Small transactions.

## Amazon File Format
- **Sheet Name**: `B2CSMALL` or `b2csmall`
- **Columns**:
  - Invoice Date
  - Invoice No
  - HSN
  - Description
  - Quantity
  - Taxable Value
  - CGST
  - SGST
  - IGST
  - Total

## How It Works

### 1. File Upload
When you upload an Amazon Ready to File report:
1. The backend reads the Excel file
2. Looks for the `B2CSMALL` or `b2csmall` sheet
3. Parses the columns according to Amazon's format
4. Calculates tax rates from tax amounts

### 2. Data Processing
- **Date Conversion**: Converts dates to DD/MM/YYYY format
- **Tax Rate Calculation**: 
  - CGST & SGST rates are calculated from CGST amount
  - IGST rate is calculated from IGST amount
  - Rates are in percentage (e.g., 9% = 9.00)
- **Data Cleaning**: Skips empty rows and handles missing values

### 3. CSV Generation
The generated CSV follows the GST portal format with columns:
- Invoice Date
- Invoice No
- HSN
- Description
- Quantity
- Taxable Value
- CGST Rate
- CGST
- SGST Rate
- SGST
- IGST Rate
- IGST
- Total

## Usage Instructions

1. **Download Amazon Report**:
   - Log into Amazon Seller Central
   - Go to Reports > Tax Document Library
   - Select "Ready to File" report
   - Download the Excel file

2. **Upload in Application**:
   - Select portal: "Amazon Seller Central"
   - Upload the Excel file
   - Review the data preview

3. **Generate CSV**:
   - Click "Generate CSV"
   - Download the generated file
   - Upload to GST portal

## Technical Details

### Backend Changes
- `parse_amazon_file()`: Reads specific sheet and column mapping
- Tax rate calculation logic
- Date formatting
- GST portal CSV format generation

### Frontend
- Portal selection: "Amazon Seller Central"
- File upload and preview
- CSV generation and download

## Testing
1. Use sample data from `Ready_to_File_B2CSMALL-12-11-2024_10-44-11.xlsx`
2. Upload through the application
3. Verify data preview matches the source
4. Generate CSV and validate format

## Future Enhancements
- Support for other Amazon report formats
- Validation of invoice numbers
- Duplicate detection
- Batch processing for multiple periods
