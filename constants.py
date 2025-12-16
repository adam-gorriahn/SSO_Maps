"""
Constants and configuration for the Agentic Dataverse Visualizer
"""
import os

# --- File Paths ---
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FESTO_PLY_PATH = os.path.join(ASSETS_DIR, "festo_new_cleaned.ply")
FESTO_OBJ_PATH = os.path.join(ASSETS_DIR, "festo.obj")
GARCHING_OBJ_PATH = os.path.join(ASSETS_DIR, "garching_cleaned.obj")
GARCHING_OPTIMIZED_PATH = os.path.join(ASSETS_DIR, "garching_optimized.obj")

# --- App Configuration ---
APP_TITLE = "Agentic Dataverse Visualizer"
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8050))

# --- Data Configuration ---
KPI_DAYS = 30
POINT_CLOUD_MAX_POINTS = 100000
SPHERE_ANIMATION_FRAMES = 12
SPHERE_ANIMATION_INTERVAL = 120

# --- 3D Mesh Configuration ---
# Mesh decimation factor (0.0 = no reduction, 1.0 = maximum reduction)
# Lower values = higher quality but more memory
# For Render.com free tier (512MB), use 0.95 for very aggressive memory reduction
# Default is now 0.95 (95% reduction) to fit within 512MB limit
MESH_DECIMATION_FACTOR = float(os.getenv('MESH_DECIMATION_FACTOR', '0.95'))
# Maximum number of faces for Garching mesh (0 = no limit)
# Default reduced to 15000 for 512MB environments (Render.com free tier)
MAX_MESH_FACES = int(os.getenv('MAX_MESH_FACES', '15000'))
# Disable 3D view entirely if memory is too constrained (set to 'true' to disable)
DISABLE_3D_VIEW = os.getenv('DISABLE_3D_VIEW', 'false').lower() == 'true'

# --- Map Configuration ---
MAP_CENTER = [48.265132904052734, 11.661945343017578]  # Siemens Technology Center Garching
MAP_ZOOM = 15
FAST_TILE_URL = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
ALTERNATE_TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

# --- KPI Configuration ---
KPI_LABELS = {
    'energy_spend': 'Energy Spend',
    'carbon_intensity': 'Carbon Intensity',
    'oee': 'OEE',
    'compressed_air': 'Compressed Air',
    'water_usage': 'Water Usage'
}

KPI_UNITS = {
    'energy_spend': 'kWh',
    'carbon_intensity': 'kgCO₂/kWh',
    'oee': '%',
    'compressed_air': 'Nm³',
    'water_usage': 'm³'
}

# --- KPI Alert Thresholds ---
KPI_THRESHOLDS = {
    'energy_spend': {
        'warning': 28.0,  # kWh - above this is warning
        'critical': 32.0  # kWh - above this is critical
    },
    'carbon_intensity': {
        'warning': 0.35,  # kgCO₂/kWh - above this is warning
        'critical': 0.40  # kgCO₂/kWh - above this is critical
    },
    'oee': {
        'warning': 0.70,  # 70% - below this is warning
        'critical': 0.65  # 65% - below this is critical
    },
    'compressed_air': {
        'warning': 70.0,  # Nm³ - above this is warning
        'critical': 80.0  # Nm³ - above this is critical
    },
    'water_usage': {
        'warning': 11.0,  # m³ - above this is warning
        'critical': 13.0  # m³ - above this is critical
    }
}

# --- KPI Status Colors ---
KPI_STATUS_COLORS = {
    'normal': '#4caf50',    # Green
    'warning': '#ffb300',   # Orange/Yellow
    'critical': '#e53935'   # Red
}

KPI_STATUS_ICONS = {
    'normal': '✅',
    'warning': '⚠️',
    'critical': '🚨'
}

# --- Export & Share Configuration ---
EXPORT_FORMATS = {
    'csv': 'CSV Data',
    'json': 'JSON Data',
    'png': 'PNG Screenshot',
    'pdf': 'PDF Report'
}

SHARE_OPTIONS = {
    'view_state': 'Current View State',
    'kpi_data': 'KPI Data',
    'screenshot': 'Screenshot',
    'link': 'Shareable Link'
}

# --- Export Settings ---
EXPORT_FILENAME_PREFIX = "VizBrowser_Export"
EXPORT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# --- Component Metadata ---
COMPONENTS = [
    {"name": "Valve 22", "pressure": 4.3, "status": "Active", "last_service": "2024-12-01"},
    {"name": "Pump 7", "pressure": 3.8, "status": "Idle", "last_service": "2024-10-15"},
    {"name": "Sensor X3", "pressure": 4.1, "status": "Active", "last_service": "2024-11-20"},
    {"name": "Pipe A", "pressure": 4.0, "status": "Fault", "last_service": "2024-09-05"},
    {"name": "Valve 23", "pressure": 4.2, "status": "Active", "last_service": "2024-12-01"},
    {"name": "Pump 8", "pressure": 3.9, "status": "Idle", "last_service": "2024-10-15"},
    {"name": "Sensor Y4", "pressure": 4.4, "status": "Active", "last_service": "2024-11-20"},
    {"name": "Pipe B", "pressure": 4.1, "status": "Fault", "last_service": "2024-09-05"},
]

# --- Siemens-style Theme ---
SIEMENS_BG = "#f8fafc"
SIEMENS_BG_DARK = "#1a222c"
SIEMENS_CARD = "#ffffff"
SIEMENS_CARD_DARK = "#232b36"
SIEMENS_ACCENT = "#e3eefa"
SIEMENS_ACCENT_DARK = "#2a425a"
SIEMENS_SHADOW = "0 2px 8px rgba(44, 62, 80, 0.07)"
SIEMENS_FONT = "'Open Sans', 'Segoe UI', 'Arial', sans-serif"
SIEMENS_BLUE = "#0070b8"
SIEMENS_BLUE_DARK = "#4fc3f7"
SIEMENS_DIVIDER = "#e0e6ed"
SIEMENS_DIVIDER_DARK = "#2a425a"
SIEMENS_STATUS = {"Active": "#4caf50", "Idle": "#ffb300", "Fault": "#e53935"}

# --- Asset Tree Configuration ---
LAYERED_ASSETS = [
    {
        "layer": "Simulation Layer",
        "color": SIEMENS_ACCENT,
        "items": [
            {"key": "sim_flow", "name": "Material Flow Simulation"},
            {"key": "sim_resource", "name": "Resource Utilization Simulation"},
        ]
    },
    {
        "layer": "Model Layer",
        "color": "#f0f7fa",
        "items": [
            {"key": "mesh", "name": "Digital Twin Mesh"},
        ]
    },
    {
        "layer": "Real-World Data Layer",
        "color": SIEMENS_BG,
        "items": [
            {"key": "image", "name": "2D Images"},
            {"key": "pointcloud", "name": "3D Scan (Point Cloud)"},
        ]
    }
]

# --- Asset Name Mapping ---
ASSET_NAME_MAP = {
    "sim_flow": "Material Flow Plan",
    "sim_resource": "Resource Utilization Model",
    "mesh": "Digital Twin Mesh",
    "image": "2D Images",
    "pointcloud": "3D Scan (Point Cloud)",
}

# --- Sidebar Navigation Configuration ---
SIDEBAR_NAVIGATION = [
    {
        "id": "geospatial",
        "label": "Geospatial Navigator",
        "icon": "🗺️",
        "description": "Interactive map view"
    },
    {
        "id": "kpi",
        "label": "KPIs Navigator",
        "icon": "📊",
        "description": "Sustainability metrics"
    },
    {
        "id": "3d",
        "label": "Shopfloor Navigator",
        "icon": "🏭",
        "description": "3D Shopfloor view"
    },
    {
        "id": "assets",
        "label": "Asset Navigator",
        "icon": "🔧",
        "description": "Data view for selected model"
    }
]
