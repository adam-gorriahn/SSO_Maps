"""
Simplified callbacks for the Agentic Dataverse Visualizer
Just basic navigation - click button to show that view, nothing else changes.
"""
import dash
from dash import html, dcc, Input, Output, State, ALL
import plotly.graph_objs as go
import numpy as np
import random
from data_loader import (
    load_festo_mesh, load_festo_pointcloud, load_garching_mesh, process_point_cloud_colors,
    export_kpi_data_to_csv, export_kpi_data_to_json, export_kpi_status_to_json
)
from components import get_component_metadata, build_image_gallery
from constants import KPI_LABELS, KPI_UNITS, SPHERE_ANIMATION_FRAMES
from styles import SIEMENS_BLUE, SIEMENS_ACCENT, SIEMENS_CARD, SIEMENS_FONT, SIEMENS_STATUS
from constants import SIEMENS_DIVIDER

def register_callbacks(app, kpi_data, days):
    """Register all callback functions with the app"""
    
    # --- Sidebar Toggle Callback (Combined) ---
    @app.callback(
        Output("sidebar", "style"),
        Output("main-content", "style"),
        Output("sidebar-collapsed", "data"),
        Input("sidebar-toggle", "n_clicks"),
        Input("floating-sidebar-toggle", "n_clicks"),
        State("sidebar-collapsed", "data"),
        prevent_initial_call=True
    )
    def toggle_sidebar(sidebar_clicks, floating_clicks, is_collapsed):
        from styles import get_sidebar_style, get_sidebar_collapsed_style
        
        # Check which button was clicked
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update, dash.no_update, dash.no_update
        
        # Toggle the collapsed state
        new_collapsed_state = not is_collapsed
        
        if new_collapsed_state:
            # Hide sidebar
            sidebar_style = get_sidebar_collapsed_style()
            main_style = {"minHeight": "100vh", "background": "#f8fafc", "fontFamily": "'Open Sans', 'Segoe UI', 'Arial', sans-serif", "marginLeft": "0", "transition": "margin-left 0.3s ease-in-out"}
        else:
            # Show sidebar
            sidebar_style = get_sidebar_style()
            main_style = {"minHeight": "100vh", "background": "#f8fafc", "fontFamily": "'Open Sans', 'Segoe UI', 'Arial', sans-serif", "marginLeft": "380px", "transition": "margin-left 0.3s ease-in-out"}
        
        return sidebar_style, main_style, new_collapsed_state

    # --- Floating Button Visibility Callback ---
    @app.callback(
        Output("floating-sidebar-toggle", "style"),
        Input("sidebar-collapsed", "data"),
        prevent_initial_call=False
    )
    def update_floating_button_visibility(is_collapsed):
        """Show floating button only when sidebar is hidden"""
        from constants import SIEMENS_BLUE
        
        base_style = {
            "position": "fixed", "top": "20px", "left": "20px", "zIndex": "1001",
            "background": "rgba(255, 255, 255, 0.9)", "border": f"2px solid {SIEMENS_BLUE}", 
            "fontSize": "1.5rem", "color": SIEMENS_BLUE, "cursor": "pointer", 
            "padding": "12px", "borderRadius": "8px", "minWidth": "48px", "minHeight": "48px",
            "display": "flex", "alignItems": "center", "justifyContent": "center",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.15)", "fontWeight": "bold",
            "transition": "opacity 0.3s ease-in-out"
        }
        
        if is_collapsed:
            # Show floating button when sidebar is hidden
            base_style["opacity"] = "1"
            base_style["pointerEvents"] = "auto"
        else:
            # Hide floating button when sidebar is visible
            base_style["opacity"] = "0"
            base_style["pointerEvents"] = "none"
        
        return base_style

    # --- Sidebar Initialization Callback ---
    @app.callback(
        Output("sidebar", "style", allow_duplicate=True),
        Output("main-content", "style", allow_duplicate=True),
        Input("sidebar-collapsed", "data"),
        prevent_initial_call='initial_duplicate'
    )
    def initialize_sidebar(is_collapsed):
        """Initialize sidebar state on app load"""
        from styles import get_sidebar_style, get_sidebar_collapsed_style
        
        if is_collapsed:
            # Sidebar is hidden
            sidebar_style = get_sidebar_collapsed_style()
            main_style = {"minHeight": "100vh", "background": "#f8fafc", "fontFamily": "'Open Sans', 'Segoe UI', 'Arial', sans-serif", "marginLeft": "0", "transition": "margin-left 0.3s ease-in-out"}
        else:
            # Sidebar is visible
            sidebar_style = get_sidebar_style()
            main_style = {"minHeight": "100vh", "background": "#f8fafc", "fontFamily": "'Open Sans', 'Segoe UI', 'Arial', sans-serif", "marginLeft": "380px", "transition": "margin-left 0.3s ease-in-out"}
        
        return sidebar_style, main_style

    # --- Sidebar Navigation Callbacks ---
    @app.callback(
        Output("geospatial-section", "style"),
        Output("kpi-section", "style"),
        Output("garching-3d-section", "style"),
        Output("asset-section", "style"),
        Output("active-view", "data"),
        Input({"type": "nav-button", "id": "geospatial"}, "n_clicks"),
        Input({"type": "nav-button", "id": "kpi"}, "n_clicks"),
        Input({"type": "nav-button", "id": "3d"}, "n_clicks"),
        Input({"type": "nav-button", "id": "assets"}, "n_clicks"),
        prevent_initial_call=True
    )
    def handle_sidebar_navigation(geo_clicks, kpi_clicks, d3_clicks, assets_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        # Get the button that was clicked
        button_id = ctx.triggered[0]['prop_id'].split('"')[3]
        
        # Hide all sections first
        hidden_style = {"display": "none"}
        visible_style = {"display": "block", "marginTop": "18px"}
        
        if button_id == "geospatial":
            return visible_style, hidden_style, hidden_style, hidden_style, "geospatial"
        elif button_id == "kpi":
            return hidden_style, visible_style, hidden_style, hidden_style, "kpi"
        elif button_id == "3d":
            return hidden_style, hidden_style, visible_style, hidden_style, "3d"
        elif button_id == "assets":
            return hidden_style, hidden_style, hidden_style, visible_style, "assets"
        
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # --- Active View Button Styling Callback ---
    @app.callback(
        Output({"type": "nav-button", "id": "geospatial"}, "style"),
        Output({"type": "nav-button", "id": "kpi"}, "style"),
        Output({"type": "nav-button", "id": "3d"}, "style"),
        Output({"type": "nav-button", "id": "assets"}, "style"),
        Input("active-view", "data"),
        Input("view-visibility", "data"),
        prevent_initial_call=False
    )
    def update_active_button_styles(active_view, visibility_data):
        from styles import get_nav_button_style
        
        # Get styles for each button based on active state and visibility
        geo_style = get_nav_button_style(active=(active_view == "geospatial"), level=1)
        kpi_style = get_nav_button_style(active=(active_view == "kpi"), level=2)
        d3_style = get_nav_button_style(active=(active_view == "3d"), level=2)
        assets_style = get_nav_button_style(active=(active_view == "assets"), level=3)
        
        # Apply visibility
        if not visibility_data.get("kpi", False):
            kpi_style["display"] = "none"
        if not visibility_data.get("3d", False):
            d3_style["display"] = "none"
        if not visibility_data.get("assets", False):
            assets_style["display"] = "none"
        
        return geo_style, kpi_style, d3_style, assets_style

    # --- Hierarchical View Visibility Tracking Callback ---
    @app.callback(
        Output("view-visibility", "data"),
        Output("level-2-navigation", "style"),
        Output("level-3-navigation", "style"),
        Input("clicked-shopfloor", "data"),
        Input("garching-selected-part", "data"),
        State("view-visibility", "data"),
        prevent_initial_call=False
    )
    def track_hierarchical_visibility(shopfloor_data, selected_part, visibility_data):
        from styles import get_nav_button_style
        
        print(f"Hierarchical visibility callback: shopfloor_data={shopfloor_data}, selected_part={selected_part}")  # Debug
        
        # Update visibility based on user interactions
        new_visibility = visibility_data.copy()
        
        # Level 2: Show KPI and 3D navigation when shopfloor is opened
        level2_style = {"display": "none", "marginTop": "8px", "borderTop": f"1px solid {SIEMENS_DIVIDER}", "paddingTop": "8px"}
        if shopfloor_data is not None:
            new_visibility["kpi"] = True
            new_visibility["3d"] = True
            level2_style = {"display": "block", "marginTop": "8px", "borderTop": f"1px solid {SIEMENS_DIVIDER}", "paddingTop": "8px"}
            print("Showing Level 2 navigation (KPI and 3D)")  # Debug
        
        # Level 3: Show Assets navigation when a part is selected in 3D view
        level3_style = {"display": "none", "marginTop": "8px", "borderTop": f"1px solid {SIEMENS_DIVIDER}", "paddingTop": "8px"}
        if isinstance(selected_part, dict) and selected_part.get("type") == "sphere":
            new_visibility["assets"] = True
            level3_style = {"display": "block", "marginTop": "8px", "borderTop": f"1px solid {SIEMENS_DIVIDER}", "paddingTop": "8px"}
            print("Showing Level 3 navigation (Assets)")  # Debug
        
        print(f"Hierarchical visibility: Level2={level2_style['display']}, Level3={level3_style['display']}")  # Debug
        
        return new_visibility, level2_style, level3_style
    
    # --- Note: Section visibility is now handled by sidebar navigation callbacks ---

    # --- Garching 3D Container Callback ---
    @app.callback(
        Output("garching-3d-container", "children"),
        Input("clicked-shopfloor", "data"),
        prevent_initial_call=False
    )
    def show_garching_site(shopfloor_data):
        if shopfloor_data:
            from components import build_garching_site_view
            return build_garching_site_view()
        return dash.no_update

    # --- Garching Click Handler ---
    @app.callback(
        Output("garching-selected-part", "data"),
        Input("vtk-garching-view", "clickInfo"),
        Input("clicked-shopfloor", "data"),
        prevent_initial_call=False
    )
    def handle_garching_click(click_info, shopfloor_data):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        
        if ctx.triggered[0]['prop_id'].startswith("clicked-shopfloor"):
            return None
        
        if click_info:
            try:
                rep_id = click_info.get("representationId") if isinstance(click_info, dict) else None
            except Exception:
                rep_id = None
            if rep_id == "vtk-sphere-repr":
                return {"type": "sphere", "data": click_info}
            return click_info
        return dash.no_update


    # --- Note: No sidebar assets button, assets section always visible ---

    # --- Sphere Animation Callbacks ---
    @app.callback(
        Output("sphere-anim", "disabled"),
        Output("sphere-anim", "n_intervals"),
        Input("garching-selected-part", "data"),
        prevent_initial_call=False
    )
    def trigger_sphere_anim(selection):
        if isinstance(selection, dict) and selection.get("type") == "sphere":
            return False, 0
        return dash.no_update, dash.no_update

    @app.callback(
        Output("vtk-sphere-src", "state", allow_duplicate=True),
        Output("vtk-sphere-repr", "property", allow_duplicate=True),
        Input("sphere-anim", "n_intervals"),
        State("vtk-sphere-src", "state"),
        State("sphere-anim", "disabled"),
        prevent_initial_call=True
    )
    def animate_sphere(n, state, disabled):
        if disabled or not isinstance(state, dict):
            return dash.no_update, dash.no_update
        
        center = state.get("center", [0, 0, 0])
        base_r = float(state.get("baseRadius", state.get("radius", 0.1)))

        total_frames = SPHERE_ANIMATION_FRAMES
        t = max(0, min(int(n), total_frames))
        grow_frames = total_frames // 2
        max_scale = 1.30

        if t <= grow_frames:
            scale = 1.0 + (max_scale - 1.0) * (t / grow_frames)
        else:
            back_t = t - grow_frames
            scale = max_scale - (max_scale - 1.0) * (back_t / (total_frames - grow_frames))

        if t >= total_frames:
            radius = base_r
        else:
            radius = base_r * float(scale)

        new_state = {**state, "center": center, "radius": radius, "baseRadius": base_r}
        new_prop = {"color": [1.0, 0.0, 0.0], "opacity": 1.0}
        return new_state, new_prop

    @app.callback(
        Output("sphere-anim", "disabled", allow_duplicate=True),
        Input("sphere-anim", "n_intervals"),
        State("sphere-anim", "disabled"),
        prevent_initial_call=True
    )
    def stop_anim_after(n, disabled):
        if not disabled and n >= SPHERE_ANIMATION_FRAMES:
            return True
        return dash.no_update

    # --- Bounds Initialization ---
    @app.callback(
        Output("garching-bounds", "data"),
        Input("clicked-shopfloor", "data"),
        prevent_initial_call=False
    )
    def init_bounds(shopfloor_data):
        if shopfloor_data:
            m = load_garching_mesh()
            xmin, xmax, ymin, ymax, zmin, zmax = m.bounds
            return {"sx": float(xmax - xmin), "sy": float(ymax - ymin), "sz": float(zmax - zmin)}
        return dash.no_update

    # --- Viewer Controls ---
    @app.callback(
        Output("vtk-mesh-repr", "actor", allow_duplicate=True),
        Output("vtk-sphere-repr", "actor", allow_duplicate=True),
        Input("btn-pan-up", "n_clicks"),
        Input("btn-pan-down", "n_clicks"),
        Input("btn-pan-left", "n_clicks"),
        Input("btn-pan-right", "n_clicks"),
        Input("btn-zoom-in", "n_clicks"),
        Input("btn-zoom-out", "n_clicks"),
        Input("btn-center", "n_clicks"),
        Input("btn-rot-left", "n_clicks"),
        Input("btn-rot-right", "n_clicks"),
        State("vtk-mesh-repr", "actor"),
        State("garching-bounds", "data"),
        prevent_initial_call=True
    )
    def viewer_controls(up, down, left, right, zoom_in, zoom_out, center, rotl, rotr, actor, bounds):
        ctx = dash.callback_context
        if not ctx.triggered or not bounds:
            return dash.no_update, dash.no_update
        
        which = ctx.triggered[0]['prop_id'].split('.')[0]
        actor = dict(actor or {})
        pos = list(actor.get("position", [0.0, 0.0, 0.0]))
        ori = list(actor.get("orientation", [0.0, 0.0, 0.0]))
        sx, sy, sz = bounds.get("sx", 1.0), bounds.get("sy", 1.0), bounds.get("sz", 1.0)
        
        step_x = 0.02 * sx
        step_y = 0.02 * sy
        step_z = 0.01 * sz
        
        control_map = {
            "btn-pan-up": lambda: (pos[1] - step_y, ori),
            "btn-pan-down": lambda: (pos[1] + step_y, ori),
            "btn-pan-left": lambda: (pos[0] + step_x, ori),
            "btn-pan-right": lambda: (pos[0] - step_x, ori),
            "btn-zoom-in": lambda: (pos[2] + step_z, ori),
            "btn-zoom-out": lambda: (pos[2] - step_z, ori),
            "btn-center": lambda: ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
            "btn-rot-left": lambda: (pos, ori[2] + 12),
            "btn-rot-right": lambda: (pos, ori[2] - 12),
        }
        
        if which in control_map:
            new_pos, new_ori = control_map[which]()
            if isinstance(new_pos, list):
                pos = new_pos
            if isinstance(new_ori, list):
                ori = new_ori
            elif isinstance(new_ori, (int, float)):
                ori[2] = new_ori
        
        new_actor = {"position": [float(p) for p in pos], "orientation": [float(o) for o in ori]}
        return new_actor, new_actor

    # --- KPI Update Callbacks ---
    @app.callback(
        [Output(f"kpi-{k}", "children") for k in KPI_LABELS],
        [Output(f"status-{k}", "children") for k in KPI_LABELS],
        [Output(f"card-{k}", "style") for k in KPI_LABELS],
        Input("trend-kpi-dropdown", "value"),
        prevent_initial_call=False
    )
    def update_kpi_cards(selected_kpi):
        from data_loader import calculate_kpi_status
        from styles import get_kpi_card_with_status_style
        from constants import KPI_STATUS_ICONS
        
        # Use the latest data (idx = -1) since we're not using hover data anymore
        idx = -1
        
        values = []
        status_icons = []
        card_styles = []
        
        for k in KPI_LABELS:
            val = kpi_data[k][idx]
            if k == 'oee':
                val = f"{val*100:.1f}%"
            else:
                val = f"{val:.1f}"
            values.append(val)
            
            # Calculate status and get icon
            status = calculate_kpi_status(kpi_data, k, idx)
            status_icons.append(KPI_STATUS_ICONS[status])
            
            # Update card style based on status
            card_styles.append(get_kpi_card_with_status_style(status))
        
        return values + status_icons + card_styles

    @app.callback(
        Output("trend-chart", "figure"),
        Input("trend-kpi-dropdown", "value")
    )
    def update_trend_chart(selected_kpi):
        return make_trend_figure(selected_kpi, kpi_data, days)

    # --- KPI Hover Update Callback (Optional) ---
    @app.callback(
        [Output(f"kpi-{k}", "children", allow_duplicate=True) for k in KPI_LABELS],
        [Output(f"status-{k}", "children", allow_duplicate=True) for k in KPI_LABELS],
        [Output(f"card-{k}", "style", allow_duplicate=True) for k in KPI_LABELS],
        Input("trend-chart", "hoverData"),
        prevent_initial_call=True
    )
    def update_kpi_cards_on_hover(trend_hover):
        from data_loader import calculate_kpi_status
        from styles import get_kpi_card_with_status_style
        from constants import KPI_STATUS_ICONS
        
        idx = -1
        if trend_hover and 'points' in trend_hover:
            try:
                day = int(trend_hover['points'][0].get('x', 0))
                if 1 <= day <= 30:
                    idx = day - 1
            except Exception:
                pass
        
        values = []
        status_icons = []
        card_styles = []
        
        for k in KPI_LABELS:
            val = kpi_data[k][idx]
            if k == 'oee':
                val = f"{val*100:.1f}%"
            else:
                val = f"{val:.1f}"
            values.append(val)
            
            # Calculate status and get icon
            status = calculate_kpi_status(kpi_data, k, idx)
            status_icons.append(KPI_STATUS_ICONS[status])
            
            # Update card style based on status
            card_styles.append(get_kpi_card_with_status_style(status))
        
        return values + status_icons + card_styles

    # --- Analytics Tabs Callback ---
    @app.callback(
        Output("kpi-analytics-content", "children"),
        Input("kpi-analytics-tabs", "value"),
        Input("trend-kpi-dropdown", "value")
    )
    def update_analytics_content(active_tab, selected_kpi):
        from components import build_combined_analytics_view, build_forecast_view
        
        if active_tab == "trend":
            # For trend tab, we just return the existing trend-chart component
            return dcc.Graph(
                figure=make_trend_figure(selected_kpi, kpi_data, days),
                config={"displayModeBar": False},
                style={"height": "300px"}
            )
        elif active_tab == "analytics":
            return build_combined_analytics_view(kpi_data, selected_kpi)
        elif active_tab == "forecast":
            return build_forecast_view(kpi_data, selected_kpi)
        
        return html.Div("Select an analysis type", style={"textAlign": "center", "color": "#666"})

    # --- Asset Selection Callbacks ---
    @app.callback(
        Output("selected-asset-key", "data"),
        Output("asset-title", "children"),
        Output("view-tabs", "children"),
        Output("view-tabs", "value"),
        [Output({"type": "asset-btn", "id": ALL}, "n_clicks")],
        Input({"type": "asset-btn", "id": ALL}, "n_clicks"),
        State({"type": "asset-btn", "id": ALL}, "id"),
        prevent_initial_call=True
    )
    def select_asset(n_clicks_list, id_list):
        for idx, (n_clicks, btn_id) in enumerate(zip(n_clicks_list, id_list)):
            if n_clicks:
                key = btn_id["id"]
                from constants import ASSET_NAME_MAP
                name = ASSET_NAME_MAP.get(key, key)
                tabs = [dash.dcc.Tab(label="Main View", value="main")]
                reset_clicks = [0] * len(n_clicks_list)
                return key, name, tabs, "main", reset_clicks
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # --- Asset View Panel Callback ---
    @app.callback(
        Output("asset-view-panel", "children"),
        Input("view-tabs", "value"),
        Input("multi-assets-dropdown", "value"),
        State("selected-asset-key", "data"),
        State("asset-title", "children")
    )
    def show_asset_view(view, multi_keys, asset_key, asset_name):
        if multi_keys and len(multi_keys) > 1:
            return build_multi_asset_view(multi_keys, view)
        
        if not asset_key or not asset_name:
            return "Select a data layer or model from the tree."
        
        return build_single_asset_view(asset_key)

    # --- Geospatial Info Callback ---
    @app.callback(
        Output("geospatial-info-box", "children"),
        Input("geospatial-map", "center"),
        Input("geospatial-map", "zoom"),
        prevent_initial_call=False
    )
    def update_geospatial_info(center, zoom):
        if center and isinstance(center, (list, tuple)) and len(center) >= 2 and zoom:
            return f"Center: ({center[0]:.4f}, {center[1]:.4f}) | Zoom: {zoom}"
        return "Center: (48.265132904052734, 11.661945343017578) | Zoom: 15"

    # --- Shopfloor Click Callback ---
    @app.callback(
        Output("clicked-shopfloor", "data"),
        Input("shopfloor-1-button", "n_clicks"),
        prevent_initial_call=True
    )
    def handle_shopfloor_click(shop1_clicks):
        ctx = dash.callback_context
        print(f"Shopfloor callback triggered! n_clicks: {shop1_clicks}, triggered: {ctx.triggered}")  # Debug
        if not ctx.triggered:
            return None
        print("Returning shopfloor-1")  # Debug
        return "shopfloor-1"

    # --- Debug: Show when shopfloor data changes ---
    @app.callback(
        Output("geospatial-info-box", "children", allow_duplicate=True),
        Input("clicked-shopfloor", "data"),
        State("geospatial-info-box", "children"),
        prevent_initial_call=True
    )
    def debug_shopfloor_change(shopfloor_data, current_info):
        print(f"Shopfloor data changed to: {shopfloor_data}")  # Debug
        if shopfloor_data:
            return f"Shopfloor opened: {shopfloor_data} | {current_info}"
        return current_info

    # --- Note: No sidebar buttons, all sections always visible ---

    # --- Mesh Metadata Callback ---
    @app.callback(
        Output("mesh-metadata-panel", "children"),
        Input("vtk-view", "hoverInfo"),
    )
    def show_mesh_metadata(hover):
        if hover:
            idx = random.randint(0, len(get_component_metadata(0)) - 1)
            meta = get_component_metadata(idx)
            return dash.html.Div([
                dash.html.Div(f"Component: {meta['name']}", style={"fontWeight": "bold"}),
                dash.html.Div(f"Pressure: {meta['pressure']} bar"),
                dash.html.Div(f"Status: {meta['status']}", style={"color": SIEMENS_STATUS.get(meta['status'], '#444')}),
                dash.html.Div(f"Last Service: {meta['last_service']}")
            ], style={"background": SIEMENS_ACCENT, "padding": "10px", "borderRadius": "8px"})
        return dash.html.Div("Hover over mesh for metadata", style={"color": "#888"})

    # --- Export Callbacks ---
    
    # Export Modal Toggle
    @app.callback(
        Output("export-modal", "style"),
        Input("export-data-btn", "n_clicks"),
        Input("export-cancel-btn", "n_clicks"),
        Input("export-confirm-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_export_modal(export_btn, cancel_btn, confirm_btn):
        ctx = dash.callback_context
        if not ctx.triggered:
            return {"display": "none"}
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == "export-data-btn":
            return {"display": "block"}
        else:
            return {"display": "none"}
    
    # Export Data with Loading State
    @app.callback(
        Output("download-data", "data"),
        Output("export-btn-text", "children"),
        Output("export-loading", "children"),
        Output("export-loading", "style"),
        Input("export-confirm-btn", "n_clicks"),
        State("export-format-dropdown", "value"),
        State("export-data-checklist", "value"),
        prevent_initial_call=True
    )
    def export_data(confirm_clicks, export_format, export_options):
        if not confirm_clicks or not export_options:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        # Show loading state
        loading_spinner = html.Span("⏳", style={"fontSize": "16px"})
        
        try:
            # Handle CSV format
            if export_format == "csv":
                if "kpi_data" in export_options:
                    csv_data, filename = export_kpi_data_to_csv(kpi_data, days)
                    return (
                        dict(content=csv_data, filename=filename),
                        "CSV Export Complete!",
                        loading_spinner,
                        {"display": "none"}
                    )
                elif "kpi_status" in export_options:
                    # Convert JSON status to CSV format
                    from data_loader import export_kpi_status_to_json
                    json_data, _ = export_kpi_status_to_json(kpi_data)
                    import json
                    import pandas as pd
                    status_data = json.loads(json_data)
                    
                    # Create CSV from status data
                    csv_rows = []
                    for kpi_key, kpi_info in status_data["kpi_status"].items():
                        csv_rows.append({
                            "KPI": kpi_info["label"],
                            "Value": kpi_info["value"],
                            "Unit": kpi_info["unit"],
                            "Status": kpi_info["status"]
                        })
                    
                    df = pd.DataFrame(csv_rows)
                    csv_data = df.to_csv(index=False)
                    filename = f"VizBrowser_KPI_Status_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    
                    return (
                        dict(content=csv_data, filename=filename),
                        "CSV Export Complete!",
                        loading_spinner,
                        {"display": "none"}
                    )
            
            # Handle JSON format
            elif export_format == "json":
                if "kpi_data" in export_options:
                    # Export KPI data directly to JSON format
                    json_data, filename = export_kpi_data_to_json(kpi_data, days)
                    
                    return (
                        dict(content=json_data, filename=filename),
                        "JSON Export Complete!",
                        loading_spinner,
                        {"display": "none"}
                    )
                    
                elif "kpi_status" in export_options:
                    json_data, filename = export_kpi_status_to_json(kpi_data)
                    return (
                        dict(content=json_data, filename=filename),
                        "JSON Export Complete!",
                        loading_spinner,
                        {"display": "none"}
                    )
            
            # If no valid combination found
            return (
                dash.no_update,
                "No data selected",
                loading_spinner,
                {"display": "none"}
            )
            
        except Exception as e:
            print(f"Export error: {e}")
            return (
                dash.no_update,
                "Export Failed",
                loading_spinner,
                {"display": "none"}
            )


def make_trend_figure(selected_kpi, kpi_data, days):
    """Create trend chart figure"""
    y = kpi_data[selected_kpi]
    if selected_kpi == 'oee':
        y = y * 100  # percent
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=y, mode="lines+markers", name=KPI_LABELS[selected_kpi],
        line=dict(color=SIEMENS_BLUE, width=3), 
        marker=dict(size=8, color=SIEMENS_ACCENT, line=dict(width=2, color=SIEMENS_BLUE))
    ))
    
    fig.update_layout(
        xaxis_title="Day",
        yaxis_title=f"{KPI_LABELS[selected_kpi]} ({KPI_UNITS[selected_kpi]})",
        plot_bgcolor=SIEMENS_CARD,
        paper_bgcolor=SIEMENS_CARD,
        font=dict(family=SIEMENS_FONT, size=18),
        margin=dict(l=30, r=20, t=36, b=36),
        height=370,
        hovermode="x unified",
        showlegend=False,
        xaxis=dict(title_font=dict(size=18), tickfont=dict(size=15)),
        yaxis=dict(title_font=dict(size=18), tickfont=dict(size=15)),
    )
    
    fig.update_xaxes(showgrid=True, gridcolor=SIEMENS_ACCENT, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=SIEMENS_ACCENT, zeroline=False)
    return fig

def build_multi_asset_view(multi_keys, view):
    """Build multi-asset comparison view"""
    from constants import LAYERED_ASSETS
    panels = []
    for key in multi_keys:
        name = next(
            (item["name"] for layer in LAYERED_ASSETS for item in layer["items"] if item["key"] == key),
            key
        )
        content = build_single_asset_view(key)
        panels.append(
            dash.html.Div(
                [dash.html.H3(name, style={"marginBottom": "8px", "color": SIEMENS_BLUE, "fontSize": "1.1rem"}), content],
                style={"flex": "1", "margin": "0 10px"}
            )
        )
    return dash.html.Div(panels, style={"display": "flex", "gap": "20px"})

def build_single_asset_view(asset_key):
    """Build single asset view"""
    import dash_vtk
    from dash import html
    
    if asset_key == "sim_flow":
        return html.Img(src="/assets/simulation.png", alt="Material Flow Plan", 
                       style={"height": "300px", "borderRadius": "8px", "boxShadow": "0 2px 8px rgba(44, 62, 80, 0.07)"})
    elif asset_key == "sim_resource":
        return html.Div("Resource Utilization Model visualization coming soon...", 
                       style={"color": SIEMENS_BLUE, "fontSize": "1.1rem", "padding": "20px"})
    elif asset_key == "mesh":
        mesh = load_festo_mesh()
        points, faces = mesh.points, mesh.faces.tolist()
        return html.Div([
            dash_vtk.View(
                children=[
                    dash_vtk.GeometryRepresentation(
                        children=[
                            dash_vtk.PolyData(
                                points=points.flatten().tolist(),
                                polys=faces
                            )
                        ],
                        property={"pointSize": 8}
                    )
                ],
                id="vtk-view",
                pickingModes=["hover"],
                style={"height": "400px", "width": "100%"},
                background=[1, 1, 1]
            ),
            html.Div(id="mesh-metadata-panel", style={"marginTop": "10px"})
        ])
    elif asset_key == "image":
        return build_image_gallery()
    elif asset_key == "pointcloud":
        pc = load_festo_pointcloud()
        xyz, rgb = process_point_cloud_colors(pc)
        return html.Div([
            dash_vtk.View(
                [
                    dash_vtk.PointCloudRepresentation(
                        xyz=xyz,
                        rgb=rgb,
                        property={"pointSize": 2}
                    )
                ],
                id="vtk-lidar-view",
                pickingModes=["hover"],
                background=[1, 1, 1],
                style={"height": "400px", "width": "100%"}
            )
        ])
    
    return "No view available."
