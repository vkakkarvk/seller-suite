# Quick Start Guide for Windows

## Step 1: Start Backend Server

Open PowerShell and run:
```powershell
cd backend
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

Keep this terminal window open.

## Step 2: Start Frontend Server

Open a NEW PowerShell window and run:
```powershell
cd frontend
npm install
npm start
```

Wait for it to open your browser automatically at `http://localhost:3000`

## Troubleshooting

### Backend not starting?
1. Make sure Python is installed: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Try a different port if 5000 is busy: Edit `backend/app.py` line 194, change `port=5000` to `port=5001`

### Frontend not starting?
1. Make sure Node.js is installed: `node --version`
2. Delete `node_modules` folder: `rmdir /s node_modules`
3. Reinstall: `npm install`
4. Start again: `npm start`

### Port already in use?
- Backend port (5000): Change in `backend/app.py`
- Frontend port (3000): Will ask automatically to use 3001

## Access the Application

Once both servers are running:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api/health
