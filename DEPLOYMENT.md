# Deployment Guide - VizBrowser

This guide will help you deploy your VizBrowser application to a public domain with password protection.

## Prerequisites

- A GitHub account
- A Render account (free tier available) or Heroku account
- Your code pushed to a GitHub repository

## Option 1: Deploy to Render (Recommended)

Render is a modern platform that offers a free tier and is easy to use.

### Step 1: Push Your Code to GitHub

1. Initialize a git repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Create a new repository on GitHub and push your code:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `vizbrowser` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free (or choose a paid plan)

5. **Set Environment Variables** (click "Advanced" → "Environment Variables"):
   - `ADMIN_PASSWORD`: Set a strong password (e.g., `MySecurePassword123!`)
   - `HOST`: `0.0.0.0`
   - `PORT`: `8050` (Render will set this automatically, but include it)
   - `DEBUG_MODE`: `False`
   - `SESSION_SECRET_KEY`: Leave blank (will be auto-generated)

6. Click "Create Web Service"
7. Wait for deployment (usually 5-10 minutes)
8. Your app will be available at: `https://your-app-name.onrender.com`

### Step 3: Access Your Application

When you visit your deployed URL, you'll be prompted for a password:
- **Username**: Any username (can be left blank or use "admin")
- **Password**: The password you set in `ADMIN_PASSWORD` environment variable

## Option 2: Deploy to Heroku

### Step 1: Install Heroku CLI

Download and install from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

### Step 2: Login and Create App

```bash
heroku login
heroku create your-app-name
```

### Step 3: Set Environment Variables

```bash
heroku config:set ADMIN_PASSWORD=your_secure_password_here
heroku config:set DEBUG_MODE=False
heroku config:set HOST=0.0.0.0
```

### Step 4: Deploy

```bash
git push heroku main
```

Your app will be available at: `https://your-app-name.herokuapp.com`

## Option 3: Deploy to Railway

1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables:
   - `ADMIN_PASSWORD`: Your secure password
   - `DEBUG_MODE`: `False`
5. Railway will automatically detect and deploy your app

## Option 4: Deploy to DigitalOcean App Platform

1. Go to [digitalocean.com](https://www.digitalocean.com/products/app-platform)
2. Create a new app from GitHub
3. Configure build and run commands
4. Set environment variables
5. Deploy

## Local Testing with Password Protection

To test password protection locally:

1. Create a `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set:
   ```
   ADMIN_PASSWORD=test_password
   DEBUG_MODE=False
   ```

3. Install python-dotenv (if not already installed):
   ```bash
   pip install python-dotenv
   ```

4. Update `app.py` to load `.env` file (optional, for local development):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

5. Run the app:
   ```bash
   python app.py
   ```

## Security Best Practices

1. **Use a Strong Password**: Set a complex password in `ADMIN_PASSWORD`
2. **Use HTTPS**: All deployment platforms provide HTTPS by default
3. **Rotate Passwords**: Change `ADMIN_PASSWORD` periodically
4. **Environment Variables**: Never commit passwords to git
5. **Session Security**: `SESSION_SECRET_KEY` should be unique and secret

## Troubleshooting

### App won't start
- Check that all dependencies are in `requirements.txt`
- Verify environment variables are set correctly
- Check build logs in your deployment platform

### Password not working
- Verify `ADMIN_PASSWORD` is set correctly in environment variables
- Clear browser cache and cookies
- Try a different browser or incognito mode

### Static assets not loading
- Ensure `assets/` folder is included in your git repository
- Check that file paths are correct

## Custom Domain (Optional)

Most platforms allow you to add a custom domain:

1. **Render**: Settings → Custom Domain
2. **Heroku**: Settings → Domains
3. **Railway**: Settings → Networking

After adding a custom domain, you may need to configure DNS records as instructed by your platform.

## Updating Your Deployment

To update your deployed app:

1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. Your platform will automatically redeploy (or trigger a manual redeploy)

## Support

For platform-specific issues:
- **Render**: [render.com/docs](https://render.com/docs)
- **Heroku**: [devcenter.heroku.com](https://devcenter.heroku.com)
- **Railway**: [docs.railway.app](https://docs.railway.app)

