========================================
GST SELLER APPLICATION - START HERE
========================================

CURRENT STATUS:
✅ Backend is running on http://localhost:5000
❌ Frontend needs to be started

========================================
HOW TO START THE APPLICATION
========================================

METHOD 1: Using Batch Files (Easiest)
--------------------------------------
1. Double-click: start-backend.bat
2. Wait for "Running on http://127.0.0.1:5000"
3. Double-click: start-frontend.bat
4. Browser will open automatically at http://localhost:3000


METHOD 2: Manual Command (If batch files don't work)
------------------------------------------------------
STEP 1 - Start Backend (Terminal 1):
  cd backend
  python app.py

STEP 2 - Start Frontend (Terminal 2 - NEW window):
  cd frontend
  npm start


========================================
VERIFY IT'S WORKING
========================================

1. Backend API: http://localhost:5000/api/health
   Should show: {"status":"ok","message":"GST Seller API is running"}

2. Frontend App: http://localhost:3000
   Should show: GST Seller Dashboard


========================================
TROUBLESHOOTING
========================================

Problem: "Port already in use"
Solution:
- Stop other programs using port 5000 or 3000
- Or edit backend/app.py and change port to 5001

Problem: "npm not found"
Solution: Install Node.js from https://nodejs.org/

Problem: "python not found"
Solution: Install Python from https://www.python.org/downloads/

Problem: Frontend shows blank page
Solution: Open browser console (F12) and check for errors


========================================
WHAT TO DO NOW
========================================

Right now, your backend IS running. You need to:
1. Open a NEW terminal window
2. Run: cd frontend
3. Run: npm start
4. Wait for browser to open

Or just double-click: start-frontend.bat

========================================
