"""
Reusable UI components for the Agentic Dataverse Visualizer
"""
import os
import random
from dash import html, dcc
import dash_vtk
import dash_leaflet as dl
from constants import (
    LAYERED_ASSETS, ASSET_NAME_MAP, COMPONENTS, MAP_CENTER, 
    FAST_TILE_URL, ASSETS_DIR, SIEMENS_BLUE, SIEMENS_ACCENT, SIEMENS_FONT, SIEMENS_SHADOW, KPI_LABELS, KPI_UNITS, SIDEBAR_NAVIGATION, SIEMENS_DIVIDER,
    EXPORT_FORMATS, SHARE_OPTIONS
)
from styles import (
    get_card_style, get_title_style, get_subtitle_style, get_button_style,
    get_control_button_style, get_kpi_card_style, get_asset_tree_style,
    get_view_panel_style, get_vtk_viewer_style, get_map_style,
    get_sidebar_style, get_sidebar_header_style, get_nav_button_style,
    get_export_button_style, get_share_button_style, get_export_modal_style, get_modal_overlay_style,
    get_smooth_transition_style
)

def build_sidebar():
    """Build the navigation sidebar"""
    return html.Div([
        # Sidebar Header with Toggle Button
        html.Div([
            html.Div([
                html.Div([
                    html.Img(src="/assets/logo.png", alt="Siemens Logo", style={
                        "height": "32px", "marginRight": "12px", "flexShrink": "0"
                    }),
                    html.Div([
                        html.Div("Agentic Dataverse Visualizer", style={
                            "fontWeight": "bold", "fontSize": "0.95rem", "color": SIEMENS_BLUE,
                            "fontFamily": SIEMENS_FONT, "lineHeight": "1.2", "whiteSpace": "nowrap"
                        }),
                        html.Div("Visualizer for the Industrial Metaverse", style={
                            "fontSize": "0.8rem", "color": "#666", "fontFamily": SIEMENS_FONT, "whiteSpace": "nowrap"
                        })
                    ], style={"display": "flex", "flexDirection": "column", "minWidth": "0", "flex": "1"})
                ], style={"display": "flex", "alignItems": "center", "width": "100%", "minWidth": "0"})
            ], id="sidebar-header-content"),
            html.Button("☰", id="sidebar-toggle", n_clicks=0, style={
                "position": "absolute", "top": "20px", "right": "16px",
                "background": "rgba(255, 255, 255, 0.9)", "border": f"1px solid {SIEMENS_BLUE}", 
                "fontSize": "1.2rem", "color": SIEMENS_BLUE, "cursor": "pointer", 
                "padding": "8px", "borderRadius": "4px", "minWidth": "32px", "minHeight": "32px",
                "display": "flex", "alignItems": "center", "justifyContent": "center",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.15)", "zIndex": "1001"
            })
        ], style=get_sidebar_header_style()),
        
        # Hierarchical Navigation
        html.Div(id="sidebar-navigation", children=[
            # Level 1: Geospatial (always visible)
            html.Div([
                html.Button([
                    html.Span("🗺️", style={"fontSize": "1.2rem"}),
                    html.Div([
                        html.Div("Geospatial Navigator", style={"fontWeight": "600", "fontSize": "1rem"}),
                        html.Div("Interactive map view", style={"fontSize": "0.8rem", "color": "#666"})
                    ], style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"})
                ], 
                id={"type": "nav-button", "id": "geospatial"},
                n_clicks=0,
                title="View interactive map of industrial locations",
                style={**get_nav_button_style(active=True, level=1), **get_smooth_transition_style()}
                ),
                
                # Level 2: KPI and 3D View (shown after shopfloor is opened)
                html.Div(id="level-2-navigation", children=[
                    html.Button([
                        html.Span("📊", style={"fontSize": "1.1rem"}),
                        html.Div([
                            html.Div("KPIs Navigator", style={"fontWeight": "500", "fontSize": "0.9rem"}),
                            html.Div("Sustainability metrics view", style={"fontSize": "0.75rem", "color": "#666"})
                        ], style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"})
                    ], 
                    id={"type": "nav-button", "id": "kpi"},
                    n_clicks=0,
                    title="View sustainability KPIs and performance metrics",
                    style={**get_nav_button_style(active=False, level=2), "display": "none", **get_smooth_transition_style()}
                    ),
                    html.Button([
                        html.Span("🏭", style={"fontSize": "1.1rem"}),
                        html.Div([
                            html.Div("Shopfloor Navigator", style={"fontWeight": "500", "fontSize": "0.9rem"}),
                            html.Div("3D shopfloor view", style={"fontSize": "0.75rem", "color": "#666"})
                        ], style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"})
                    ], 
                    id={"type": "nav-button", "id": "3d"},
                    n_clicks=0,
                    title="Explore 3D industrial shopfloor environment",
                    style={**get_nav_button_style(active=False, level=2), "display": "none", **get_smooth_transition_style()}
                    )
                ], style={"display": "none", "marginTop": "8px", "borderTop": f"1px solid {SIEMENS_DIVIDER}", "paddingTop": "8px"}),
                
                # Level 3: Asset View (shown after 3D part is selected)
                html.Div(id="level-3-navigation", children=[
                    html.Button([
                        html.Span("🔧", style={"fontSize": "1.0rem"}),
                        html.Div([
                            html.Div("Asset Navigator", style={"fontWeight": "500", "fontSize": "0.85rem"}),
                            html.Div("Data view for selected model", style={"fontSize": "0.7rem", "color": "#666"})
                        ], style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"})
                    ], 
                    id={"type": "nav-button", "id": "assets"},
                    n_clicks=0,
                    title="Browse data layers and models for selected assets",
                    style={**get_nav_button_style(active=False, level=3), "display": "none", **get_smooth_transition_style()}
                    )
                ], style={"display": "none", "marginTop": "8px", "borderTop": f"1px solid {SIEMENS_DIVIDER}", "paddingTop": "8px"})
            ], style={"display": "flex", "flexDirection": "column"})
        ], style={"padding": "8px 0"})
        
    ], id="sidebar", style=get_sidebar_style())

def build_asset_tree():
    """Build the hierarchical asset tree"""
    tree = []
    for i, layer in enumerate(LAYERED_ASSETS):
        tree.append(
            html.Div([
                html.Div(layer["layer"], style={
                    "fontWeight": "bold", "fontSize": "1.05rem", "color": SIEMENS_BLUE, 
                    "marginBottom": "6px", "marginTop": "8px" if i > 0 else "0", 
                    "fontFamily": SIEMENS_FONT,
                }),
                html.Div([
                    html.Button(
                        item["name"],
                        id={"type": "asset-btn", "id": item["key"]},
                        n_clicks=0,
                        style={
                            "width": "100%", "textAlign": "left", "marginBottom": "7px", 
                            "background": layer["color"], "border": "none", "borderRadius": "8px", 
                            "padding": "8px 14px", "color": SIEMENS_BLUE, "fontWeight": "bold", 
                            "fontFamily": SIEMENS_FONT, "cursor": "pointer",
                            "boxShadow": SIEMENS_SHADOW, "marginLeft": "10px"
                        }
                    ) for item in layer["items"]
                ], style={"marginLeft": "0.5em"})
            ], style={
                "background": layer["color"],
                "borderRadius": "10px", "padding": "10px 8px 8px 8px", "marginBottom": "10px",
                "boxShadow": SIEMENS_SHADOW,
            })
        )
    return html.Div(tree)

def build_kpi_cards():
    """Build KPI display cards with status indicators and analytics tabs"""
    return html.Div([
        html.Div([
            html.Div("Sustainability KPIs", style=get_title_style()),
            html.Div("Key metrics for industrial sustainability performance", style=get_subtitle_style()),
            html.Div([
                html.Div([
                    html.Div([
                        html.Span(KPI_LABELS[k], style={
                            "fontWeight": "bold", "fontSize": "14px", "color": SIEMENS_BLUE, "marginBottom": "2px"
                        }),
                        html.Span(id=f"status-{k}", style={
                            "fontSize": "16px", "marginLeft": "8px"
                        })
                    ], style={"display": "flex", "alignItems": "center"}),
                    html.Div(id=f"kpi-{k}", style={
                        "fontSize": "1.7rem", "fontWeight": "600", "color": "#222", "marginBottom": "2px"
                    }),
                    html.Div(KPI_UNITS[k], style={"fontSize": "12px", "color": "#888"})
                ], id=f"card-{k}", className="card-hover", style=get_kpi_card_style()) for k in KPI_LABELS
            ], style={
                "display": "flex", "flexDirection": "column", "justifyContent": "flex-start",
                "alignItems": "flex-start", "gap": "0px", "flex": "0 0 180px"
            })
        ], style={"flex": "0 0 210px"}),
        html.Div([
            html.Div([
                html.Div([
                    html.Div("KPI Analytics Dashboard", style={
                        "fontWeight": "bold", "fontSize": "1.1rem", "color": SIEMENS_BLUE, 
                        "marginBottom": "2px", "fontFamily": SIEMENS_FONT
                    }),
                    html.Div("Advanced analysis and insights for KPI data", style=get_subtitle_style()),
                    dcc.Dropdown(
                        id="trend-kpi-dropdown",
                        options=[{"label": KPI_LABELS[k], "value": k} for k in KPI_LABELS],
                        value="energy_spend",
                        clearable=False,
                        style={"width": "180px", "marginBottom": "8px", "fontWeight": "bold"}
                    )
                ], style={"display": "flex", "flexDirection": "column", "alignItems": "flex-end"}),
                build_export_button()
            ], style={"display": "flex", "flexDirection": "column", "alignItems": "flex-end", "gap": "12px"}),
            
            # Analytics Tabs
            dcc.Tabs(id="kpi-analytics-tabs", value="trend", children=[
                dcc.Tab(label="📈 Trend", value="trend", style={"fontSize": "14px", "fontWeight": "600"}),
                dcc.Tab(label="📊 Analytics", value="analytics", style={"fontSize": "14px", "fontWeight": "600"}),
                dcc.Tab(label="🔮 Forecast", value="forecast", style={"fontSize": "14px", "fontWeight": "600"})
            ], style={"marginBottom": "12px"}),
            
            # Tab Content
            html.Div(id="kpi-analytics-content", children=[
                dcc.Graph(
                    id="trend-chart",
                    config={"displayModeBar": False},
                    style={"height": "300px"}
                )
            ], style={
                "background": "#ffffff",
                "borderRadius": "12px",
                "boxShadow": SIEMENS_SHADOW,
                "padding": "16px",
                "minHeight": "300px"
            })
        ], style={"flex": "1 1 0", "marginLeft": "28px"})
    ], style={
        "display": "flex", "flexDirection": "row", "gap": "28px",
        **get_card_style(),
        "alignItems": "flex-start"
    })

def build_geospatial_map(snapshot_kpi):
    """Build the geospatial map component"""
    return dl.Map(
        id="geospatial-map",
        center=MAP_CENTER,
        zoom=15,
        style=get_map_style(),
        children=[
            dl.TileLayer(
                url=FAST_TILE_URL,
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                subdomains='abcd',
                maxZoom=19,
                updateWhenZooming=False,
                updateWhenIdle=True,
            ),
            dl.LayerGroup([
                dl.Marker(
                    position=MAP_CENTER,
                    id="shopfloor-1-marker",
                    children=[
                        dl.Tooltip("Siemens Technology Center Garching", permanent=False),
                        dl.Popup([
                            html.Div([
                                html.H4("Siemens Technology Center Garching", style={
                                    "marginBottom": "10px", "color": SIEMENS_BLUE, "fontWeight": "bold"
                                }),
                                html.Img(
                                    src="/assets/garching.png",
                                    alt="Siemens Technology Center Garching",
                                    style={
                                        "width": "200px", "height": "150px", "objectFit": "cover",
                                        "borderRadius": "8px", "marginBottom": "10px", "boxShadow": SIEMENS_SHADOW
                                    }
                                ),
                                html.Div([
                                    html.Div("📊 Sustainability KPIs:", style={
                                        "fontWeight": "bold", "marginBottom": "8px", "color": SIEMENS_BLUE
                                    }),
                                    html.Div([
                                        html.Div(f"⚡ Energy Spend: {snapshot_kpi['Energy Spend']}", style={"marginBottom": "4px"}),
                                        html.Div(f"🌍 Carbon Intensity: {snapshot_kpi['Carbon Intensity']}", style={"marginBottom": "4px"}),
                                        html.Div(f"🔧 OEE: {snapshot_kpi['OEE']}", style={"marginBottom": "4px"}),
                                        html.Div(f"💨 Compressed Air: {snapshot_kpi['Compressed Air']}", style={"marginBottom": "4px"}),
                                        html.Div(f"💧 Water Usage: {snapshot_kpi['Water Usage']}", style={"marginBottom": "4px"})
                                    ], style={"fontSize": "12px", "color": "#666"})
                                ]),
                                html.Div("📍 Friedrich-Ludwig-Bauer-Straße 3, 85748 Garching bei München", style={
                                    "fontSize": "11px", "color": "#888", "marginTop": "8px", "fontStyle": "italic"
                                }),
                                html.Button(
                                    "Open Siemens Technology Center Garching",
                                    id="shopfloor-1-button",
                                    style=get_button_style()
                                )
                            ], style={
                                "padding": "10px", "maxWidth": "250px", "fontFamily": SIEMENS_FONT
                            })
                        ])
                    ]
                )
            ]),
            dl.FullScreenControl(position="topleft"),
            dl.ScaleControl(position="bottomleft"),
        ],
        preferCanvas=True,
        zoomSnap=0.5,
        zoomDelta=0.5,
    )

def build_3d_controls():
    """Build 3D viewer control buttons"""
    return html.Div([
        # Row 1: Up
        html.Div([
            html.Button("▲", id="btn-pan-up", n_clicks=0, title="Pan up",
                        style=get_control_button_style())
        ], style={"textAlign": "center"}),
        # Row 2: Left / Zoom In / Center / Zoom Out / Right
        html.Div([
            html.Button("◀", id="btn-pan-left", n_clicks=0, title="Pan left",
                        style={**get_control_button_style(), "marginRight": "6px"}),
            html.Button("＋", id="btn-zoom-in", n_clicks=0, title="Zoom in",
                        style={**get_control_button_style("#2e7d32"), "marginRight": "6px"}),
            html.Button("◎", id="btn-center", n_clicks=0, title="Center view",
                        style={
                            "fontSize": "22px", "padding": "8px 12px", "borderRadius": "50%",
                            "background": SIEMENS_ACCENT, "color": SIEMENS_BLUE, 
                            "border": "1px solid #e0e6ed", "cursor": "pointer", 
                            "marginRight": "6px", "boxShadow": SIEMENS_SHADOW
                        }),
            html.Button("－", id="btn-zoom-out", n_clicks=0, title="Zoom out",
                        style={**get_control_button_style("#c62828"), "marginRight": "6px"}),
            html.Button("▶", id="btn-pan-right", n_clicks=0, title="Pan right",
                        style=get_control_button_style()),
        ], style={"textAlign": "center", "marginTop": "6px", "marginBottom": "6px"}),
        # Row 3: Down
        html.Div([
            html.Button("▼", id="btn-pan-down", n_clicks=0, title="Pan down",
                        style=get_control_button_style())
        ], style={"textAlign": "center"}),
        # Row 4: Rotate left/right
        html.Div([
            html.Button("⟲", id="btn-rot-left", n_clicks=0, title="Rotate left",
                        style={**get_control_button_style(SIEMENS_ACCENT, SIEMENS_BLUE), "marginRight": "6px"}),
            html.Button("⟳", id="btn-rot-right", n_clicks=0, title="Rotate right",
                        style=get_control_button_style(SIEMENS_ACCENT, SIEMENS_BLUE)),
        ], style={"textAlign": "center", "marginTop": "6px"}),
    ], style={
        "position": "absolute", "bottom": "12px", "right": "12px", 
        "background": "rgba(255,255,255,0.95)", "borderRadius": "12px", 
        "padding": "10px 12px", "boxShadow": SIEMENS_SHADOW
    })

def get_component_metadata(idx):
    """Get simulated component metadata"""
    comp = COMPONENTS[idx % len(COMPONENTS)].copy()
    comp["pressure"] = round(comp["pressure"] + random.uniform(-0.2, 0.2), 2)
    comp["status"] = random.choices(["Active", "Idle", "Fault"], weights=[0.7, 0.2, 0.1])[0]
    return comp

def build_garching_site_view():
    """Build the Garching 3D site view"""
    from data_loader import load_garching_mesh
    import dash_vtk
    
    mesh = load_garching_mesh()
    xmin, xmax, ymin, ymax, zmin, zmax = mesh.bounds
    sx = (xmax - xmin)
    sy = (ymax - ymin)
    sz = (zmax - zmin)
    center_list = [float(-0.0375 * sx), float(0.05 * sy), float(0.045 * sz)]
    points = mesh.points
    faces = mesh.faces.tolist()
    
    return html.Div([
        dash_vtk.View(
            children=[
                dash_vtk.GeometryRepresentation(
                    id="vtk-mesh-repr",
                    children=[
                        dash_vtk.PolyData(
                            points=points.flatten().tolist(),
                            polys=faces
                        )
                    ],
                    property={"pointSize": 2},
                    actor={"position": [0.0, 0.0, 0.0], "orientation": [0.0, 0.0, 0.0]}
                ),
                dash_vtk.GeometryRepresentation(
                    id="vtk-sphere-repr",
                    children=[
                        dash_vtk.Algorithm(
                            id="vtk-sphere-src",
                            vtkClass="vtkSphereSource",
                            state={
                                "center": center_list,
                                "radius": max(float(mesh.length) / 2000.0, 0.05),
                                "thetaResolution": 24,
                                "phiResolution": 24,
                            },
                        )
                    ],
                    property={"color": [1.0, 0.0, 0.0], "opacity": 1.0},
                    actor={"position": [0.0, 0.0, 0.0], "orientation": [0.0, 0.0, 0.0]}
                )
            ],
            id="vtk-garching-view",
            pickingModes=["click", "hover"],
            style={"height": "480px", "width": "100%"},
            background=[1, 1, 1]
        ),
        build_3d_controls()
    ], style={"position": "relative"})

def build_image_gallery():
    """Build image gallery for 2D images"""
    img_files = [
        f for f in os.listdir(ASSETS_DIR)
        if f.lower().startswith("festo_img") and f.lower().endswith(".png")
    ]
    
    if not img_files:
        return html.Div("No images named 'festo_img*.png' found.", style={"color": SIEMENS_BLUE})
    
    return html.Div([
        html.Div([
            html.Img(
                src=f"/assets/{fname}",
                alt=fname,
                style={
                    "width": "120px",
                    "objectFit": "cover",
                    "height": "auto",
                    "margin": "8px",
                    "borderRadius": "8px",
                    "boxShadow": SIEMENS_SHADOW
                }
            ) for fname in img_files
        ], style={
            "display": "flex",
            "flexWrap": "wrap",
            "justifyContent": "center"
        })
    ])

def build_export_button():
    """Build export button positioned near the graph"""
    return html.Button([
        html.Span("📊", style={"fontSize": "16px"}),
        html.Span("Export Data", id="export-btn-text"),
        html.Span(id="export-loading", style={"display": "none"})
    ], 
    id="export-data-btn",
    n_clicks=0,
    title="Export KPI data as CSV or JSON",
    style={**get_export_button_style(), **get_smooth_transition_style()}
    )

def build_export_modal():
    """Build simplified export modal for KPI data only"""
    return html.Div([
        # Modal Overlay
        html.Div(id="export-modal-overlay", style=get_modal_overlay_style()),
        
        # Modal Content
        html.Div([
            html.Div([
                html.Div("Export KPI Data", style={
                    "fontSize": "1.2rem",
                    "fontWeight": "bold",
                    "color": SIEMENS_BLUE,
                    "marginBottom": "16px"
                }),
                html.Div("Export your KPI data for analysis:", style={
                    "fontSize": "14px",
                    "color": "#666",
                    "marginBottom": "16px"
                }),
                
                # Export Options
                html.Div([
                    html.Div([
                        html.Label("Export Format:", style={
                            "fontWeight": "600",
                            "marginBottom": "8px",
                            "display": "block"
                        }),
                        dcc.Dropdown(
                            id="export-format-dropdown",
                            options=[
                                {"label": "CSV Data (30 days)", "value": "csv"},
                                {"label": "JSON Status Report", "value": "json"}
                            ],
                            value="csv",
                            clearable=False,
                            style={"marginBottom": "16px"}
                        )
                    ]),
                    
                    html.Div([
                        html.Label("Data to Export:", style={
                            "fontWeight": "600",
                            "marginBottom": "8px",
                            "display": "block"
                        }),
                        dcc.Checklist(
                            id="export-data-checklist",
                            options=[
                                {"label": "KPI Data (30 days)", "value": "kpi_data"},
                                {"label": "Current KPI Status", "value": "kpi_status"}
                            ],
                            value=["kpi_data"],
                            style={"marginBottom": "16px"}
                        )
                    ])
                ]),
                
                # Action Buttons
                html.Div([
                    html.Button("Cancel", 
                        id="export-cancel-btn",
                        n_clicks=0,
                        style={
                            **get_share_button_style(),
                            "marginRight": "12px"
                        }
                    ),
                    html.Button("Export", 
                        id="export-confirm-btn",
                        n_clicks=0,
                        style=get_export_button_style()
                    )
                ], style={"display": "flex", "justifyContent": "flex-end"})
                
            ], style={"padding": "0"})
        ], id="export-modal-content", style=get_export_modal_style())
        
    ], id="export-modal", style={"display": "none"})

def build_statistics_view(kpi_data, kpi_key):
    """Build statistical analysis view"""
    from data_loader import calculate_descriptive_statistics, detect_anomalies, calculate_trend_analysis
    from constants import KPI_LABELS, KPI_UNITS
    
    stats = calculate_descriptive_statistics(kpi_data, kpi_key)
    anomalies = detect_anomalies(kpi_data, kpi_key)
    trend = calculate_trend_analysis(kpi_data, kpi_key)
    
    return html.Div([
        html.Div([
            html.Div("📊 Descriptive Statistics", style={
                "fontSize": "1.1rem", "fontWeight": "bold", "color": SIEMENS_BLUE, "marginBottom": "16px"
            }),
            html.Div([
                html.Div([
                    html.Div("Central Tendency", style={"fontWeight": "600", "color": "#333", "marginBottom": "8px"}),
                    html.Div(f"Mean: {stats['mean']:.2f} {KPI_UNITS[kpi_key]}", style={"fontSize": "14px", "marginBottom": "4px"}),
                    html.Div(f"Median: {stats['median']:.2f} {KPI_UNITS[kpi_key]}", style={"fontSize": "14px", "marginBottom": "4px"}),
                    html.Div(f"Mode: {stats['mode']:.2f} {KPI_UNITS[kpi_key]}" if 'mode' in stats else f"Mode: N/A", style={"fontSize": "14px"})
                ], style={"flex": "1", "padding": "12px", "background": "#f8f9fa", "borderRadius": "8px", "marginRight": "8px"}),
                
                html.Div([
                    html.Div("Variability", style={"fontWeight": "600", "color": "#333", "marginBottom": "8px"}),
                    html.Div(f"Std Dev: {stats['std']:.2f}", style={"fontSize": "14px", "marginBottom": "4px"}),
                    html.Div(f"Variance: {stats['var']:.2f}", style={"fontSize": "14px", "marginBottom": "4px"}),
                    html.Div(f"CV: {stats['cv']:.2%}", style={"fontSize": "14px"})
                ], style={"flex": "1", "padding": "12px", "background": "#f8f9fa", "borderRadius": "8px", "marginRight": "8px"}),
                
                html.Div([
                    html.Div("Distribution", style={"fontWeight": "600", "color": "#333", "marginBottom": "8px"}),
                    html.Div(f"Skewness: {stats['skewness']:.2f}", style={"fontSize": "14px", "marginBottom": "4px"}),
                    html.Div(f"Kurtosis: {stats['kurtosis']:.2f}", style={"fontSize": "14px", "marginBottom": "4px"}),
                    html.Div(f"Range: {stats['range']:.2f}", style={"fontSize": "14px"})
                ], style={"flex": "1", "padding": "12px", "background": "#f8f9fa", "borderRadius": "8px"})
            ], style={"display": "flex", "marginBottom": "16px"}),
            
            html.Div([
                html.Div("📈 Trend Analysis", style={"fontWeight": "600", "color": "#333", "marginBottom": "8px"}),
                html.Div(f"Direction: {trend['trend_direction'].title()}", style={"fontSize": "14px", "marginBottom": "4px"}),
                html.Div(f"Significance: {trend['trend_significance'].title()}", style={"fontSize": "14px", "marginBottom": "4px"}),
                html.Div(f"R²: {trend['linear_r_squared']:.3f}", style={"fontSize": "14px"})
            ], style={"padding": "12px", "background": "#e3f2fd", "borderRadius": "8px", "marginBottom": "16px"}),
            
            html.Div([
                html.Div("🚨 Anomaly Detection", style={"fontWeight": "600", "color": "#333", "marginBottom": "8px"}),
                html.Div(f"Total Anomalies: {anomalies['total_anomalies']}", style={"fontSize": "14px", "marginBottom": "4px"}),
                html.Div(f"Anomaly Rate: {anomalies['anomaly_rate']:.1%}", style={"fontSize": "14px", "marginBottom": "4px"}),
                html.Div(f"Threshold: {anomalies['threshold']}σ", style={"fontSize": "14px"})
            ], style={"padding": "12px", "background": "#fff3e0", "borderRadius": "8px"})
        ])
    ])

def build_forecast_view(kpi_data, kpi_key):
    """Build predictive analytics view"""
    from data_loader import generate_forecast
    from constants import KPI_LABELS, KPI_UNITS
    import plotly.graph_objs as go
    
    forecast_data = generate_forecast(kpi_data, kpi_key, forecast_days=7)
    
    # Create forecast chart
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=forecast_data['historical_days'],
        y=forecast_data['historical_values'],
        mode='lines+markers',
        name='Historical',
        line=dict(color=SIEMENS_BLUE, width=3),
        marker=dict(size=6)
    ))
    
    # Forecast data
    fig.add_trace(go.Scatter(
        x=forecast_data['forecast_days'],
        y=forecast_data['forecast_values'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#ff6b35', width=3, dash='dash'),
        marker=dict(size=6)
    ))
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=forecast_data['forecast_days'] + forecast_data['forecast_days'][::-1],
        y=forecast_data['upper_bound'] + forecast_data['lower_bound'][::-1],
        fill='toself',
        fillcolor='rgba(255, 107, 53, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='95% Confidence',
        hoverinfo="skip"
    ))
    
    fig.update_layout(
        title=f"{KPI_LABELS[kpi_key]} - 7-Day Forecast",
        xaxis_title="Day",
        yaxis_title=f"{KPI_LABELS[kpi_key]} ({KPI_UNITS[kpi_key]})",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family=SIEMENS_FONT, size=12),
        height=300,
        showlegend=True,
        legend=dict(x=0.02, y=0.98)
    )
    
    return html.Div([
        html.Div([
            dcc.Graph(figure=fig, config={"displayModeBar": False}),
            html.Div([
                html.Div([
                    html.Div("Model Performance", style={"fontWeight": "600", "color": "#333", "marginBottom": "8px"}),
                    html.Div(f"R² Score: {forecast_data['r_squared']:.3f}", style={"fontSize": "14px", "marginBottom": "4px"}),
                    html.Div(f"Slope: {forecast_data['slope']:.4f}", style={"fontSize": "14px", "marginBottom": "4px"}),
                    html.Div(f"Intercept: {forecast_data['intercept']:.2f}", style={"fontSize": "14px"})
                ], style={"flex": "1", "padding": "12px", "background": "#f8f9fa", "borderRadius": "8px", "marginRight": "8px"}),
                
                html.Div([
                    html.Div("Next 7 Days", style={"fontWeight": "600", "color": "#333", "marginBottom": "8px"}),
                    html.Div(f"Day 31: {forecast_data['forecast_values'][0]:.2f} {KPI_UNITS[kpi_key]}", style={"fontSize": "14px", "marginBottom": "4px"}),
                    html.Div(f"Day 35: {forecast_data['forecast_values'][4]:.2f} {KPI_UNITS[kpi_key]}", style={"fontSize": "14px", "marginBottom": "4px"}),
                    html.Div(f"Day 37: {forecast_data['forecast_values'][6]:.2f} {KPI_UNITS[kpi_key]}", style={"fontSize": "14px"})
                ], style={"flex": "1", "padding": "12px", "background": "#e8f5e8", "borderRadius": "8px"})
            ], style={"display": "flex", "marginTop": "16px"})
        ])
    ])

def build_combined_analytics_view(kpi_data, kpi_key):
    """Build combined statistics and correlation analysis view"""
    from data_loader import calculate_descriptive_statistics, detect_anomalies, calculate_trend_analysis, perform_correlation_analysis
    from constants import KPI_LABELS, KPI_UNITS
    
    # Get statistics data
    stats = calculate_descriptive_statistics(kpi_data, kpi_key)
    anomalies = detect_anomalies(kpi_data, kpi_key)
    trend = calculate_trend_analysis(kpi_data, kpi_key)
    
    # Get correlation data for key insights only
    corr_data = perform_correlation_analysis(kpi_data)
    
    # Find strongest correlations
    strong_correlations = []
    for i, kpi1 in enumerate(KPI_LABELS.keys()):
        for j, kpi2 in enumerate(KPI_LABELS.keys()):
            if i < j:  # Avoid duplicates
                corr_val = corr_data[kpi1][kpi2]
                if abs(corr_val) > 0.5:  # Strong correlation threshold
                    strong_correlations.append({
                        'kpi1': KPI_LABELS[kpi1],
                        'kpi2': KPI_LABELS[kpi2],
                        'correlation': corr_val,
                        'strength': 'Strong' if abs(corr_val) > 0.7 else 'Moderate'
                    })
    
    return html.Div([
        # Statistics Grid - Dense Layout
        html.Div([
            # Row 1: Central Tendency & Variability
            html.Div([
                html.Div([
                    html.Div("📊 Central Tendency", style={
                        "fontWeight": "600", "color": SIEMENS_BLUE, "marginBottom": "8px", "fontSize": "14px"
                    }),
                    html.Div(f"Mean: {stats['mean']:.2f} {KPI_UNITS[kpi_key]}", style={"fontSize": "13px", "marginBottom": "3px"}),
                    html.Div(f"Median: {stats['median']:.2f} {KPI_UNITS[kpi_key]}", style={"fontSize": "13px", "marginBottom": "3px"}),
                    html.Div(f"Mode: {stats['mode']:.2f} {KPI_UNITS[kpi_key]}" if 'mode' in stats else f"Mode: N/A", style={"fontSize": "13px"})
                ], style={"flex": "1", "padding": "10px", "background": "#f8f9fa", "borderRadius": "6px", "marginRight": "8px"}),
                
                html.Div([
                    html.Div("📈 Variability", style={
                        "fontWeight": "600", "color": SIEMENS_BLUE, "marginBottom": "8px", "fontSize": "14px"
                    }),
                    html.Div(f"Std Dev: {stats['std']:.2f}", style={"fontSize": "13px", "marginBottom": "3px"}),
                    html.Div(f"Variance: {stats['var']:.2f}", style={"fontSize": "13px", "marginBottom": "3px"}),
                    html.Div(f"CV: {stats['cv']:.2%}", style={"fontSize": "13px"})
                ], style={"flex": "1", "padding": "10px", "background": "#f8f9fa", "borderRadius": "6px", "marginRight": "8px"}),
                
                html.Div([
                    html.Div("📊 Distribution", style={
                        "fontWeight": "600", "color": SIEMENS_BLUE, "marginBottom": "8px", "fontSize": "14px"
                    }),
                    html.Div(f"Skewness: {stats['skewness']:.2f}", style={"fontSize": "13px", "marginBottom": "3px"}),
                    html.Div(f"Kurtosis: {stats['kurtosis']:.2f}", style={"fontSize": "13px", "marginBottom": "3px"}),
                    html.Div(f"Range: {stats['range']:.2f}", style={"fontSize": "13px"})
                ], style={"flex": "1", "padding": "10px", "background": "#f8f9fa", "borderRadius": "6px"})
            ], style={"display": "flex", "marginBottom": "12px"}),
            
            # Row 2: Trend & Anomaly Analysis
            html.Div([
                html.Div([
                    html.Div("📈 Trend Analysis", style={
                        "fontWeight": "600", "color": SIEMENS_BLUE, "marginBottom": "8px", "fontSize": "14px"
                    }),
                    html.Div(f"Direction: {trend['trend_direction'].title()}", style={"fontSize": "13px", "marginBottom": "3px"}),
                    html.Div(f"Significance: {trend['trend_significance'].title()}", style={"fontSize": "13px", "marginBottom": "3px"}),
                    html.Div(f"R²: {trend['linear_r_squared']:.3f}", style={"fontSize": "13px"})
                ], style={"flex": "1", "padding": "10px", "background": "#e3f2fd", "borderRadius": "6px", "marginRight": "8px"}),
                
                html.Div([
                    html.Div("🚨 Anomaly Detection", style={
                        "fontWeight": "600", "color": SIEMENS_BLUE, "marginBottom": "8px", "fontSize": "14px"
                    }),
                    html.Div(f"Total Anomalies: {anomalies['total_anomalies']}", style={"fontSize": "13px", "marginBottom": "3px"}),
                    html.Div(f"Anomaly Rate: {anomalies['anomaly_rate']:.1%}", style={"fontSize": "13px", "marginBottom": "3px"}),
                    html.Div(f"Threshold: {anomalies['threshold']}σ", style={"fontSize": "13px"})
                ], style={"flex": "1", "padding": "10px", "background": "#fff3e0", "borderRadius": "6px"})
            ], style={"display": "flex", "marginBottom": "12px"}),
            
            # Row 3: Key Correlations (if any)
            html.Div([
                html.Div("🔗 Key Correlations", style={
                    "fontWeight": "600", "color": SIEMENS_BLUE, "marginBottom": "8px", "fontSize": "14px"
                }),
                html.Div([
                    html.Div([
                        html.Div(f"{corr['kpi1']} ↔ {corr['kpi2']}", style={"fontWeight": "500", "fontSize": "13px"}),
                        html.Div(f"{corr['correlation']:.3f} ({corr['strength']})", style={"fontSize": "12px", "color": "#666"})
                    ], style={
                        "display": "flex", "justifyContent": "space-between", "alignItems": "center",
                        "padding": "6px 10px", "background": "#f0f8ff", "borderRadius": "4px", "marginBottom": "4px"
                    })
                    for corr in strong_correlations[:3]  # Show top 3 in dense format
                ]) if strong_correlations else html.Div("No significant correlations found", style={"fontSize": "13px", "color": "#666", "fontStyle": "italic"})
            ], style={"padding": "10px", "background": "#f8f9fa", "borderRadius": "6px"})
        ], style={"display": "flex", "flexDirection": "column"})
    ])

