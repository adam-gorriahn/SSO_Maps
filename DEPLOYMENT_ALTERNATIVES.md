# Deployment Alternatives to Render.com

This guide covers various platforms where you can deploy your VizBrowser application. All platforms support Python/Dash applications and provide HTTPS automatically.

## Quick Comparison

| Platform | Free Tier | Ease of Use | Best For |
|----------|-----------|-------------|----------|
| **Render** | ✅ Yes | ⭐⭐⭐⭐⭐ | Beginners, quick setup |
| **Railway** | ✅ Yes (limited) | ⭐⭐⭐⭐⭐ | Modern apps, great DX |
| **Fly.io** | ✅ Yes (generous) | ⭐⭐⭐⭐ | Global distribution |
| **Heroku** | ❌ No (paid only) | ⭐⭐⭐⭐ | Established apps |
| **PythonAnywhere** | ✅ Yes | ⭐⭐⭐ | Python-focused |
| **DigitalOcean App Platform** | ❌ No | ⭐⭐⭐⭐ | Production apps |
| **AWS/GCP/Azure** | ⚠️ Pay-as-you-go | ⭐⭐ | Enterprise, scale |

---

## 1. Railway.app ⭐ Recommended Alternative

**Why Railway?** Modern platform, excellent developer experience, automatic deployments from GitHub.

### Setup Steps:

1. **Go to [railway.app](https://railway.app)** and sign up with GitHub
2. **Create New Project** → "Deploy from GitHub repo"
3. **Select your repository**
4. **Add Environment Variables**:
   - `ADMIN_PASSWORD`: Your secure password
   - `DEBUG_MODE`: `False`
   - `HOST`: `0.0.0.0`
   - `PORT`: `8050` (Railway sets this automatically via `$PORT`)
5. **Railway auto-detects** Python and deploys automatically

### Pros:
- ✅ Free tier with $5 credit/month
- ✅ Automatic HTTPS
- ✅ Great UI and logs
- ✅ Auto-deploys on git push
- ✅ Simple pricing

### Cons:
- ⚠️ Free tier limited (sleeps after inactivity)
- ⚠️ Need to add payment method for production

### Pricing:
- Free: $5 credit/month (good for testing)
- Paid: $5-20/month for always-on service

---

## 2. Fly.io

**Why Fly.io?** Generous free tier, global edge deployment, great for performance.

### Setup Steps:

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**:
   ```bash
   fly auth login
   ```

3. **Create app**:
   ```bash
   fly launch
   ```

4. **Create `fly.toml`**:
   ```toml
   app = "your-app-name"
   primary_region = "iad"

   [build]
     builder = "paketobuildpacks/builder:base"

   [http_service]
     internal_port = 8050
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0

   [[services]]
     http_checks = []
     internal_port = 8050
     processes = ["app"]
     protocol = "tcp"
     script_checks = []
   ```

5. **Set secrets**:
   ```bash
   fly secrets set ADMIN_PASSWORD=your_password
   fly secrets set DEBUG_MODE=False
   ```

6. **Deploy**:
   ```bash
   fly deploy
   ```

### Pros:
- ✅ Generous free tier (3 shared VMs)
- ✅ Global edge network
- ✅ Great performance
- ✅ Auto-scaling

### Cons:
- ⚠️ Requires CLI setup
- ⚠️ More complex than Render/Railway

### Pricing:
- Free: 3 shared VMs, 160GB outbound data
- Paid: $1.94/month per VM

---

## 3. Heroku

**Why Heroku?** Established platform, reliable, but no free tier anymore.

### Setup Steps:

1. **Install Heroku CLI**:
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login**:
   ```bash
   heroku login
   ```

3. **Create app**:
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set ADMIN_PASSWORD=your_password
   heroku config:set DEBUG_MODE=False
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

### Pros:
- ✅ Very reliable
- ✅ Great documentation
- ✅ Add-ons ecosystem
- ✅ Established platform

### Cons:
- ❌ No free tier (removed in 2022)
- ⚠️ More expensive ($5-7/month minimum)
- ⚠️ Requires credit card

### Pricing:
- Eco Dyno: $5/month (sleeps after 30min inactivity)
- Basic Dyno: $7/month (always on)

---

## 4. PythonAnywhere

**Why PythonAnywhere?** Python-focused, great for Python apps, simple setup.

### Setup Steps:

1. **Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)**
2. **Upload your code** via Files tab or Git
3. **Create Web App**:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" → Python 3.11
4. **Set up WSGI file** to point to your app
5. **Set environment variables** in Web app settings
6. **Reload web app**

### Pros:
- ✅ Free tier available
- ✅ Python-focused
- ✅ Built-in console/IDE
- ✅ Simple for Python apps

### Cons:
- ⚠️ Free tier has limitations (1 web app, limited CPU)
- ⚠️ Less modern than other platforms
- ⚠️ Manual setup required

### Pricing:
- Beginner: Free (limited)
- Hacker: $5/month
- Web Dev: $12/month

---

## 5. DigitalOcean App Platform

**Why DigitalOcean?** Good balance of features and price, reliable infrastructure.

### Setup Steps:

1. **Go to [digitalocean.com](https://www.digitalocean.com/products/app-platform)**
2. **Create App** → "GitHub" → Select repository
3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python app.py`
   - Environment Variables: Set `ADMIN_PASSWORD`, etc.
4. **Deploy**

### Pros:
- ✅ Reliable infrastructure
- ✅ Good pricing
- ✅ Auto-scaling
- ✅ Good documentation

### Cons:
- ❌ No free tier
- ⚠️ Minimum $5/month
- ⚠️ Requires credit card

### Pricing:
- Basic: $5/month
- Professional: $12/month+

---

## 6. Google Cloud Run

**Why Cloud Run?** Pay only for what you use, serverless, scales to zero.

### Setup Steps:

1. **Install gcloud CLI**
2. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "app.py"]
   ```

3. **Deploy**:
   ```bash
   gcloud run deploy --source .
   ```

4. **Set environment variables** in Cloud Console

### Pros:
- ✅ Pay only for requests
- ✅ Scales to zero
- ✅ Serverless
- ✅ Generous free tier

### Cons:
- ⚠️ More complex setup
- ⚠️ Requires Docker knowledge
- ⚠️ Cold starts possible

### Pricing:
- Free: 2 million requests/month
- Paid: $0.40 per million requests

---

## 7. AWS Elastic Beanstalk / Lightsail

**Why AWS?** Enterprise-grade, highly scalable, many services.

### Setup Steps:

1. **AWS Elastic Beanstalk** (Easier):
   - Go to AWS Console → Elastic Beanstalk
   - Create application → Python platform
   - Upload code or connect Git
   - Set environment variables

2. **AWS Lightsail** (Simpler):
   - Create instance → Python app
   - Deploy via Git or upload
   - Set environment variables

### Pros:
- ✅ Enterprise-grade
- ✅ Highly scalable
- ✅ Many services
- ✅ Free tier available (limited)

### Cons:
- ⚠️ Complex setup
- ⚠️ Steep learning curve
- ⚠️ Can be expensive if not careful

### Pricing:
- Free tier: Limited (12 months)
- Lightsail: $3.50/month+
- Beanstalk: Pay for EC2 resources

---

## 8. Azure App Service

**Why Azure?** Microsoft ecosystem, good integration, enterprise features.

### Setup Steps:

1. **Azure Portal** → Create App Service
2. **Configure**:
   - Runtime: Python 3.11
   - Deployment: GitHub
3. **Set Application Settings** (environment variables)
4. **Deploy**

### Pros:
- ✅ Enterprise features
- ✅ Good Microsoft integration
- ✅ Auto-scaling
- ✅ Free tier available

### Cons:
- ⚠️ Complex interface
- ⚠️ Can be expensive
- ⚠️ Steeper learning curve

### Pricing:
- Free: Limited (shared)
- Basic: $13/month+
- Standard: $50/month+

---

## Recommendation Summary

### For Beginners:
1. **Railway** - Easiest alternative to Render
2. **Render** - Still the simplest overall

### For Production:
1. **Fly.io** - Best free tier, great performance
2. **DigitalOcean** - Good balance
3. **Heroku** - Most established

### For Cost-Conscious:
1. **Fly.io** - Generous free tier
2. **Google Cloud Run** - Pay per use
3. **Railway** - $5 credit/month

### For Enterprise:
1. **AWS** - Most services
2. **Azure** - Microsoft ecosystem
3. **Google Cloud** - Data/AI focus

---

## Quick Setup Commands

### Railway
```bash
# Just connect GitHub repo in web UI - no CLI needed!
```

### Fly.io
```bash
fly launch
fly secrets set ADMIN_PASSWORD=your_password
fly deploy
```

### Heroku
```bash
heroku create your-app
heroku config:set ADMIN_PASSWORD=your_password
git push heroku main
```

### DigitalOcean
```bash
# Use web UI - connect GitHub and deploy
```

---

## Environment Variables for All Platforms

Set these on any platform:
- `ADMIN_PASSWORD`: Your secure password (required)
- `DEBUG_MODE`: `False` (required)
- `HOST`: `0.0.0.0` (usually required)
- `PORT`: Check platform docs (some auto-set via `$PORT`)

---

## Need Help?

- **Railway**: [docs.railway.app](https://docs.railway.app)
- **Fly.io**: [fly.io/docs](https://fly.io/docs)
- **Heroku**: [devcenter.heroku.com](https://devcenter.heroku.com)
- **DigitalOcean**: [docs.digitalocean.com](https://docs.digitalocean.com)

