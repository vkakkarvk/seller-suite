# Deploy SellerSuite to Render

## Quick Start Guide

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Click "Get Started" or "Sign Up"
3. Sign up with your **GitHub account** (recommended for easy deployment)

### Step 2: Connect Your Repository
1. In Render dashboard, click "New +" button
2. Select "Web Service"
3. Connect your GitHub repository: `vkakkarvk/seller-suite`
4. Render will automatically detect your repo

### Step 3: Configure Backend Service

**Service Settings:**
- **Name**: `seller-suite-backend` (or any name you like)
- **Region**: Choose closest to you (e.g., Singapore for India)
- **Branch**: `main`
- **Root Directory**: `backend` ⬅️ **Important!**
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Instance Type**: Free ⬅️ Select free tier
- **Auto-Deploy**: Yes (deploys on every push to GitHub)

**Environment Variables** (optional, not needed for basic setup):
- `PYTHON_VERSION`: `3.11.0` (if needed)

### Step 4: Deploy!
1. Click "Create Web Service"
2. Wait 3-5 minutes for deployment
3. You'll get a URL like: `https://seller-suite-backend.onrender.com`

### Step 5: Test Your Backend
1. Visit your URL: `https://YOUR-APP-NAME.onrender.com/api/health`
2. You should see: `{"status": "ok", "message": "SellerSuite API is running"}`

---

## Update Frontend to Use Deployed Backend

Once backend is deployed, update frontend:

### Step 1: Update Frontend API URL
1. Edit `frontend/src/components/B2CSales.js`
2. Find line 19: `const API_BASE_URL = 'http://localhost:5000/api';`
3. Replace with your Render URL:
   ```javascript
   const API_BASE_URL = 'https://YOUR-APP-NAME.onrender.com/api';
   ```

### Step 2: Build Frontend
```bash
cd frontend
npm run build
```

### Step 3: Deploy Frontend to Render (Same Process)
1. In Render, create another "Static Site"
2. Connect same GitHub repo
3. **Settings:**
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
4. Deploy!

---

## What You'll Get

**Backend URL**: `https://seller-suite-backend.onrender.com`  
**Frontend URL**: `https://seller-suite-frontend.onrender.com`

---

## Important Notes

✅ **Free Tier**:
- 15 minutes of inactivity timeout (sleeps after 15 min)
- First visitor after sleep waits 30-60 seconds
- After wake-up, works normally
- 100GB bandwidth/month

✅ **Auto-Deploy**:
- Every time you push to GitHub, Render automatically redeploys
- No manual deployment needed!

✅ **Updates**:
- Just push to GitHub: `git push`
- Render deploys automatically

---

## Troubleshooting

### Backend not responding?
- Check deployment logs in Render dashboard
- Make sure `backend` folder is set as Root Directory
- Verify `requirements.txt` exists in backend folder

### Frontend can't connect to backend?
- Make sure frontend API URL points to your Render backend URL
- Check CORS settings (should already be configured)
- Make sure backend is deployed and running (green status)

### Build fails?
- Check that all dependencies are in `requirements.txt`
- Make sure Python version is compatible

---

## Next Steps

Once deployed:
1. Share your Render URL with friends
2. Test file upload functionality
3. Make changes locally and push to GitHub
4. Watch Render auto-deploy!

---

**Ready to deploy?** Just follow the steps above and you'll have your app live in 5 minutes! 🚀
