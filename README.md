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

### Development Mode (No Password)

```bash
python app.py
```

The app will be available at `http://127.0.0.1:8050`

### With Password Protection

Set environment variables:
```bash
export ADMIN_PASSWORD=your_password
export DEBUG_MODE=False
python app.py
```

Or use the deployment script:
```bash
python deploy.py --mode dev
```

## Deployment

Deploy to a public domain with password protection. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Quick Deploy (Render)

1. Push code to GitHub
2. Create a new Web Service on [Render](https://render.com)
3. Connect your repository
4. Set environment variable: `ADMIN_PASSWORD=your_secure_password`
5. Deploy!

For more options and detailed steps, see [QUICK_START.md](QUICK_START.md) or [DEPLOYMENT.md](DEPLOYMENT.md).

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

## Support

For deployment issues, see [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section.

