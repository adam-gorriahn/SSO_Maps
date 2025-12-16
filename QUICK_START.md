# Quick Start - Deploy with Password Protection

## Fastest Way to Deploy (Render - 5 minutes)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [render.com](https://render.com) → Sign up/Login
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
   - **Environment Variables** (Advanced → Environment):
     - `ADMIN_PASSWORD`: `YourSecurePassword123!`
     - `DEBUG_MODE`: `False`
     - `HOST`: `0.0.0.0`
     - `PORT`: `8050`
   - Click "Create Web Service"
   - Wait 5-10 minutes

3. **Access Your Site**:
   - URL: `https://your-app-name.onrender.com`
   - Username: (any, can be blank)
   - Password: `YourSecurePassword123!`

## Local Testing with Password

1. **Set environment variable**:
   ```bash
   export ADMIN_PASSWORD=test_password
   export DEBUG_MODE=False
   python app.py
   ```

2. **Or use .env file** (requires python-dotenv):
   ```bash
   pip install python-dotenv
   ```
   Create `.env`:
   ```
   ADMIN_PASSWORD=test_password
   DEBUG_MODE=False
   ```
   Update `app.py` to load .env (add at top):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Important Notes

- **Password is required in production** - Set `ADMIN_PASSWORD` environment variable
- **Default password 'admin' only works in DEBUG_MODE=True** (local development)
- **Never commit passwords to git** - Use environment variables only
- **HTTPS is automatic** on all deployment platforms

For detailed instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

