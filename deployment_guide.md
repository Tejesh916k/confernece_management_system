# MongoDB Atlas Deployment Guide

## Quick Setup

1. **Run interactive setup:**
```bash
python config/atlas_setup.py
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Test connection locally:**
```bash
python config/database.py
```

## Deployment Steps

### For Heroku
```bash
heroku login
heroku create your-app-name
heroku config:set MONGODB_URI="your_atlas_connection_string"
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY="your-secret-key"
git push heroku main
```

### For Railway
```bash
railway login
railway init
railway link
railway up
```

### For Render
1. Connect GitHub repository
2. Create new Web Service
3. Set environment variables in dashboard
4. Deploy

### For PythonAnywhere
1. Upload files to PythonAnywhere
2. Create Web app with Flask
3. Set MONGODB_URI in Web app settings
4. Reload web app

## MongoDB Atlas Checklist

- [ ] Cluster created and running
- [ ] Database user created
- [ ] IP whitelist configured
- [ ] Connection string copied
- [ ] .env file configured locally
- [ ] Connection tested
- [ ] .env deployed to production
- [ ] Application running successfully
