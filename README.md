# SellerSuite

Your complete business management platform for Indian sellers. Starting with GST returns - more features coming soon.

SellerSuite is designed to be a comprehensive product suite for everything a seller needs to run their business, with GST returns as our first launch feature. We're building the platform with scalability in mind to add more seller tools as we grow.

## Features

### Current (Phase 1)
- ✅ B2C Sales CSV Generator for GSTR-1
- Support for multiple portal formats (Amazon, Flipkart, Pepperfry, etc.)
- Upload Excel/CSV files from different portals
- Merge sales data from multiple sources
- Generate GST-compliant CSV for portal upload

### Planned Features (Seller Business Suite)

**GST & Compliance**
- GSTR-3B return assistance
- GSTR-9 annual return
- Audit trail and compliance reports

**Inventory & Operations**
- Multi-channel inventory sync
- Order management across portals
- Shipping label generation
- Returns & refund management

**Finance & Analytics**
- P&L statements
- Tax liability forecasting
- Revenue analytics by channel
- Cost tracking & profitability

**Automation & Integrations**
- Direct API integration with portals
- Automated reconciliation
- Chrome extension for quick access
- Mobile app for on-the-go management

## Tech Stack

- **Frontend**: React, Material-UI
- **Backend**: Python Flask
- **File Processing**: pandas, openpyxl

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

#### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## Usage

1. Navigate to the B2C Sales module
2. Upload CSV/Excel files from your selling portals (Amazon, Flipkart, etc.)
3. Review merged data
4. Download the GST-compliant CSV file
5. Upload to GST portal

## Portal Support

- Amazon Seller Central
- Flipkart Seller
- Pepperfry
- Myntra
- Custom marketplace exports

## License

MIT
