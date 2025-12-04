# Render Deployment Guide - Conference Management System

## Prerequisites
- GitHub account with your project pushed
- Render account (https://render.com)
- MongoDB Atlas account with your connection string
- Your MongoDB connection string ready

## Deployment Steps

### 1. Push to GitHub
First, make sure your project is on GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/conference-management.git
git push -u origin main
```

### 2. Create Render Account & Connect GitHub
- Go to https://render.com
- Sign up with GitHub
- Click "New+" button
- Select "Web Service"
- Connect your GitHub account
- Select the repository with your project

### 3. Configure Web Service

**Name:** conference-management (or your preferred name)

**Runtime:** Python 3.11

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn app:app
```

**Instance Type:** Free (or Starter for better performance)

### 4. Add Environment Variables
In the Render dashboard, go to **Environment** and add:

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate a random string, e.g., using Python: python -c "import secrets; print(secrets.token_hex(32))">
MONGODB_URI=<your MongoDB Atlas connection string>
```

**How to get MongoDB Atlas URI:**
1. Go to MongoDB Atlas (https://cloud.mongodb.com)
2. Click on your cluster
3. Click "Connect"
4. Select "Drivers"
5. Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority&appName=AppName`)
6. Replace `<password>` with your actual password
7. Replace `<database>` with your database name

### 5. Deploy
- Click "Create Web Service"
- Render will automatically deploy when you push to GitHub
- Your app will be available at: `https://conference-management.onrender.com`

### 6. Enable Auto-Deploy (Optional)
- In Render dashboard, go to your service settings
- Under "Auto-Deploy", select "Yes"
- Now every push to main branch will auto-deploy

## Troubleshooting

### Deployment Fails
1. Check build logs in Render dashboard
2. Verify all dependencies are in `requirements.txt`
3. Check environment variables are set correctly

### MongoDB Connection Error
1. Verify MONGODB_URI is correct (no missing < > placeholders)
2. Check MongoDB Atlas IP whitelist - add Render's IP (0.0.0.0/0) or use "Allow from anywhere"
3. Ensure database exists in MongoDB Atlas

### Static Files Not Loading
1. Flask automatically serves static files from the `static/` folder
2. Make sure CSS and JS files are in `static/css/` and `static/js/`
3. Check that static file paths in templates are correct

### Session Not Persisting
- This is normal in free tier with multiple instances
- Consider upgrading to Starter tier for persistent sessions

## After Deployment

### First Time Setup
1. Go to your deployed app URL
2. Create an account and login
3. Test creating conferences, sessions, and attendees
4. Verify MongoDB is storing data

### Monitoring
1. Check Render logs regularly: Dashboard → Logs
2. Monitor MongoDB Atlas usage in MongoDB dashboard
3. Set up error notifications if available

### Scaling (When Needed)
- Upgrade from Free to Starter plan for reliability
- Upgrade MongoDB Atlas tier if storage/queries increase
- Consider adding caching with Redis for performance

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| FLASK_ENV | Flask environment | production |
| FLASK_DEBUG | Enable debug mode | False |
| SECRET_KEY | Flask secret key | generated-random-string |
| MONGODB_URI | MongoDB connection string | mongodb+srv://... |

## Important Notes

⚠️ **Free tier limitations:**
- Services spin down after 15 minutes of inactivity
- Limited compute power
- No persistent filesystem (uploads lost after restart)
- For production, upgrade to Paid tier

✅ **Best Practices:**
- Always use environment variables for secrets
- Never commit `.env` file to GitHub
- Keep `requirements.txt` updated
- Test locally before pushing
- Monitor logs regularly
