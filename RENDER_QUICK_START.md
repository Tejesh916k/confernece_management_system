# Quick Render Deployment Checklist

## Pre-Deployment ✓
- [x] `requirements.txt` configured with gunicorn
- [x] `Procfile` created (already exists)
- [x] `render.yaml` configuration added
- [x] `.env.example` created
- [x] `app.py` updated for production
- [x] `.gitignore` configured

## Deployment Steps (In Order)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Render deployment ready"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/your-repo.git
git push -u origin main
```

### Step 2: Create Render Service
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your GitHub repository
5. Fill in details:
   - Name: `conference-management`
   - Runtime: `Python 3.11`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`

### Step 3: Add Environment Variables
In Render dashboard → Environment, add:
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<random-32-char-string>
MONGODB_URI=<your-mongodb-atlas-uri>
```

### Step 4: Deploy
Click "Create Web Service" and wait for deployment to complete.

## MongoDB Atlas Setup (If Using Render's MongoDB)
Skip this if using existing MongoDB Atlas connection.

1. In Render dashboard, select your service
2. Click "Blueprint" (if using render.yaml)
3. Render creates MongoDB database automatically
4. Connection string in Environment tab

## Verify Deployment
- [ ] App loads at https://your-service-name.onrender.com
- [ ] Can signup/login
- [ ] Can create conferences
- [ ] Can view dashboard
- [ ] Can see data in MongoDB Atlas

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError" | Add missing package to requirements.txt |
| "MONGODB_URI not found" | Set env var in Render dashboard |
| "Connection refused" | Check MongoDB whitelist allows Render IP |
| App loads but no styling | Check static file paths are correct |
| Uploads lost after restart | Use Render's persistent storage or cloud storage |

## Next Steps

After successful deployment:
1. Monitor logs in Render dashboard
2. Test all features thoroughly
3. Check MongoDB Atlas usage
4. Set up automated backups (recommended)
5. Consider upgrading to Starter tier for stability

## Important Notes

- **Free tier**: Services auto-sleep after 15 mins of inactivity
- **Database**: Free MongoDB on Render is limited; upgrade if needed
- **Files**: Uploads not persistent on free tier; consider AWS S3
- **Performance**: Starter tier recommended for production

## Support Resources
- Render Docs: https://render.com/docs
- MongoDB Atlas: https://www.mongodb.com/docs/atlas/
- Flask Deployment: https://flask.palletsprojects.com/en/2.3.x/deploying/
