# How to Start the GST Seller Application

## 🚀 Quick Start (Easiest Method)

1. **Double-click `start-backend.bat`** - This starts the backend server
2. Wait for it to show "Running on http://127.0.0.1:5000"
3. **Double-click `start-frontend.bat`** - This starts the frontend server
4. Your browser will automatically open at http://localhost:3000

## 📝 Manual Method

If the batch files don't work, follow these steps:

### Step 1: Start Backend (Terminal 1)
```powershell
cd backend
python app.py
```

### Step 2: Start Frontend (Terminal 2)
Open a NEW terminal/powershell window:
```powershell
cd frontend
npm install  # Only needed the first time
npm start
```

## ✅ Check if it's working

1. Backend API: http://localhost:5000/api/health
2. Frontend App: http://localhost:3000

You should see a JSON response from the backend and the GST Seller dashboard from the frontend.

## ❌ Common Issues

### "Port already in use"
- Backend (5000): Change line 194 in `backend/app.py` from `port=5000` to `port=5001`
- Frontend (3000): It will ask to use port 3001 automatically

### "Module not found"
Run these commands:
```powershell
cd backend
pip install -r requirements.txt

cd ..\frontend
npm install
```

### Python not found
Install Python from https://www.python.org/downloads/

### npm not found  
Install Node.js from https://nodejs.org/

## 🎯 Need Help?

Check the detailed setup guide: SETUP_GUIDE.md
