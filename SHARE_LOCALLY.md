# How to Share SellerSuite Locally with Friends

## Quick Setup

### Step 1: Find Your IP Address
Your computer's IP addresses:
- **Local Network IP**: `10.5.0.2` (for same WiFi)
- **VPN/Public IP**: `100.110.86.27` (for internet)

### Step 2: Start the Backend
```bash
# Option A: Double-click
start-backend.bat

# Option B: Command line
cd backend
python app.py
```

The backend will start on: `http://0.0.0.0:5000`

### Step 3: Start the Frontend
```bash
# In a NEW terminal window:
cd frontend
npm start
```

The frontend will start on: `http://localhost:3000`

### Step 4: Share with Friends

#### For Same WiFi Network:
Tell your friend to visit:
```
http://10.5.0.2:3000
```

#### For Different Network (Internet):
Tell your friend to visit:
```
http://100.110.86.27:3000
```

**Important Notes:**
- ⚠️ Make sure your **Windows Firewall** allows connections on ports 3000 and 5000
- ⚠️ Your friend needs port 5000 (backend API) to work properly

---

## Configure Frontend for External Access

The frontend is currently hardcoded to `localhost:5000`. To share externally, you have two options:

### Option A: Quick Fix (Manual)

1. Open `frontend/src/components/B2CSales.js`
2. Find line 19: `const API_BASE_URL = 'http://localhost:5000/api';`
3. Replace with your IP:
   ```javascript
   const API_BASE_URL = 'http://10.5.0.2:5000/api';
   ```
4. Restart frontend: `npm start` in frontend folder

### Option B: Dynamic (Better Solution)
See below for environment variable setup.

---

## Production Deployment Options

### Option 1: Deploy to Heroku (Free)
1. Create account at https://heroku.com
2. Install Heroku CLI
3. Run: `heroku create seller-suite`
4. Push code: `git push heroku main`
5. Your app will be live at: `https://seller-suite.herokuapp.com`

### Option 2: Deploy to Vercel (Free, Frontend)
1. Create account at https://vercel.com
2. Connect your GitHub repo
3. Auto-deploy on every commit

### Option 3: Deploy to Railway (Free Tier)
1. Create account at https://railway.app
2. New Project → Deploy from GitHub
3. Select your repository
4. Auto-deploy!

### Option 4: Deploy to AWS (Pay as you go)
- Use AWS Amplify for frontend
- Use AWS EC2 for backend
- Or use AWS App Runner

---

## Recommended: Deploy to Vercel + Railway

### Frontend (Vercel)
1. Go to https://vercel.com
2. Sign up with GitHub
3. Import project: `vkakkarvk/seller-suite`
4. Root Directory: `frontend`
5. Build Command: `npm install && npm run build`
6. Output Directory: `build`
7. Add environment variable:
   - Name: `REACT_APP_API_URL`
   - Value: `https://your-railway-backend.railway.app/api`

### Backend (Railway)
1. Go to https://railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub
4. Select your repository
5. Root Directory: `backend`
6. Add environment variables if needed

---

## Quick Local Testing with Friends

1. **Both on same WiFi?**
   - Start backend: `python backend/app.py` (in current terminal)
   - Start frontend: `npm start` (in frontend folder, new terminal)
   - Friend visits: `http://10.5.0.2:3000`

2. **Different locations?**
   - You need to expose port 5000 and 3000
   - Use ngrok: `ngrok http 3000`
   - Share the ngrok URL with friend

3. **Production Ready?**
   - Deploy to Vercel + Railway (recommended)
   - Or use Heroku for everything

---

## Troubleshooting

### Friend can't connect
- Check Windows Firewall settings
- Make sure backend is running
- Try accessing `http://YOUR-IP:5000/api/health` directly

### Port already in use
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Need to change ports?
- Backend: Edit line 738 in `backend/app.py`
- Frontend: `PORT=3001 npm start`
