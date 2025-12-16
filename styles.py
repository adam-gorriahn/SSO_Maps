"""
Styling constants and utility functions for the Agentic Dataverse Visualizer
"""
from constants import (
    SIEMENS_BG, SIEMENS_CARD, SIEMENS_ACCENT, SIEMENS_BLUE, 
    SIEMENS_FONT, SIEMENS_SHADOW, SIEMENS_DIVIDER, SIEMENS_STATUS
)

# --- Common Style Patterns ---
def get_card_style():
    """Standard card styling"""
    return {
        "background": SIEMENS_CARD,
        "borderRadius": "18px",
        "boxShadow": SIEMENS_SHADOW,
        "fontFamily": SIEMENS_FONT,
    }

def get_section_style():
    """Standard section styling"""
    return {
        "background": SIEMENS_BG,
        "fontFamily": SIEMENS_FONT,
    }

def get_title_style():
    """Standard title styling"""
    return {
        "fontWeight": "bold",
        "fontSize": "1.25rem",
        "color": SIEMENS_BLUE,
        "marginBottom": "2px",
        "fontFamily": SIEMENS_FONT
    }

def get_subtitle_style():
    """Standard subtitle styling"""
    return {
        "fontSize": "0.98rem",
        "color": "#888",
        "marginBottom": "12px",
        "fontFamily": SIEMENS_FONT
    }

def get_button_style(background_color=SIEMENS_BLUE, text_color="white"):
    """Standard button styling"""
    return {
        "background": background_color,
        "color": text_color,
        "border": "none",
        "borderRadius": "8px",
        "padding": "8px 16px",
        "cursor": "pointer",
        "fontWeight": "bold",
        "fontFamily": SIEMENS_FONT,
        "boxShadow": SIEMENS_SHADOW
    }

def get_control_button_style(background_color=SIEMENS_BLUE, text_color="white", size="24px"):
    """Control button styling for 3D viewer"""
    return {
        "fontSize": size,
        "padding": "8px 12px",
        "borderRadius": "8px",
        "background": background_color,
        "color": text_color,
        "border": "none",
        "cursor": "pointer",
        "boxShadow": SIEMENS_SHADOW
    }

def get_kpi_card_style():
    """KPI card styling"""
    return {
        "background": SIEMENS_CARD,
        "borderRadius": "12px",
        "boxShadow": SIEMENS_SHADOW,
        "padding": "14px 18px 12px 14px",
        "marginBottom": "12px",
        "width": "180px",
        "minWidth": "180px"
    }

def get_asset_tree_style():
    """Asset tree container styling"""
    return {
        "background": SIEMENS_CARD,
        "borderRadius": "18px",
        "boxShadow": SIEMENS_SHADOW,
        "padding": "24px 20px 18px 20px",
        "margin": "0 0 0 0",
        "width": "230px",
        "fontFamily": SIEMENS_FONT,
        "height": "100%",
        "minWidth": "210px"
    }

def get_view_panel_style():
    """View panel styling"""
    return {
        "background": SIEMENS_CARD,
        "borderRadius": "12px",
        "boxShadow": SIEMENS_SHADOW,
        "padding": "18px 18px 18px 18px",
        "width": "100%",
        "margin": "0 auto 0 28px",
        "flex": "1 1 0"
    }

def get_vtk_viewer_style():
    """VTK viewer styling"""
    return {
        "height": "400px",
        "width": "100%",
        "borderRadius": "10px",
        "boxShadow": SIEMENS_SHADOW
    }

def get_map_style():
    """Map styling"""
    return {
        "width": "100%",
        "height": "500px",
        "borderRadius": "10px",
        "boxShadow": SIEMENS_SHADOW
    }

def get_sidebar_style():
    """Sidebar container styling"""
    return {
        "width": "380px",
        "height": "100vh",
        "background": SIEMENS_CARD,
        "borderRight": f"1px solid {SIEMENS_DIVIDER}",
        "position": "fixed",
        "left": "0",
        "top": "0",
        "zIndex": "1000",
        "boxShadow": "2px 0 8px rgba(44, 62, 80, 0.1)",
        "fontFamily": SIEMENS_FONT,
        "overflowY": "auto",
        "transition": "transform 0.3s ease-in-out"
    }

def get_sidebar_collapsed_style():
    """Sidebar collapsed styling"""
    return {
        "width": "380px",
        "height": "100vh",
        "background": SIEMENS_CARD,
        "borderRight": f"1px solid {SIEMENS_DIVIDER}",
        "position": "fixed",
        "left": "-380px",
        "top": "0",
        "zIndex": "1000",
        "boxShadow": "2px 0 8px rgba(44, 62, 80, 0.1)",
        "fontFamily": SIEMENS_FONT,
        "overflowY": "auto",
        "transition": "transform 0.3s ease-in-out"
    }

def get_sidebar_header_style():
    """Sidebar header styling"""
    return {
        "padding": "20px 16px 16px 16px",
        "borderBottom": f"1px solid {SIEMENS_DIVIDER}",
        "background": SIEMENS_ACCENT,
        "position": "relative",
        "overflow": "hidden"
    }

def get_nav_button_style(active=False, level=1):
    """Unified navigation button styling with hierarchy levels"""
    # Unified styling with subtle level differences
    base_padding = "14px 20px"
    base_fontSize = "0.95rem"
    base_fontWeight = "600" if active else "500"
    
    # Level-specific adjustments
    if level == 1:
        padding = base_padding
        fontSize = base_fontSize
        fontWeight = base_fontWeight
        borderLeft = f"4px solid {SIEMENS_BLUE}" if active else "4px solid transparent"
        marginLeft = "0"
    elif level == 2:
        padding = "12px 20px"
        fontSize = "0.9rem"
        fontWeight = "500" if active else "400"
        borderLeft = f"3px solid {SIEMENS_BLUE}" if active else "3px solid transparent"
        marginLeft = "16px"
    else:  # level 3
        padding = "10px 20px"
        fontSize = "0.85rem"
        fontWeight = "500" if active else "400"
        borderLeft = f"2px solid {SIEMENS_BLUE}" if active else "2px solid transparent"
        marginLeft = "32px"
    
    base_style = {
        "width": "100%",
        "padding": padding,
        "marginLeft": marginLeft,
        "border": "none",
        "background": SIEMENS_CARD if not active else SIEMENS_ACCENT,
        "color": SIEMENS_BLUE if not active else "#000",
        "textAlign": "left",
        "cursor": "pointer",
        "fontFamily": SIEMENS_FONT,
        "fontSize": fontSize,
        "fontWeight": fontWeight,
        "borderLeft": borderLeft,
        "transition": "all 0.3s ease",
        "display": "flex",
        "alignItems": "center",
        "gap": "12px",
        "borderRadius": "0 8px 8px 0" if level > 1 else "8px",
        "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.1)" if active else "none",
        "transform": "translateX(2px)" if active else "translateX(0)"
    }
    return base_style

def get_nav_button_hover_style():
    """Navigation button hover styling"""
    return {
        "background": SIEMENS_ACCENT,
        "borderLeft": f"4px solid {SIEMENS_BLUE}"
    }

def get_main_content_style():
    """Main content area styling with sidebar offset"""
    return {
        "marginLeft": "280px",
        "minHeight": "100vh",
        "background": SIEMENS_BG,
        "fontFamily": SIEMENS_FONT,
        "scrollBehavior": "smooth"
    }

def get_kpi_status_indicator_style(status):
    """KPI status indicator styling"""
    from constants import KPI_STATUS_COLORS
    
    return {
        "display": "inline-flex",
        "alignItems": "center",
        "justifyContent": "center",
        "width": "24px",
        "height": "24px",
        "borderRadius": "50%",
        "background": KPI_STATUS_COLORS.get(status, KPI_STATUS_COLORS['normal']),
        "color": "white",
        "fontSize": "12px",
        "fontWeight": "bold",
        "marginLeft": "8px",
        "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.2)"
    }

def get_kpi_card_with_status_style(status):
    """KPI card styling with status indicator"""
    from constants import KPI_STATUS_COLORS
    
    base_style = get_kpi_card_style()
    status_color = KPI_STATUS_COLORS.get(status, KPI_STATUS_COLORS['normal'])
    
    # Add subtle border color based on status
    base_style["borderLeft"] = f"4px solid {status_color}"
    base_style["background"] = f"linear-gradient(135deg, {SIEMENS_CARD} 0%, {status_color}08 100%)"
    
    return base_style

def get_export_button_style():
    """Export button styling"""
    return {
        "background": SIEMENS_BLUE,
        "color": "white",
        "border": "none",
        "borderRadius": "8px",
        "padding": "10px 16px",
        "fontSize": "14px",
        "fontWeight": "600",
        "cursor": "pointer",
        "fontFamily": SIEMENS_FONT,
        "boxShadow": SIEMENS_SHADOW,
        "transition": "all 0.3s ease",
        "display": "inline-flex",
        "alignItems": "center",
        "gap": "8px"
    }

def get_share_button_style():
    """Share button styling"""
    return {
        "background": SIEMENS_ACCENT,
        "color": SIEMENS_BLUE,
        "border": f"2px solid {SIEMENS_BLUE}",
        "borderRadius": "8px",
        "padding": "10px 16px",
        "fontSize": "14px",
        "fontWeight": "600",
        "cursor": "pointer",
        "fontFamily": SIEMENS_FONT,
        "boxShadow": SIEMENS_SHADOW,
        "transition": "all 0.3s ease",
        "display": "inline-flex",
        "alignItems": "center",
        "gap": "8px"
    }

def get_export_modal_style():
    """Export modal styling"""
    return {
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "background": SIEMENS_CARD,
        "borderRadius": "12px",
        "boxShadow": "0 8px 32px rgba(0, 0, 0, 0.2)",
        "padding": "24px",
        "minWidth": "400px",
        "maxWidth": "500px",
        "zIndex": "1000",
        "fontFamily": SIEMENS_FONT
    }

def get_modal_overlay_style():
    """Modal overlay styling"""
    return {
        "position": "fixed",
        "top": "0",
        "left": "0",
        "width": "100%",
        "height": "100%",
        "background": "rgba(0, 0, 0, 0.5)",
        "zIndex": "999"
    }

def get_loading_spinner_style():
    """Loading spinner styling"""
    return {
        "display": "inline-block",
        "width": "20px",
        "height": "20px",
        "border": f"3px solid {SIEMENS_ACCENT}",
        "borderRadius": "50%",
        "borderTopColor": SIEMENS_BLUE,
        "animation": "spin 1s ease-in-out infinite",
        "marginRight": "8px"
    }

def get_smooth_transition_style():
    """Smooth transition styling for interactive elements"""
    return {
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "transform": "translateZ(0)"  # Hardware acceleration
    }
