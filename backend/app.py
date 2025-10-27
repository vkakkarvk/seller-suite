from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Portal report frequency mapping
PORTAL_FREQUENCY = {
    'amazon': 'quarterly',      # Amazon provides quarterly reports
    'flipkart': 'monthly',      # Flipkart provides monthly reports
    'pepperfry': 'monthly',     # Pepperfry provides monthly reports
    'custom': 'monthly'         # Default to monthly
}

# State code mapping for B2CS format
STATE_MAPPING = {
    '01': 'Jammu & Kashmir', '02': 'Himachal Pradesh', '03': 'Punjab', '04': 'Chandigarh',
    '05': 'Uttarakhand', '06': 'Haryana', '07': 'Delhi', '08': 'Rajasthan',
    '09': 'Uttar Pradesh', '10': 'Bihar', '11': 'Sikkim', '12': 'Arunachal Pradesh',
    '13': 'Nagaland', '14': 'Manipur', '15': 'Mizoram', '16': 'Tripura',
    '17': 'Meghalaya', '18': 'Assam', '19': 'West Bengal', '20': 'Jharkhand',
    '21': 'Odisha', '22': 'Chhattisgarh', '23': 'Madhya Pradesh', '24': 'Gujarat',
    '25': 'Daman and Diu', '26': 'Dadra & Nagar Haveli & Daman & Diu', '27': 'Maharashtra',
    '29': 'Karnataka', '30': 'Goa', '31': 'Lakshadweep', '32': 'Kerala',
    '33': 'Tamil Nadu', '34': 'Puducherry', '35': 'Andaman & Nicobar Islands',
    '36': 'Telangana', '37': 'Andhra Pradesh', '38': 'Ladakh'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_gstin_from_amazon_file(file_path):
    """Extract GSTIN from Amazon file - looks in first sheet for 'Merchant GSTIN' label"""
    try:
        # Read the first sheet without headers
        df = pd.read_excel(file_path, sheet_name=0, header=None)
        print(f"Reading first sheet for GSTIN extraction")
        print(f"First few rows:\n{df.head(20)}")
        
        # Search through the first 20 rows to find "Merchant GSTIN" label
        for idx in range(min(20, len(df))):
            row = df.iloc[idx]
            row_str = ' '.join([str(cell) for cell in row if pd.notna(cell)])
            
            # Check if this row contains "Merchant GSTIN"
            if 'merchant' in row_str.lower() and 'gstin' in row_str.lower():
                print(f"Found 'Merchant GSTIN' label in row {idx}")
                # The GSTIN value is typically in the next row (idx+1)
                if idx + 1 < len(df):
                    next_row = df.iloc[idx + 1]
                    # GSTIN is usually in the first few columns of the next row
                    for col in range(min(5, len(next_row))):
                        gstin = str(next_row.iloc[col])
                        gstin = gstin.strip()
                        print(f"Checking cell ({idx+1}, {col}): '{gstin}'")
                        # GSTIN format is 15 characters (e.g., 29AICPN1083C1ZI)
                        if gstin and len(gstin) >= 10 and gstin.replace('-', '').replace('_', '').isalnum() and not gstin.lower() in ['merchant gstin', 'gstin', 'nan']:
                            print(f"Valid GSTIN found: {gstin}")
                            return gstin
        
        print("No GSTIN found in first 20 rows")
        return None
    except Exception as e:
        print(f"Error extracting GSTIN: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def parse_amazon_file(file_path):
    """Parse Amazon seller reports - Ready to File format"""
    try:
        # Read all sheets
        xls = pd.ExcelFile(file_path)
        
        print(f"Available sheets: {xls.sheet_names}")
        
        # Try to read from B2C Small sheet (Amazon Ready to File format)
        # Find sheet name with case-insensitive matching
        b2c_sheet = None
        for sheet_name in xls.sheet_names:
            sheet_lower = sheet_name.lower()
            print(f"Checking sheet: '{sheet_name}' -> '{sheet_lower}'")
            if 'b2c' in sheet_lower and 'small' in sheet_lower:
                b2c_sheet = sheet_name
                print(f"Found B2C sheet: {b2c_sheet}")
                break
        
        if b2c_sheet:
            print(f"Reading from {b2c_sheet} sheet")
            # Skip first 2 rows and use row 2 (0-indexed) as header
            df = pd.read_excel(file_path, sheet_name=b2c_sheet, skiprows=2)
        else:
            # Try first sheet
            print(f"B2C Small sheet not found. Reading from first sheet: {xls.sheet_names[0]}")
            df = pd.read_excel(file_path, sheet_name=0)
        
        print(f"Columns in sheet: {df.columns.tolist()}")
        print(f"Number of rows: {len(df)}")
        print(f"First few rows:\n{df.head()}")
        
        # Check if this is already in aggregated format (Amazon Ready to File B2CS format)
        # The columns will be: Type, Place Of Supply, Rate, Taxable Value, etc.
        # Check if first row is header by looking at first row's first column
        first_row_first_col = df.iloc[0, 0] if len(df) > 0 else None
        is_header = (isinstance(first_row_first_col, str) and first_row_first_col.lower() == 'type')
        
        if is_header:
            print("Detected aggregated B2CS format with header row")
            # First row is header, skip it and parse data
            data = []
            for idx, row in df.iterrows():
                # Skip header row (first row)
                if idx == 0:
                    continue
                
                # Get values by position since columns may not be named correctly
                # Row structure: Type, Place Of Supply, Applicable % of Tax Rate, Rate, Taxable Value, Cess Amount, E-Commerce GSTIN
                place_of_supply = str(row.iloc[1]) if len(row) > 1 else ''
                
                if not place_of_supply or place_of_supply == 'nan' or place_of_supply == '':
                    continue
                
                # Get the rate from column 3 (index 3)
                rate = row.iloc[3] if len(row) > 3 else 0
                
                # Convert rate from decimal (0.18) to percentage (18)
                if rate > 0 and rate < 1:
                    rate = int(rate * 100)
                else:
                    rate = int(rate)
                
                # Get taxable value from column 4 (index 4)
                taxable_val = row.iloc[4] if len(row) > 4 else 0
                taxable_val = float(taxable_val or 0)
                
                if taxable_val == 0:
                    continue
                
                data.append({
                    'place_of_supply': place_of_supply,
                    'rate': rate,
                    'taxable_value': round(taxable_val, 2),
                    'portal': 'Amazon'
                })
            
            print(f"Parsed {len(data)} rows from aggregated B2CS format")
            print(f"Sample data: {data[:3] if len(data) >= 3 else data}")
            return data
        else:
            # Handle detailed format with individual invoices
            data = []
            for _, row in df.iterrows():
                # Skip empty rows
                if pd.isna(row.get('Invoice Date', '')) or row.get('Invoice Date', '') == '':
                    continue
                    
                # Parse date
                invoice_date = row.get('Invoice Date', '')
                if not pd.isna(invoice_date):
                    invoice_date = pd.to_datetime(invoice_date).strftime('%d/%m/%Y')
                
                # Get Place of Supply if available
                place_of_supply = str(row.get('Place Of Supply', '')) if not pd.isna(row.get('Place Of Supply', '')) else ''
                
                # Get tax rates - calculate from amounts if needed
                taxable_val = float(row.get('Taxable Value', 0) or 0)
                cgst_amt = float(row.get('CGST', 0) or 0)
                sgst_amt = float(row.get('SGST', 0) or 0)
                igst_amt = float(row.get('IGST', 0) or 0)
                
                # Calculate rates
                cgst_rate = 0
                sgst_rate = 0
                igst_rate = 0
                if taxable_val > 0:
                    if cgst_amt > 0:
                        cgst_rate = (cgst_amt / taxable_val) * 100
                        sgst_rate = cgst_rate
                    elif igst_amt > 0:
                        igst_rate = (igst_amt / taxable_val) * 100
                
                data.append({
                    'invoice_date': invoice_date,
                    'invoice_no': str(row.get('Invoice No', '')),
                    'hsn_code': str(row.get('HSN', '')),
                    'product_name': str(row.get('Description', '')),
                    'quantity': float(row.get('Quantity', 0) or 0),
                    'taxable_value': round(taxable_val, 2),
                    'cgst_rate': round(cgst_rate, 2),
                    'sgst_rate': round(sgst_rate, 2),
                    'igst_rate': round(igst_rate, 2),
                    'cgst_amount': round(cgst_amt, 2),
                    'sgst_amount': round(sgst_amt, 2),
                    'igst_amount': round(igst_amt, 2),
                    'total_amount': round(float(row.get('Total', 0) or 0), 2),
                    'place_of_supply': place_of_supply,
                    'portal': 'Amazon'
                })
            
            return data
    except Exception as e:
        print(f"Error parsing Amazon file: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def parse_amazon_b2b(file_path):
    """Parse Amazon B2B sheet from Ready to File report"""
    try:
        xls = pd.ExcelFile(file_path)
        print(f"Available sheets: {xls.sheet_names}")
        
        # Find B2B sheet
        b2b_sheet = None
        for sheet_name in xls.sheet_names:
            sheet_lower = sheet_name.lower()
            print(f"Checking sheet: '{sheet_name}' -> '{sheet_lower}'")
            if 'b2b' in sheet_lower and 'cn' not in sheet_lower and 'cdnr' not in sheet_lower:
                b2b_sheet = sheet_name
                print(f"Found B2B sheet: {b2b_sheet}")
                break
        
        if not b2b_sheet:
            print("B2B sheet not found")
            return []
        
        # Read B2B sheet
        df = pd.read_excel(file_path, sheet_name=b2b_sheet, skiprows=2)
        print(f"B2B Columns: {df.columns.tolist()}")
        print(f"B2B Rows: {len(df)}")
        print(f"B2B Sample:\n{df.head()}")
        
        # Debug: Print first row to understand structure
        if len(df) > 0:
            print(f"First row values: {df.iloc[0].tolist()}")
            print(f"First row keys: {df.columns.tolist()}")
            # Check if first row is header
            first_cell = str(df.iloc[0, 0]) if len(df.columns) > 0 else ''
            if first_cell and first_cell.lower() in ['buyer gstin', 'gstin/uin of recipient', 'gstin']:
                print("First row appears to be header, skipping it")
                # Skip the first row
                df = df.iloc[1:].reset_index(drop=True)
                print(f"After skipping header, {len(df)} rows remain")
        
        data = []
        for idx, row in df.iterrows():
            # Debug first few rows
            if idx < 3:
                print(f"Row {idx}: {row.tolist()}")
            
            # Skip empty rows - check by position since column names may not be correct
            first_col = row.iloc[0] if len(row) > 0 else None
            if pd.isna(first_col) or first_col == '' or str(first_col).lower() == 'nan':
                continue
            
            # B2B column order: 0=GSTIN, 1=ReceiverName, 2=InvoiceNumber, 3=InvoiceDate, 
            # 4=InvoiceValue, 5=PlaceOfSupply, 6=ReverseCharge, 7=App%TaxRate, 8=InvoiceType
            # 9=E-CommerceGSTIN, 10=Rate, 11=TaxableValue, 12=CessAmount
            
            # Get GSTIN - Column 0
            gstin = str(row.iloc[0]) if len(row) > 0 else ''
            if not gstin or gstin == 'nan':
                continue
            
            print(f"Processing B2B row with GSTIN: {gstin}")
            
            # Parse invoice date - Column index 3
            invoice_date = row.iloc[3] if len(row) > 3 else ''
            if not pd.isna(invoice_date):
                try:
                    dt = pd.to_datetime(invoice_date)
                    # Format as "9-May-25" (day without leading zero, abbreviated month, 2-digit year)
                    day = dt.day
                    month = dt.strftime('%b')  # Jan, Feb, Mar, etc.
                    year = dt.strftime('%y')   # 25, 26, etc.
                    invoice_date = f"{day}-{month}-{year}"
                except:
                    invoice_date = str(invoice_date)
            else:
                invoice_date = ''
            
            # Get invoice details
            invoice_no = str(row.iloc[2]) if len(row) > 2 else ''  # Invoice Number is column 2
            invoice_value = float(row.iloc[4] if len(row) > 4 else 0 or 0)  # Invoice Value is column 4
            
            # Get Place of Supply - Column 5
            place_of_supply = str(row.iloc[5]) if len(row) > 5 else ''
            
            # Extract state code from place of supply (format: "06-Haryana")
            state_code = place_of_supply.split('-')[0] if place_of_supply and '-' in place_of_supply else ''
            
            # Get Rate and Taxable Value
            rate = int(row.iloc[10] if len(row) > 10 else 0 or 0)  # Rate is column 10
            taxable_val = float(row.iloc[11] if len(row) > 11 else 0 or 0)  # Taxable Value is column 11
            
            # For IGST calculation - we'll use the rate from column 10 directly
            igst_amt = 0  # We'll calculate this from rate if needed
            
            # Rate is already provided in the data (column 10)
            # No need to calculate
            
            if invoice_value == 0:
                continue
            
            data.append({
                'buyer_gstin': gstin,
                'buyer_name': '',
                'invoice_no': invoice_no,
                'invoice_date': invoice_date,
                'invoice_value': round(invoice_value, 2),
                'place_of_supply': place_of_supply,
                'state_code': state_code,
                'reverse_charge': 'N',
                'applicable_tax_rate': '',
                'invoice_type': 'Regular B2B',
                'ecommerce_gstin': '',
                'rate': rate,
                'taxable_value': round(taxable_val, 2),
                'cess_amount': 0
            })
        
        print(f"Parsed {len(data)} B2B records")
        return data
    except Exception as e:
        print(f"Error parsing Amazon B2B: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def parse_flipkart_file(file_path):
    """Parse Flipkart seller reports"""
    try:
        df = pd.read_excel(file_path)
        # Map Flipkart columns to GST format
        data = []
        for _, row in df.iterrows():
            data.append({
                'gstin': '',
                'invoice_date': row.get('date', ''),
                'invoice_no': row.get('invoice_id', ''),
                'hsn_code': row.get('hsn', ''),
                'product_name': row.get('product_title', ''),
                'quantity': row.get('quantity', 0),
                'taxable_value': row.get('selling_price', 0),
                'igst_rate': row.get('igst', 0),
                'cgst_rate': row.get('cgst', 0),
                'sgst_rate': row.get('sgst', 0),
                'igst_amount': row.get('igst_value', 0),
                'cgst_amount': row.get('cgst_value', 0),
                'sgst_amount': row.get('sgst_value', 0),
                'total_amount': row.get('total_price', 0),
                'portal': 'Flipkart'
            })
        return data
    except Exception as e:
        print(f"Error parsing Flipkart file: {str(e)}")
        return None

def parse_custom_file(file_path):
    """Parse generic portal files - tries to auto-detect columns"""
    try:
        df = pd.read_excel(file_path)
        # Try to map common column names
        data = []
        for _, row in df.iterrows():
            data.append({
                'gstin': '',
                'invoice_date': '',
                'invoice_no': '',
                'hsn_code': '',
                'product_name': '',
                'quantity': 0,
                'taxable_value': 0,
                'igst_rate': 0,
                'cgst_rate': 0,
                'sgst_rate': 0,
                'igst_amount': 0,
                'cgst_amount': 0,
                'sgst_amount': 0,
                'total_amount': 0,
                'portal': 'Custom'
            })
        return data
    except Exception as e:
        print(f"Error parsing custom file: {str(e)}")
        return None

def generate_aggregated_b2cs(data):
    """Generate aggregated B2CS format by state and tax rate"""
    try:
        df = pd.DataFrame(data)
        
        # Check if data already has 'rate' (from Amazon aggregated format)
        if 'rate' not in df.columns:
            # Determine tax rate for each row (use CGST+SGST rate or IGST rate)
            df['rate'] = df.apply(lambda row: 
                int(row['cgst_rate']) if row.get('cgst_rate', 0) > 0 else 
                int(row['igst_rate']) if row.get('igst_rate', 0) > 0 else 0, axis=1)
        
        # Extract state code from place_of_supply (format: XX-StateName)
        df['state_code'] = df['place_of_supply'].apply(lambda x: x.split('-')[0] if x and '-' in x else '')
        
        # Group by state_code and rate, then sum taxable values
        aggregated = []
        
        if 'state_code' in df.columns and 'rate' in df.columns:
            # Group by state_code and rate
            grouped = df.groupby(['state_code', 'rate'])['taxable_value'].sum().reset_index()
            
            for _, row in grouped.iterrows():
                state_code = row['state_code']
                rate = row['rate']
                taxable_value = row['taxable_value']
                
                # Get state name from mapping
                state_name = STATE_MAPPING.get(state_code, 'Unknown')
                
                aggregated.append({
                    'Type': 'OE',
                    'Place Of Supply': f"{state_code}-{state_name}",
                    'Rate': rate,
                    'Applicable % of Tax Rate': '',
                    'Taxable Value': round(taxable_value, 2),
                    'Cess Amount': '',
                    'E-Commerce GSTIN': ''
                })
        
        return aggregated
    except Exception as e:
        print(f"Error generating aggregated B2CS: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def generate_b2b_csv(data):
    """Generate B2B CSV format for GSTR-1"""
    try:
        df = pd.DataFrame(data)
        
        b2b_records = []
        for _, row in df.iterrows():
            b2b_records.append({
                'GSTIN/UIN of Recipient': row.get('buyer_gstin', ''),
                'Receiver Name': row.get('buyer_name', ''),
                'Invoice Number': row.get('invoice_no', ''),
                'Invoice date': row.get('invoice_date', ''),
                'Invoice Value': row.get('invoice_value', 0),
                'Place Of Supply': row.get('place_of_supply', ''),
                'Reverse Charge': row.get('reverse_charge', 'N'),
                'Applicable % of Tax Rate': row.get('applicable_tax_rate', ''),
                'Invoice Type': row.get('invoice_type', 'Regular B2B'),
                'E-Commerce GSTIN': row.get('ecommerce_gstin', ''),
                'Rate': row.get('rate', 0),
                'Taxable Value': row.get('taxable_value', 0),
                'Cess Amount': row.get('cess_amount', 0)
            })
        
        return b2b_records
    except Exception as e:
        print(f"Error generating B2B CSV: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'SellerSuite API is running'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    portal = request.form.get('portal', 'custom')
    report_period = request.form.get('report_period', None)  # 'monthly' or 'quarterly'
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if portal is supported (P0: Only Amazon)
    SUPPORTED_PORTALS = ['amazon']
    if portal.lower() not in SUPPORTED_PORTALS:
        return jsonify({
            'error': f'Portal "{portal}" is not yet supported. Currently supporting: {", ".join(SUPPORTED_PORTALS).title()} only.',
            'supported_portals': SUPPORTED_PORTALS
        }), 400
    
    # Get report frequency for this portal
    report_frequency = PORTAL_FREQUENCY.get(portal.lower(), 'monthly')
    if report_period:
        report_frequency = report_period  # User can override
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Parse file based on portal
        if portal.lower() == 'amazon':
            data = parse_amazon_file(file_path)
        elif portal.lower() == 'flipkart':
            data = parse_flipkart_file(file_path)
        elif portal.lower() == 'pepperfry':
            data = parse_custom_file(file_path)  # Similar to custom
        else:
            data = parse_custom_file(file_path)
        
        if data is None:
            return jsonify({'error': 'Failed to parse file'}), 500
        
        # Extract GSTIN from Amazon file
        gstin = None
        if portal.lower() == 'amazon':
            gstin = extract_gstin_from_amazon_file(file_path)
            print(f"Extracted GSTIN: {gstin}")
            
            # If no GSTIN found in GSTIN sheet, try to extract from B2CS E-Commerce GSTIN column
            if not gstin and data:
                try:
                    df_temp = pd.DataFrame(data)
                    if 'place_of_supply' in df_temp.columns and data[0].get('portal') == 'Amazon':
                        # In aggregated format, we can get GSTIN from the Excel file's B2CS sheet
                        xls_temp = pd.ExcelFile(file_path)
                        for sheet_name in xls_temp.sheet_names:
                            if 'b2c' in sheet_name.lower() and 'small' in sheet_name.lower():
                                df_b2cs = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)
                                # The E-Commerce GSTIN is typically in column 6 (index 6)
                                if len(df_b2cs) > 1:  # Skip header row
                                    ecommerce_gstin = str(df_b2cs.iloc[1, 6]) if len(df_b2cs.columns) > 6 else ''
                                    if ecommerce_gstin and len(ecommerce_gstin.strip()) >= 10:
                                        gstin = ecommerce_gstin.strip()
                                        print(f"Extracted GSTIN from B2CS sheet E-Commerce column: {gstin}")
                                        break
                except Exception as e:
                    print(f"Error extracting GSTIN from data: {str(e)}")
        
        # Add debug info
        debug_info = []
        if portal.lower() == 'amazon':
            try:
                xls = pd.ExcelFile(file_path)
                debug_info.append(f"Sheets: {xls.sheet_names}")
                if xls.sheet_names:
                    df_temp = pd.read_excel(file_path, sheet_name=0)
                    debug_info.append(f"Columns in first sheet: {df_temp.columns.tolist()}")
                    debug_info.append(f"Rows in sheet: {len(df_temp)}")
            except:
                pass
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'rows_processed': len(data),
            'data': data[:10],  # Return first 10 rows for preview
            'debug_info': debug_info if debug_info else [],
            'report_frequency': report_frequency,  # 'monthly' or 'quarterly'
            'portal': portal,
            'gstin': gstin  # Return GSTIN if extracted
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/generate-csv', methods=['POST'])
def generate_csv():
    try:
        data = request.json.get('data', [])
        format_type = request.json.get('format', 'detailed')  # 'detailed' or 'aggregated'
        report_frequency = request.json.get('report_frequency', 'monthly')  # 'monthly' or 'quarterly'
        gstin = request.json.get('gstin', None)  # GSTIN from uploaded file
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create filename with GSTIN if available
        gstin_suffix = f"_{gstin}" if gstin else ""
        
        if format_type == 'aggregated':
            # Generate aggregated B2CS format
            aggregated_data = generate_aggregated_b2cs(data)
            period_suffix = 'quarterly' if report_frequency == 'quarterly' else 'monthly'
            output_filename = f"b2cs_{period_suffix}{gstin_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            
            gst_df = pd.DataFrame(aggregated_data)
            gst_df.to_csv(output_path, index=False)
            
            # Calculate total taxable value
            total_taxable_value = gst_df['Taxable Value'].sum() if 'Taxable Value' in gst_df.columns else 0
            
            return jsonify({
                'success': True,
                'filename': output_filename,
                'message': 'Aggregated B2CS CSV generated successfully',
                'rows': len(gst_df),
                'total_taxable_value': round(total_taxable_value, 2)
            })
        else:
            # Generate detailed format
            df = pd.DataFrame(data)
            output_filename = f"gstr1_b2c{gstin_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            
            # Check if this is aggregated data being generated as detailed
            # If so, automatically switch to aggregated format
            if 'place_of_supply' in df.columns and 'rate' in df.columns and 'invoice_date' not in df.columns:
                # This is aggregated data, regenerate as aggregated
                aggregated_data = generate_aggregated_b2cs(data)
                output_filename = f"b2cs_aggregated{gstin_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                gst_df = pd.DataFrame(aggregated_data)
                
                # Calculate total taxable value for aggregated format
                total_taxable_value = gst_df['Taxable Value'].sum() if 'Taxable Value' in gst_df.columns else 0
            else:
                # Create GST portal format columns
                gst_df = pd.DataFrame({
                    'Invoice Date': df['invoice_date'],
                    'Invoice No': df['invoice_no'],
                    'HSN': df['hsn_code'],
                    'Description': df['product_name'],
                    'Quantity': df['quantity'],
                    'Taxable Value': df['taxable_value'],
                    'CGST Rate': df['cgst_rate'],
                    'CGST': df['cgst_amount'],
                    'SGST Rate': df['sgst_rate'],
                    'SGST': df['sgst_amount'],
                    'IGST Rate': df['igst_rate'],
                    'IGST': df['igst_amount'],
                    'Total': df['total_amount']
                })
            
            # Save to CSV
            gst_df.to_csv(output_path, index=False)
            
            # Calculate total taxable value
            if 'Taxable Value' in gst_df.columns:
                total_taxable_value = gst_df['Taxable Value'].sum()
            elif 'taxable_value' in df.columns:
                total_taxable_value = df['taxable_value'].sum()
            else:
                total_taxable_value = 0
            
            return jsonify({
                'success': True,
                'filename': output_filename,
                'message': 'CSV generated successfully',
                'rows': len(gst_df),
                'total_taxable_value': round(total_taxable_value, 2)
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-b2b', methods=['POST'])
def generate_b2b():
    """Generate B2B CSV from uploaded Amazon file"""
    try:
        filename = request.json.get('filename', '')
        report_frequency = request.json.get('report_frequency', 'quarterly')
        gstin = request.json.get('gstin', None)  # GSTIN from uploaded file
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
        
        # Create filename with GSTIN if available
        gstin_suffix = f"_{gstin}" if gstin else ""
        
        # Find the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Parse B2B data from Amazon file
        b2b_data = parse_amazon_b2b(file_path)
        
        if not b2b_data:
            return jsonify({'error': 'No B2B data found in file'}), 400
        
        # Generate B2B CSV
        b2b_records = generate_b2b_csv(b2b_data)
        
        if not b2b_records:
            return jsonify({'error': 'Failed to generate B2B CSV'}), 500
        
        # Save to CSV file
        period_suffix = 'quarterly' if report_frequency == 'quarterly' else 'monthly'
        output_filename = f"b2b_{period_suffix}{gstin_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        b2b_df = pd.DataFrame(b2b_records)
        b2b_df.to_csv(output_path, index=False)
        
        # Calculate total taxable value for B2B
        total_taxable_value = b2b_df['Taxable Value'].sum() if 'Taxable Value' in b2b_df.columns else 0
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'message': 'B2B CSV generated successfully',
            'rows': len(b2b_df),
            'total_taxable_value': round(total_taxable_value, 2)
        })
    
    except Exception as e:
        print(f"Error in generate_b2b: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 5000))
    # Run on all interfaces (0.0.0.0) to allow external connections
    app.run(debug=True, host='0.0.0.0', port=port)
