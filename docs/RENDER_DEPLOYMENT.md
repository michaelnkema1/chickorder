# Deploy ChickOrder to Render.com (Free Tier) 🚀

This guide walks you through deploying ChickOrder to Render.com's free tier with automatic SSL, PostgreSQL database, and continuous deployment from GitHub.

## 📋 Prerequisites

- GitHub account
- Render.com account (free) - [Sign up here](https://render.com)
- Your code pushed to GitHub repository

## 🎯 Quick Deploy (Recommended)

### Step 1: Push Your Code to GitHub

If you haven't already:

```bash
git add .
git commit -m "Add Render deployment config"
git push origin main
```

### Step 2: Deploy to Render

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click **"New +"** → **"Blueprint"**

2. **Connect Your GitHub Repository**
   - Select your `chickorder` repository
   - Render will detect the `render.yaml` file

3. **Review and Deploy**
   - Review the services that will be created:
     - PostgreSQL Database (Free tier - 90 days)
     - Backend API (Web Service)
     - Frontend (Static Site)
   - Click **"Apply"**

4. **Wait for Deployment** (~5-10 minutes)
   - Render will automatically:
     - Create PostgreSQL database
     - Build and deploy backend
     - Build and deploy frontend
     - Generate SSL certificates
     - Provide public URLs

### Step 3: Initialize Database

Once deployment completes:

1. Go to your backend service in Render dashboard
2. Click **"Shell"** tab
3. Run the initialization command:
   ```bash
   python init_db.py
   ```

### Step 4: Access Your Application

You'll get URLs like:
- **Frontend**: `https://chickorder-frontend.onrender.com`
- **Backend API**: `https://chickorder-backend.onrender.com`
- **API Docs**: `https://chickorder-backend.onrender.com/docs`

---

## 🔧 Manual Deployment (Alternative)

If you prefer manual setup:

### 1. Create PostgreSQL Database

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `chickorder-db`
   - **Database**: `chickorderdb`
   - **User**: `chickorder`
   - **Region**: Choose closest to you
   - **Plan**: Free
3. Click **"Create Database"**
4. Copy the **Internal Database URL** (starts with `postgresql://`)

### 2. Deploy Backend

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `chickorder-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Docker`
   - **Plan**: Free
   - **Docker Command**: Leave default
4. Add Environment Variables:
   ```
   DATABASE_URL=<paste internal database URL>
   SECRET_KEY=<generate random string>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ADMIN_EMAIL=admin@chickorder.com
   ADMIN_PASSWORD=admin123
   ENVIRONMENT=production
   DEBUG=False
   ```
5. Click **"Create Web Service"**

### 3. Deploy Frontend

1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `chickorder-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add Environment Variable:
   ```
   VITE_API_URL=https://chickorder-backend.onrender.com
   ```
5. Click **"Create Static Site"**

### 4. Initialize Database

Same as Quick Deploy Step 3 above.

---

## ⚙️ Configuration

### Update Frontend API URL

After backend is deployed, update the frontend environment:

1. Go to your frontend static site in Render
2. Go to **"Environment"** tab
3. Add/Update:
   ```
   VITE_API_URL=https://chickorder-backend.onrender.com
   ```
4. Click **"Save Changes"** (will trigger rebuild)

### Update Backend CORS

The backend should allow requests from your frontend URL. This is already configured in `main.py` with `allow_origins=["*"]`. For production, you might want to restrict to your frontend URL only.

---

## 🆓 Render Free Tier Limitations

- **PostgreSQL Database**: Free for 90 days, then $7/month
- **Web Services**: 
  - Spin down after 15 minutes of inactivity
  - First request after spin-down takes ~30 seconds (cold start)
  - 750 hours/month of runtime (enough for one service 24/7)
- **Static Sites**: Unlimited and always on
- **Bandwidth**: 100 GB/month

### Handling Cold Starts

Your backend may sleep after 15 minutes of inactivity. To prevent this:

1. Use a free uptime monitor like [UptimeRobot](https://uptimerobot.com) to ping your API every 14 minutes
2. Upgrade to paid plan ($7/month) for always-on service

---

## 🔄 Continuous Deployment

Render automatically deploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update features"
git push origin main

# Render will automatically detect and deploy changes
```

---

## 🐛 Troubleshooting

### Backend Not Starting

1. Check logs in Render dashboard
2. Verify `DATABASE_URL` environment variable is set correctly
3. Check if database is running

### Frontend Shows "Cannot connect to API"

1. Update `VITE_API_URL` in frontend environment variables
2. Ensure backend service is running
3. Check CORS configuration in backend

### Database Connection Failed

1. Verify database service is running
2. Use the **Internal Database URL** (not external)
3. Check database credentials

### Cold Start Issues

- First request after inactivity takes 30 seconds
- Use uptime monitoring service to keep backend warm
- Or upgrade to paid plan

---

## 📊 Monitoring

View logs and metrics in Render Dashboard:

1. **Logs**: Real-time application logs
2. **Metrics**: CPU, Memory, Request metrics
3. **Events**: Deployment history

---

## 🔐 Security Recommendations

1. **Change Admin Password**: 
   - Login to your app
   - Change the default admin password immediately

2. **Secret Keys**:
   - Use Render's "Generate Value" for sensitive env vars
   - Never commit API keys to Git

3. **Database Backups**:
   - Render doesn't backup free tier databases
   - Export data regularly if important

---

## 💰 Cost Breakdown (Free Tier)

- **Month 1-3**: $0 (everything free)
- **Month 4+**: $7/month (PostgreSQL only)
  - Backend & Frontend remain free
  - Alternative: Switch to SQLite (free forever, but loses data on restart)

---

## 🎉 Success!

Your ChickOrder application is now live and accessible to everyone!

**Default Admin Login:**
- Email: `admin@chickorder.com`
- Password: `admin123` (⚠️ CHANGE THIS IMMEDIATELY!)

---

## 📞 Support

If you encounter issues:
1. Check Render's [documentation](https://render.com/docs)
2. Review application logs in Render dashboard
3. Check GitHub repository issues
