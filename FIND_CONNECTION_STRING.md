# Where to Find Your MongoDB Atlas Connection String

## Visual Step-by-Step Guide

### Step 1: Log In to MongoDB Atlas
1. Go to https://cloud.mongodb.com
2. Enter your email and password
3. Click "Sign In"
4. You should see your project dashboard

### Step 2: Navigate to Your Cluster
1. Look at the left sidebar
2. Click on **"Databases"** or **"Clusters"**
3. You should see your cluster listed (e.g., "Cluster0")
4. Click the **"Connect"** button on your cluster

### Step 3: Select "Drivers"
In the connection dialog that opens:
1. You'll see three options at the top:
   - Shell (Command line)
   - Compass (Desktop app)
   - **Drivers** ← Click this
2. Click on **"Drivers"**

### Step 4: Select Python
1. You'll see "Select your driver" dropdown
2. Choose **"Python"**
3. Select version (latest is fine)

### Step 5: View Connection String
You'll see a box with the connection string that looks like:

```
mongodb+srv://<username>:<password>@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

### Step 6: Copy the Connection String
1. Click the **"Copy"** button (icon on right side)
2. The string is now in your clipboard

---

## What the Connection String Looks Like

**Before customization:**
```
mongodb+srv://<username>:<password>@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

**After you replace placeholders:**
```
mongodb+srv://conference_user:MyP@ssw0rd123@cluster0.abc123.mongodb.net/conference_db?retryWrites=true&w=majority
```

---

## Connection String Placeholders to Replace

| Placeholder | Replace With | Example |
|------------|--------------|---------|
| `<username>` | Your database user | `conference_user` |
| `<password>` | Your database password | `MyP@ssw0rd123` |
| `cluster0.abc123` | Your cluster name | `cluster0.7hk9x` |
| Add `/conference_db` | Database name | At end before `?` |

---

## Step-by-Step Replacement Example

**Original string from Atlas:**
```
mongodb+srv://<username>:<password>@cluster0.7hk9x.mongodb.net/?retryWrites=true&w=majority
```

**Step 1: Replace `<username>`**
```
mongodb+srv://conference_user:<password>@cluster0.7hk9x.mongodb.net/?retryWrites=true&w=majority
```

**Step 2: Replace `<password>`**
```
mongodb+srv://conference_user:MyP@ssw0rd123@cluster0.7hk9x.mongodb.net/?retryWrites=true&w=majority
```

**Step 3: Add database name before `?`**
```
mongodb+srv://conference_user:MyP@ssw0rd123@cluster0.7hk9x.mongodb.net/conference_db?retryWrites=true&w=majority
```

**Final connection string:**
```
mongodb+srv://conference_user:MyP@ssw0rd123@cluster0.7hk9x.mongodb.net/conference_db?retryWrites=true&w=majority
```

---

## Where Each Part Goes in Your .env File

Your `.env` file should look like:

```env
MONGODB_URI=mongodb+srv://conference_user:MyP@ssw0rd123@cluster0.7hk9x.mongodb.net/conference_db?retryWrites=true&w=majority
DATABASE_NAME=conference_db
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
HOST=localhost
PORT=5000
```

---

## If You Can't Find the Connection String

### Problem 1: Can't see "Clusters" in sidebar
**Solution:**
- Go to https://cloud.mongodb.com
- Check you're in the correct project
- Look for "Databases" in left menu instead

### Problem 2: "Connect" button is grayed out
**Solution:**
- Your cluster might still be loading
- Wait 5-10 minutes and refresh
- Check that your IP is whitelisted

### Problem 3: Connection dialog shows "Shell" instead of "Drivers"
**Solution:**
- You clicked the wrong tab
- Click the **"Drivers"** tab at the top

### Problem 4: Can't find cluster in list
**Solution:**
- Make sure you're in the correct organization
- Check project dropdown in top-left
- Create a new cluster if none exist

---

## Connection String Components Explained

```
mongodb+srv://conference_user:MyP@ssw0rd123@cluster0.7hk9x.mongodb.net/conference_db?retryWrites=true&w=majority
│              │                 │                │                  │              │
Protocol       Username          Password        Cluster URL        Database       Options
```

- **Protocol:** `mongodb+srv://` (always for Atlas)
- **Username:** `conference_user` (database user)
- **Password:** `MyP@ssw0rd123` (database password)
- **Cluster URL:** `cluster0.7hk9x.mongodb.net` (Atlas cluster)
- **Database:** `/conference_db` (your database name)
- **Options:** `?retryWrites=true&w=majority` (connection settings)

---

## Security Notes

⚠️ **IMPORTANT:**
- Never share your connection string publicly
- Don't commit it to GitHub
- Use `.env` file (added to `.gitignore`)
- In production, store in environment variables
- Rotate passwords periodically

---

## Next Steps

1. Copy your connection string from Atlas
2. Replace placeholders with your actual values
3. Paste into `.env` file
4. Run: `python scripts/test_atlas_connection.py`
5. Verify connection is successful
