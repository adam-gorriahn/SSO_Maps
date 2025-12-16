# Agentic Dataverse Visualizer

An interactive web application for visualizing industrial assets, KPIs, and 3D models with geospatial mapping capabilities.

## Features

- 🗺️ **Geospatial Navigator** - Interactive map view of industrial assets and locations
- 📊 **KPIs Navigator** - Real-time sustainability metrics and performance indicators
- 🏭 **Shopfloor Navigator** - 3D visualization of industrial sites and equipment
- 🔧 **Asset Navigator** - Detailed view of data layers, models, and simulations
- 🔒 **Password Protection** - Secure access control for public deployments

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd VizBrowser
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

### Development Mode (No Password - Default)

Simply run:
```bash
python app.py
```

The app will be available at `http://127.0.0.1:8050` without password protection.

### With Password Protection (Local Testing)

If you want to test password protection locally, set the password:
```bash
export ADMIN_PASSWORD=test_password
python app.py
```

Or set it inline:
```bash
ADMIN_PASSWORD=test_password python app.py
```

**Note:** When running locally (not in a cloud environment), the app defaults to no password protection unless you explicitly set `ADMIN_PASSWORD`. This makes local development easier.

### Using the Deployment Script

```bash
python deploy.py --mode dev
```

## Deployment

Deploy to a public domain with password protection.

### Quick Deploy (Render)

1. Push code to GitHub
2. Create a new Web Service on [Render](https://render.com)
3. Connect your repository
4. Set environment variable: `ADMIN_PASSWORD=your_secure_password`
5. Deploy!

### Other Deployment Options

See [DEPLOYMENT_ALTERNATIVES.md](DEPLOYMENT_ALTERNATIVES.md) for comprehensive guides on:
- **Railway** - Modern, easy alternative to Render
- **Fly.io** - Generous free tier, great performance
- **Heroku** - Established platform (paid)
- **PythonAnywhere** - Python-focused hosting
- **DigitalOcean** - Reliable infrastructure
- **AWS/Google Cloud/Azure** - Enterprise options

For detailed Render steps, see [QUICK_START.md](QUICK_START.md).

### Updating Your Deployment

**Render automatically deploys when you push to GitHub!**

Simply commit and push your changes:
```bash
git add .
git commit -m "Your update description"
git push
```

Render will automatically detect the push and deploy your changes in 3-5 minutes. See [UPDATE_DEPLOYMENT.md](UPDATE_DEPLOYMENT.md) for detailed instructions.

## Project Structure

```
VizBrowser/
├── app.py              # Main application entry point
├── callbacks.py        # Dash callbacks and interactivity
├── components.py       # UI components
├── constants.py        # Configuration and constants
├── data_loader.py      # Data loading and simulation
├── styles.py           # Styling utilities
├── auth.py             # Password authentication
├── assets/             # Static assets (images, models)
└── requirements.txt    # Python dependencies
```

## Usage

1. **Navigate Views**: Use the sidebar to switch between different navigators
2. **Interact with Map**: Click on markers to view asset details
3. **Explore 3D Models**: Use controls to pan, zoom, and rotate 3D views
4. **View KPIs**: Monitor real-time metrics and alerts
5. **Browse Assets**: Select assets from the tree to view detailed information

## Requirements

- dash
- plotly
- numpy
- dash-vtk
- dash-leaflet
- pyvista
- pandas
- scikit-learn
- scipy

## License

This project is for internal use.

## Memory Optimization

The application has been optimized for memory efficiency, especially for Render.com's free tier (512MB limit). The 3D mesh loading has been optimized with:

- **Lazy Loading**: Mesh is only loaded when the 3D view is actually displayed (not on app startup)
- **Memory-Efficient Conversion**: Mesh data is converted efficiently and cleared from memory immediately
- **Aggressive Decimation**: Default settings reduce mesh size by 95% to fit within 512MB
- **Cache Clearing**: Mesh cache is cleared immediately after conversion to free memory

**Default settings (optimized for Render.com 512MB):**
- `MESH_DECIMATION_FACTOR=0.95` (95% reduction)
- `MAX_MESH_FACES=15000` (maximum faces)

**If you still experience memory issues on Render.com:**

**Option 1 - Disable 3D view entirely:**
- `DISABLE_3D_VIEW=true` (completely disables 3D visualization)

**Option 2 - More aggressive reduction:**
- `MESH_DECIMATION_FACTOR=0.98` (98% reduction)
- `MAX_MESH_FACES=10000` (fewer faces)

**Option 3 - Upgrade plan:**
Upgrade to a Render.com plan with 1GB+ memory for better performance.

**For higher memory limits (1GB+):**
You can use higher quality settings:
- `MESH_DECIMATION_FACTOR=0.85` (85% reduction)
- `MAX_MESH_FACES=30000` (more faces)

## Support

For deployment issues, see [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section.

