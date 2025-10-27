# Deploy Frontend to Render

## Current Status
- ✅ Backend deployed at: `https://seller-suite.onrender.com`
- ✅ Frontend `.env` file created with backend URL
- ✅ All changes committed to GitHub

## Step-by-Step: Deploy Frontend to Render

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Sign in with your account

### Step 2: Create New Static Site
1. Click "New +" button (top right)
2. Select "Static Site"

### Step 3: Connect Repository
1. Choose **"Connect a repository"**
2. Connect your GitHub account if not already connected
3. Select repository: **`vkakkarvk/seller-suite`**
4. Click "Connect"

### Step 4: Configure Static Site
Fill in the following settings:

- **Name**: `seller-suite-frontend` (or any name you like)
- **Environment**: `Static Site`
- **Root Directory**: `frontend` ⬅️ **IMPORTANT!**
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `build`
- **Auto-Deploy**: `Yes` (deploys automatically when you push to GitHub)

### Step 5: Add Environment Variable
Click "Add Environment Variable":
- **Key**: `REACT_APP_API_URL`
- **Value**: `https://seller-suite.onrender.com/api`

### Step 6: Deploy
1. Scroll down
2. Click "Create Static Site"
3. Wait 3-5 minutes for deployment

### Step 7: Get Your Frontend URL
Once deployment finishes, you'll get a URL like:
```
https://seller-suite-frontend.onrender.com
```

### Step 8: Test
1. Open the URL in browser
2. Check browser console (F12) → Should show: `Using API URL: https://seller-suite.onrender.com/api`
3. Try uploading a file

---

## Troubleshooting

### If build fails:
1. Check "Logs" tab in Render
2. Common issues:
   - Wrong `Root Directory` (should be `frontend`)
   - Missing dependencies (check `package.json`)
   - Build command error (check `npm run build` locally first)

### If upload doesn't work:
1. Check browser console (F12) for errors
2. Check that API URL is correct: `https://seller-suite.onrender.com/api`
3. Check backend is running: Visit `https://seller-suite.onrender.com/api/health`

---

## Need Help?
Share any error messages you see in:
- Render build logs
- Browser console (F12)
