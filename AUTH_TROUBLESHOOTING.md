# Authentication Troubleshooting Guide

## Problem: Login Window Not Appearing on Render.com

If the login/password prompt doesn't appear when accessing your deployed app, follow these steps:

## Quick Fix

1. **Verify ADMIN_PASSWORD is set** in Render dashboard:
   - Go to your Render service → Environment tab
   - Check that `ADMIN_PASSWORD` is set with a value
   - Make sure there are no extra spaces or quotes

2. **Check the logs** in Render dashboard:
   - Look for: `✅ Authentication enabled (ADMIN_PASSWORD is set)`
   - If you see: `ℹ️ Authentication disabled` → ADMIN_PASSWORD is not set correctly

3. **Redeploy** after setting environment variables

## Step-by-Step Fix

### 1. Set Environment Variable in Render

1. Go to [render.com](https://render.com) dashboard
2. Click on your web service
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Set:
   - **Key**: `ADMIN_PASSWORD`
   - **Value**: `YourSecurePassword123!` (use a strong password)
6. Click **"Save Changes"**
7. Render will automatically redeploy

### 2. Verify in Logs

After deployment, check the logs:
- Look for: `✅ Authentication enabled (ADMIN_PASSWORD is set)`
- This confirms authentication is active

### 3. Test the Login

1. Open your app URL in a browser
2. You should see a browser login prompt (not a custom form)
3. Enter:
   - **Username**: (can be anything or leave blank)
   - **Password**: The password you set in `ADMIN_PASSWORD`

## Common Issues

### Issue 1: No Login Prompt Appears

**Cause**: `ADMIN_PASSWORD` environment variable is not set or not detected

**Solution**:
1. Double-check the environment variable name (must be exactly `ADMIN_PASSWORD`)
2. Make sure there are no spaces: `ADMIN_PASSWORD=password` (not `ADMIN_PASSWORD = password`)
3. Redeploy after setting the variable
4. Check logs to confirm auth is enabled

### Issue 2: "Authentication disabled" in Logs

**Cause**: The app thinks it's running locally

**Solution**:
- Make sure `ADMIN_PASSWORD` is set in Render dashboard
- The app will enable auth automatically when `ADMIN_PASSWORD` is set

### Issue 3: Login Prompt Appears But Password Doesn't Work

**Cause**: Wrong password or password not set correctly

**Solution**:
1. Check the exact value in Render environment variables
2. Make sure there are no extra characters
3. Try clearing browser cache and cookies
4. Try incognito/private browsing mode

### Issue 4: Works Locally But Not on Render

**Cause**: Environment variable not set on Render

**Solution**:
- Local: Uses default 'admin' password if not set
- Render: Requires `ADMIN_PASSWORD` to be explicitly set
- Set `ADMIN_PASSWORD` in Render dashboard

## Verification Checklist

- [ ] `ADMIN_PASSWORD` is set in Render environment variables
- [ ] No extra spaces in the environment variable value
- [ ] App has been redeployed after setting the variable
- [ ] Logs show: `✅ Authentication enabled`
- [ ] Browser shows login prompt when accessing the URL
- [ ] Password works when entered

## Testing Locally

To test authentication locally:

```bash
export ADMIN_PASSWORD=test_password
export DEBUG_MODE=False
python app.py
```

Then visit `http://127.0.0.1:8050` - you should see a login prompt.

## How Authentication Works

1. **Basic HTTP Authentication**: Uses browser's built-in login prompt
2. **Session-based**: Once authenticated, session remembers you
3. **Automatic**: Enabled when `ADMIN_PASSWORD` environment variable is set
4. **Secure**: Password is transmitted over HTTPS (automatic on Render)

## Still Not Working?

1. **Check Render logs** for any errors
2. **Verify environment variable** is actually set (check in Render dashboard)
3. **Try a simple password** first (like `test123`) to rule out special character issues
4. **Clear browser cache** completely
5. **Try different browser** or incognito mode
6. **Check if HTTPS is working** (Render provides this automatically)

## Debug Mode

To see what's happening, check the application logs in Render:

- Look for authentication-related messages
- Check for any errors during startup
- Verify environment variables are loaded

## Security Note

- Never commit passwords to git
- Always use environment variables
- Use strong passwords in production
- Rotate passwords periodically

