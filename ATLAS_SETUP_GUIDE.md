# MongoDB Atlas Configuration - Step by Step Guide

## Table of Contents
1. [Account Setup](#account-setup)
2. [Create Organization & Project](#create-organization--project)
3. [Create Database Cluster](#create-database-cluster)
4. [Create Database User](#create-database-user)
5. [Configure Network Access](#configure-network-access)
6. [Get Connection String](#get-connection-string)
7. [Configure Application](#configure-application)
8. [Test Connection](#test-connection)
9. [Deploy to Production](#deploy-to-production)

---

## Account Setup

### Step 1.1: Create MongoDB Atlas Account
1. Open https://www.mongodb.com/cloud/atlas in your browser
2. Click **"Try Free"** or **"Sign Up"**
3. Choose sign-up method:
   - Email/Password
   - Google Account
   - GitHub Account
4. Fill in required information
5. Accept terms and conditions
6. Click **"Create Your Atlas Account"**
7. **Check your email** and verify your account
8. Complete the setup wizard (optional but recommended)

✓ **Result:** You now have a MongoDB Atlas account

---

## Create Organization & Project

### Step 2.1: Create Organization (Optional)
1. Log in to MongoDB Atlas
2. In top-left, click the **Organization dropdown**
3. Click **"Create New Organization"**
4. Enter Organization Name: `Conference Management`
5. Click **"Create Organization"**

### Step 2.2: Create Project
1. Click **"Create New Project"** or **"+ New Project"**
2. Enter Project Name: `conference-system`
3. Select Organization (if created above)
4. Click **"Create Project"**
5. Wait for project to be created (usually instant)

✓ **Result:** Project created and ready for cluster

---

## Create Database Cluster

### Step 3.1: Build Cluster
1. In your project, click **"Build a Database"** or **"Create Deployment"**
2. Choose deployment option: **"M0 Shared"** (Free tier - sufficient for development)
3. Select Cloud Provider:
   - **AWS** (recommended - most regions available)
   - Google Cloud Platform
   - Microsoft Azure
4. Select Region:
   - Choose closest to your location or deployment server
   - Example: `N. Virginia (us-east-1)` for North America
5. Click **"Create Deployment"**

### Step 3.2: Wait for Cluster Creation
⏱️ **Wait 5-10 minutes** while Atlas creates your cluster

You'll see:
```
Creating cluster...
[████████░░░░░░░░░░] 50%
```

Once complete, you'll see a green checkmark.

✓ **Result:** Your cluster is now active and running

---

## Create Database User

### Step 4.1: Navigate to Database Access
1. In left sidebar, click **"Database Access"** (or "Security" → "Database Access")
2. Click **"+ Add New Database User"** button

### Step 4.2: Create User Credentials
1. **Choose Authentication Method:** Select **"Password"**
2. **Username:** Enter `conference_user`
3. **Password:** Enter a strong password (min 8 characters)
   - Example: `P@ssw0rd123!Conference`
   - **Save this password somewhere safe!** (Password Manager)
   - **Do NOT use:** Special characters that need URL encoding if possible
4. **User Privileges:** Select **"Read and write to any database"**
5. Click **"Add User"**

### Step 4.3: Verify User Creation
- You should see the new user in the "Database Access" list
- Status should show as "Active"

✓ **Result:** Database user created with credentials
- Username: `conference_user`
- Password: `your_password_here`

---

## Configure Network Access

### Step 5.1: Whitelist IP Addresses
1. In left sidebar, click **"Network Access"** (or "Security" → "Network Access")
2. Click **"+ Add IP Address"** button

### Step 5.2: Choose IP Whitelist Option

**Option A: For Development (Recommended)**
1. Click **"Add Current IP Address"**
2. Atlas automatically detects your IP
3. Click **"Confirm"**

**Option B: For Deployment Server**
1. Click **"Add a Different IP Address"**
2. Enter your server IP address
3. Click **"Confirm"**

**Option C: Allow All IPs (Testing Only)**
1. Click **"Add IP Address"**
2. Enter: `0.0.0.0/0`
3. Description: `Allow All (Development Only)`
4. Click **"Confirm"**
⚠️ **WARNING:** Never use `0.0.0.0/0` in production!

### Step 5.3: Verify Changes
- Wait for changes to apply (usually instant)
- You'll see a green checkmark when ready

✓ **Result:** IP whitelist configured

---

## Get Connection String

### Step 6.1: Access Connection String
1. Go to **"Databases"** section
2. Find your cluster and click **"Connect"** button
3. Choose **"Drivers"** (for application connection)
4. Select **Language: "Python"**
5. Select **"PyMongo"** driver
6. You'll see the connection string template

### Step 6.2: Copy Connection String
The string will look like:
```
mongodb+srv://conference_user:<password>@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

### Step 6.3: Customize Connection String
Replace placeholders:
- **`<password>`** → Your database password (from Step 4.2)
- **Add database name** → Add `/conference_db?` at the end

**Final Connection String:**
```
mongodb+srv://conference_user:P@ssw0rd123!Conference@cluster0.abc123.mongodb.net/conference_db?retryWrites=true&w=majority
```

✓ **Result:** Connection string ready to use

---

## Configure Application

### Step 7.1: Create .env File
1. In your project root directory, create a file named `.env`
2. Add the following content:

```env
# MongoDB Atlas Configuration
MONGODB_URI=mongodb+srv://conference_user:P@ssw0rd123!Conference@cluster0.abc123.mongodb.net/conference_db?retryWrites=true&w=majority
DATABASE_NAME=conference_db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Server Configuration
HOST=localhost
PORT=5000
```

**Replace:**
- `MONGODB_URI` → Your actual connection string
- `SECRET_KEY` → A random secret key

### Step 7.2: Install Dependencies
Open terminal in project directory:
```bash
pip install -r requirements.txt
```

✓ **Result:** Application configured for Atlas

---

## Test Connection

### Step 8.1: Run Connection Test
Execute the test script:
```bash
python scripts/test_atlas_connection.py
```

### Step 8.2: Expected Output
Success message:
```
✓ MongoDB Atlas connected successfully!
✓ Database: conference_db
✓ Collections created: conferences, sessions, attendees
```

If you see errors:
- Check `.env` file has correct values
- Verify IP is whitelisted in Network Access
- Verify password doesn't have unencoded special characters
- Check internet connection

✓ **Result:** Connection verified and working

---

## Deploy to Production

### Step 9.1: For Heroku Deployment
```bash
heroku login
heroku create your-app-name
heroku config:set MONGODB_URI="your_connection_string"
heroku config:set FLASK_ENV=production
git push heroku main
```

### Step 9.2: For Railway Deployment
```bash
railway login
railway init
railway link
railway up
```

### Step 9.3: For Render Deployment
1. Connect GitHub repository
2. Create new Web Service
3. Add environment variables in Render dashboard
4. Deploy

### Step 9.4: For PythonAnywhere
1. Upload project files
2. Create Web app with Flask
3. Set `MONGODB_URI` in Web app settings
4. Reload web app

✓ **Result:** Application deployed with MongoDB Atlas

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection timeout | Check IP whitelist in Network Access |
| Authentication failed | Verify username and password |
| Database not found | Check connection string has `/conference_db` |
| Special character errors | URL encode special characters in password |
| Slow connection | May need to upgrade from M0 tier |

---

## Security Checklist for Production

- [ ] Use strong password (min 12 characters, mixed case, numbers, symbols)
- [ ] Restrict IP whitelist to production server IP only
- [ ] Create separate users for development and production
- [ ] Enable VPC peering for enhanced security
- [ ] Enable automatic backups
- [ ] Set up monitoring and alerts
- [ ] Store connection string in secure vault
- [ ] Rotate passwords periodically
- [ ] Never commit .env file to version control
- [ ] Use environment variables for all sensitive data

---

## Next Steps

1. ✓ Test application locally
2. ✓ Create production-ready deployment
3. ✓ Set up monitoring
4. ✓ Configure backups
5. ✓ Implement security best practices
