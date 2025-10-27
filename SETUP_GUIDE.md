# GST Seller Application - Setup Guide

This guide will help you set up and run the GST Seller Application on your local machine.

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

## Installation

### 1. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Or if you're using a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the backend server:

```bash
python app.py
```

The backend API will be running on `http://localhost:5000`

### 2. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install Node.js dependencies:

```bash
npm install
```

Or using yarn:

```bash
yarn install
```

Run the frontend development server:

```bash
npm start
```

The frontend will be running on `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. You'll see the Dashboard with available features
3. Click on "B2C Sales" to start generating GST CSV files
4. Select the portal (Amazon, Flipkart, etc.)
5. Upload your sales data files (Excel or CSV)
6. Review the data preview
7. Click "Generate CSV" to create a GST-compliant file
8. Download the generated CSV file

## File Format

The application currently supports:
- Amazon Seller Central exports
- Flipkart seller reports
- Pepperfry data
- Custom Excel/CSV files

## Portal Column Mapping

### Amazon
- Invoice Date
- Invoice Number
- Product Code (HSN)
- Product Name
- Quantity
- Item Price (Taxable Value)
- IGST/CGST/SGST rates and amounts

### Flipkart
- Invoice Date
- Invoice ID
- HSN Code
- Product Title
- Quantity
- Selling Price
- Tax rates and amounts

### Custom Portals
You can upload any Excel/CSV file. The application will attempt to auto-detect columns.

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError`
**Solution**: Make sure all requirements are installed: `pip install -r requirements.txt`

**Issue**: Port 5000 already in use
**Solution**: Change the port in `backend/app.py` (last line: `app.run(debug=True, port=5001)`)

### Frontend Issues

**Issue**: `Cannot find module`
**Solution**: Reinstall dependencies: `npm install` or `yarn install`

**Issue**: CORS errors
**Solution**: Make sure Flask-CORS is installed and the backend is running

**Issue**: Cannot connect to backend
**Solution**: Check that the backend is running on port 5000 and update the API_BASE_URL in `frontend/src/components/B2CSales.js` if needed

## Next Steps

### To Add More Portal Support

1. Edit `backend/app.py`
2. Add a new parsing function similar to `parse_amazon_file()` or `parse_flipkart_file()`
3. Map the portal's columns to the GST format
4. Add the portal to the frontend dropdown in `frontend/src/components/B2CSales.js`

### To Add API Integration

1. Create API service modules in `backend/services/`
2. Add authentication handling
3. Create endpoints for fetching data from portals
4. Update frontend to support API-based upload

## Project Structure

```
GST/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── uploads/               # Uploaded files (auto-created)
│   └── output/                # Generated CSV files (auto-created)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── B2CSales.js    # B2C Sales component
│   │   │   ├── Dashboard.js   # Dashboard component
│   │   │   └── Layout.js      # Layout with navigation
│   │   ├── App.js             # Main app component
│   │   └── index.js           # Entry point
│   └── package.json           # Node dependencies
├── README.md                  # Project overview
├── SETUP_GUIDE.md            # This file
└── .gitignore                # Git ignore rules
```

## Support

For issues or questions, please refer to the main README.md or open an issue in the repository.
