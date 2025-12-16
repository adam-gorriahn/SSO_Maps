"""
Optimized Agentic Dataverse Visualizer with Sidebar Navigation
A streamlined version with improved structure, performance, and navigation.
"""
import os
import dash
from dash import html, dcc
import numpy as np

# Import our modular components
from constants import APP_TITLE, DEBUG_MODE, HOST, PORT, KPI_DAYS, KPI_LABELS, SIEMENS_BLUE
from data_loader import simulate_kpi, get_latest_kpi_snapshot
from components import (
    build_asset_tree, build_kpi_cards, build_geospatial_map, 
    build_3d_controls, build_garching_site_view, build_sidebar,
    build_export_modal
)
import dash_vtk
from styles import get_card_style, get_section_style, get_title_style, get_subtitle_style
from callbacks  import register_callbacks
from auth import init_auth

# --- App Initialization ---
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = APP_TITLE

# Initialize password authentication
# Enable auth if:
# 1. ADMIN_PASSWORD is explicitly set via environment variable, OR
# 2. Running in production (cloud environment detected)
# For local testing without ADMIN_PASSWORD set, auth is disabled by default
admin_password_explicitly_set = os.getenv('ADMIN_PASSWORD') is not None
is_cloud_env = os.getenv('RENDER') is not None or os.getenv('DYNO') is not None or os.getenv('RAILWAY_ENVIRONMENT') is not None
enable_auth = admin_password_explicitly_set or (is_cloud_env and not DEBUG_MODE)
if enable_auth:
    app = init_auth(app)

# Add custom CSS for animations and improved UX
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            /* Smooth hover effects for all buttons */
            button:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }
            
            /* Loading state for buttons */
            .loading {
                opacity: 0.7;
                pointer-events: none;
            }
            
            /* Smooth transitions for cards */
            .card-hover:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# --- Data Setup ---
days = np.arange(1, KPI_DAYS + 1)
kpi_data = simulate_kpi(seed=42)
snapshot_kpi = get_latest_kpi_snapshot(kpi_data)

# --- App Layout ---
app.layout = html.Div([
    # Sidebar
    build_sidebar(),
    
    # Floating Toggle Button (always visible)
    html.Button("☰", id="floating-sidebar-toggle", n_clicks=0, style={
        "position": "fixed", "top": "20px", "left": "20px", "zIndex": "1001",
        "background": "rgba(255, 255, 255, 0.9)", "border": f"2px solid {SIEMENS_BLUE}", 
        "fontSize": "1.5rem", "color": SIEMENS_BLUE, "cursor": "pointer", 
        "padding": "12px", "borderRadius": "8px", "minWidth": "48px", "minHeight": "48px",
        "display": "flex", "alignItems": "center", "justifyContent": "center",
        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.15)", "fontWeight": "bold"
    }),
    
    # Main Content Area
    html.Div([
        # Store components
        dcc.Store(id="selected-asset-key"),
        dcc.Store(id="clicked-shopfloor", data=None),
        dcc.Store(id="garching-selected-part", data=None),
        dcc.Store(id="garching-bounds"),
        dcc.Store(id="sidebar-collapsed", data=False),  # False = sidebar visible, True = sidebar hidden
        dcc.Store(id="view-visibility", data={"geospatial": True, "kpi": False, "3d": False, "assets": False}),
        dcc.Store(id="active-view", data="geospatial"),  # Track which view is currently active
        dcc.Interval(id="sphere-anim", interval=120, n_intervals=0, disabled=True),
        
        # Geospatial Section
        html.Div(id="geospatial-section", children=[
            html.Div([
                html.Div("Geospatial View", style=get_title_style()),
                html.Div("Interactive map view of industrial assets and locations", style=get_subtitle_style()),
                html.Div([
                    build_geospatial_map(snapshot_kpi),
                    html.Div(id="geospatial-info-box", style={
                        "marginTop": "10px", "background": "#e3eefa", "padding": "8px 14px", 
                        "borderRadius": "8px", "display": "inline-block", 
                        "fontFamily": "'Open Sans', 'Segoe UI', 'Arial', sans-serif"
                    })
                ], style={"width": "100%"})
            ], style={**get_card_style(), "padding": "24px 28px 18px 24px"})
        ], style={**get_section_style(), "padding": "32px 32px 18px 32px"}),
        
        html.Div(style={"height": "18px"}),
        
        # KPI Section
        html.Div(id="kpi-section", children=[
            html.Div([
                build_kpi_cards()
            ], style={**get_section_style(), "padding": "32px 32px 18px 32px"})
        ], style={"display": "none"}),
        
        html.Div(style={"height": "18px"}),
        
        # 3D Site Section
        html.Div(id="garching-3d-section", children=[
            html.Div([
                html.Div([
                    html.Div("Industrial 3D Navigator – Siemens Technology Center Garching", style=get_title_style()),
                    html.Div("Use the overlay controls to pan, zoom, rotate, and click parts to navigate industrial assets.", style=get_subtitle_style()),
                    html.Div(id="garching-3d-container", children=[dash_vtk.View(id="vtk-garching-view", style={"display": "none"})]),
                    html.Div("📍 Site pin: Siemens Technology Center Garching", style={
                        "fontSize": "0.9rem", "color": "#666", "marginTop": "8px", 
                        "fontFamily": "'Open Sans', 'Segoe UI', 'Arial', sans-serif"
                    }),
                ], style={**get_card_style(), "padding": "24px 28px 18px 24px"})
            ], style={**get_section_style(), "padding": "0 32px 0 32px"})
        ], style={"display": "none"}),
        
        html.Div(style={"height": "18px"}),
        
        # Asset Section
        html.Div(id="asset-section", children=[
            html.Div([
                html.Div([
                    html.Div([
                        html.Div("Asset Tree", style={
                            "fontWeight": "bold", "fontSize": "1.15rem", "color": "#0070b8", 
                            "marginBottom": "2px", "fontFamily": "'Open Sans', 'Segoe UI', 'Arial', sans-serif"
                        }),
                        html.Div("Select a data layer or model to view its details and visualization.", style=get_subtitle_style()),
                        build_asset_tree(),
                        html.Div("Compare Assets:", style={
                            "fontWeight": "bold", "marginTop": "12px", 
                            "fontFamily": "'Open Sans', 'Segoe UI', 'Arial', sans-serif", "color": "#0070b8"
                        }),
                        dcc.Dropdown(
                            id="multi-assets-dropdown",
                            options=[
                                {"label": item["name"], "value": item["key"]}
                                for layer in [
                                    {"layer": "Simulation Layer", "color": "#e3eefa", "items": [
                                        {"key": "sim_flow", "name": "Material Flow Simulation"},
                                        {"key": "sim_resource", "name": "Resource Utilization Simulation"},
                                    ]},
                                    {"layer": "3D Model Layer", "color": "#f0f7fa", "items": [
                                        {"key": "mesh", "name": "Digital Twin Mesh"},
                                    ]},
                                    {"layer": "Real-World Data Layer", "color": "#f8fafc", "items": [
                                        {"key": "image", "name": "2D Images"},
                                        {"key": "pointcloud", "name": "3D Scan (Point Cloud)"},
                                    ]}
                                ] for item in layer["items"]
                            ],
                            multi=True,
                            placeholder="Select assets to compare",
                            style={"width": "100%", "marginBottom": "12px"}
                        ),
                    ], style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"})
                ], style={
                    "background": "#ffffff", "borderRadius": "18px", "boxShadow": "0 2px 8px rgba(44, 62, 80, 0.07)",
                    "padding": "24px 20px 18px 20px", "margin": "0 0 0 0", "width": "230px",
                    "fontFamily": "'Open Sans', 'Segoe UI', 'Arial', sans-serif", "height": "100%", "minWidth": "210px"
                }),
                html.Div([
                    html.H3(id="asset-title", style={
                        "fontWeight": "bold", "fontSize": "1.1rem", "color": "#0070b8",
                        "marginBottom": "12px", "marginTop": "0"
                    }),
                    dcc.Tabs(id="view-tabs", value="main", children=[], style={"fontSize": "1rem"}),
                    html.Div(id="asset-view-panel", style={"marginTop": "16px"})
                ], style={
                    "background": "#ffffff", "borderRadius": "12px", "boxShadow": "0 2px 8px rgba(44, 62, 80, 0.07)",
                    "padding": "18px 18px 18px 18px", "width": "100%", "margin": "0 auto 0 28px", "flex": "1 1 0"
                })
            ], style={
                "display": "flex", "flexDirection": "row", "alignItems": "flex-start",
                **get_section_style(), "padding": "0 32px 30px 32px"
            })
        ], style={"display": "none"})
        
    ], id="main-content", style={"minHeight": "100vh", "background": "#f8fafc", "fontFamily": "'Open Sans', 'Segoe UI', 'Arial', sans-serif", "marginLeft": "380px", "transition": "margin-left 0.3s ease-in-out"}),
    
    # Export Modal
    build_export_modal(),
    
    # Download component for file exports
    dcc.Download(id="download-data")
])

# Register all callbacks
register_callbacks(app, kpi_data, days)

# --- Main Entry Point ---
if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host=HOST, port=PORT)
