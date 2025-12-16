"""
Data loading and processing utilities
"""
import numpy as np
import pyvista as pv
import pandas as pd
import json
import base64
from datetime import datetime
from functools import lru_cache
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from constants import (
    FESTO_PLY_PATH, FESTO_OBJ_PATH, GARCHING_OBJ_PATH, POINT_CLOUD_MAX_POINTS, 
    KPI_DAYS, KPI_LABELS, EXPORT_FILENAME_PREFIX, EXPORT_TIMESTAMP_FORMAT,
    MESH_DECIMATION_FACTOR, MAX_MESH_FACES
)

@lru_cache(maxsize=1)
def load_festo_pointcloud():
    """Load and cache Festo point cloud data"""
    pc = pv.read(FESTO_PLY_PATH)
    if pc.n_points > POINT_CLOUD_MAX_POINTS:
        sampled_ids = np.random.choice(pc.n_points, size=POINT_CLOUD_MAX_POINTS, replace=False)
        pc = pc.extract_points(sampled_ids)
    return pc

@lru_cache(maxsize=1)
def load_festo_mesh():
    """Load and cache Festo mesh data"""
    mesh = pv.read(FESTO_OBJ_PATH)
    if mesh.faces.size > 0 and mesh.faces[0] not in (3, 4):
        mesh = mesh.triangulate()
    return mesh

@lru_cache(maxsize=1)
def load_garching_mesh():
    """Load and cache Garching mesh data with aggressive memory optimization"""
    import gc
    
    try:
        mesh = pv.read(GARCHING_OBJ_PATH)
        
        # Ensure triangulated
        if mesh.faces.size > 0 and mesh.faces[0] not in (3, 4):
            mesh = mesh.triangulate()
        
        # Count current faces - PyVista provides n_faces property
        try:
            n_faces_original = mesh.n_faces
        except AttributeError:
            # Fallback: estimate from faces array size (format: [n, v0, v1, v2, ...])
            n_faces_original = mesh.faces.size // 4 if mesh.faces.size > 0 else 0
        
        print(f"📊 Original mesh: {n_faces_original} faces")
        
        # Apply decimation if mesh is too large or decimation factor is set
        if MESH_DECIMATION_FACTOR > 0.0 and n_faces_original > 0:
            target_faces = max(1, int(n_faces_original * (1.0 - MESH_DECIMATION_FACTOR)))
            if target_faces < n_faces_original:
                try:
                    # PyVista decimate takes reduction factor (0.0 to 1.0)
                    reduction = 1.0 - (target_faces / n_faces_original)
                    reduction = max(0.0, min(0.99, reduction))  # Clamp between 0 and 0.99
                    print(f"🔧 Applying decimation: {reduction:.2%} reduction (target: {target_faces} faces)")
                    mesh = mesh.decimate(reduction)
                    # Force garbage collection after decimation
                    gc.collect()
                except Exception as e:
                    print(f"⚠️ Warning: Mesh decimation failed: {e}. Using original mesh.")
        
        # Apply maximum face limit if set
        if MAX_MESH_FACES > 0:
            # Recalculate faces after decimation
            try:
                n_faces_after = mesh.n_faces
            except AttributeError:
                n_faces_after = mesh.faces.size // 4 if mesh.faces.size > 0 else 0
            
            if n_faces_after > MAX_MESH_FACES:
                try:
                    reduction = 1.0 - (MAX_MESH_FACES / n_faces_after)
                    reduction = max(0.0, min(0.99, reduction))
                    print(f"🔧 Applying face limit: reducing to {MAX_MESH_FACES} faces ({reduction:.2%} reduction)")
                    mesh = mesh.decimate(reduction)
                    gc.collect()
                except Exception as e:
                    print(f"⚠️ Warning: Mesh face limit reduction failed: {e}. Using current mesh.")
        
        # Final face count
        try:
            n_faces_final = mesh.n_faces
        except AttributeError:
            n_faces_final = mesh.faces.size // 4 if mesh.faces.size > 0 else 0
        
        reduction_pct = ((n_faces_original - n_faces_final) / n_faces_original * 100) if n_faces_original > 0 else 0
        print(f"✅ Final mesh: {n_faces_final} faces ({reduction_pct:.1f}% reduction from original)")
        
        return mesh
    except MemoryError:
        print("❌ Memory error loading mesh. Try increasing MESH_DECIMATION_FACTOR or reducing MAX_MESH_FACES")
        raise
    except Exception as e:
        print(f"❌ Error loading mesh: {e}")
        raise

def simulate_kpi(seed=0):
    """Generate simulated KPI data for a 600m² shopfloor"""
    days = np.arange(1, KPI_DAYS + 1)
    rng = np.random.default_rng(seed)
    
    # Realistic values for a 600m² industrial shopfloor
    return {
        # Energy: ~15-25 kWh/m²/year for industrial facilities, scaled to daily
        'energy_spend': 25 + 5 * np.sin(days / 4) + rng.normal(0, 2, size=days.shape),  # 20-30 kWh/day
        # Carbon intensity: typical for German grid mix
        'carbon_intensity': 0.32 + 0.04 * np.cos(days / 5) + rng.normal(0, 0.01, size=days.shape),  # kgCO₂/kWh
        # OEE: typical for manufacturing
        'oee': 0.75 + 0.08 * np.sin(days / 6) + rng.normal(0, 0.01, size=days.shape),  # 67%-83%
        # Compressed air: ~0.1-0.2 Nm³/m²/day for industrial use
        'compressed_air': 60 + 15 * np.sin(days / 7) + rng.normal(0, 3, size=days.shape),  # 45-75 Nm³/day
        # Water: ~0.01-0.02 m³/m²/day for industrial processes
        'water_usage': 9 + 3 * np.sin(days / 8) + rng.normal(0, 0.5, size=days.shape)  # 6-12 m³/day
    }

def get_latest_kpi_snapshot(kpi_data):
    """Get latest KPI values for display"""
    idx = -1  # last day in simulated series
    return {
        "Energy Spend": f"{kpi_data['energy_spend'][idx]:.1f} kWh",
        "Carbon Intensity": f"{kpi_data['carbon_intensity'][idx]:.3f} kgCO₂/kWh",
        "OEE": f"{kpi_data['oee'][idx]*100:.1f}%",
        "Compressed Air": f"{kpi_data['compressed_air'][idx]:.0f} Nm³",
        "Water Usage": f"{kpi_data['water_usage'][idx]:.1f} m³",
    }

def calculate_kpi_status(kpi_data, kpi_key, day_idx=-1):
    """Calculate KPI status based on thresholds"""
    from constants import KPI_THRESHOLDS
    
    if kpi_key not in KPI_THRESHOLDS:
        return 'normal'
    
    value = kpi_data[kpi_key][day_idx]
    thresholds = KPI_THRESHOLDS[kpi_key]
    
    # For OEE, lower values are worse (inverse logic)
    if kpi_key == 'oee':
        if value < thresholds['critical']:
            return 'critical'
        elif value < thresholds['warning']:
            return 'warning'
        else:
            return 'normal'
    else:
        # For other KPIs, higher values are worse (normal logic)
        if value > thresholds['critical']:
            return 'critical'
        elif value > thresholds['warning']:
            return 'warning'
        else:
            return 'normal'

def get_kpi_status_summary(kpi_data, day_idx=-1):
    """Get status summary for all KPIs"""
    from constants import KPI_LABELS, KPI_STATUS_ICONS
    
    status_summary = {}
    for kpi_key in KPI_LABELS:
        status = calculate_kpi_status(kpi_data, kpi_key, day_idx)
        status_summary[kpi_key] = {
            'status': status,
            'icon': KPI_STATUS_ICONS[status],
            'value': kpi_data[kpi_key][day_idx]
        }
    
    return status_summary

def get_point_cloud_info(points):
    """Get point cloud statistics"""
    min_xyz = points.min(axis=0)
    max_xyz = points.max(axis=0)
    return {
        "count": len(points),
        "min": min_xyz,
        "max": max_xyz
    }

def process_point_cloud_colors(pc):
    """Process point cloud color data for visualization"""
    points = pc.points
    
    if 'RGB' in pc.point_data:
        colors = pc.point_data['RGB']
        if colors.ndim == 2 and colors.shape[1] == 3:
            colors = colors.astype(np.float32) / 255.0
        elif colors.ndim == 1:
            rgba = colors.astype(np.uint32)
            r = ((rgba >> 16) & 0xFF).astype(np.float32)
            g = ((rgba >> 8) & 0xFF).astype(np.float32)
            b = (rgba & 0xFF).astype(np.float32)
            colors = np.vstack((r, g, b)).T.astype(np.float32) / 255.0
        else:
            colors = np.ones((points.shape[0], 3), dtype=np.float32)
    elif all(k in pc.point_data for k in ('red', 'green', 'blue')):
        r = pc.point_data['red'].astype(np.float32)
        g = pc.point_data['green'].astype(np.float32)
        b = pc.point_data['blue'].astype(np.float32)
        colors = np.vstack((r, g, b)).T.astype(np.float32) / 255.0
    else:
        colors = np.ones((points.shape[0], 3), dtype=np.float32)
    
    return points.ravel().tolist(), [float(v) for v in colors.ravel()]

def export_kpi_data_to_csv(kpi_data, days):
    """Export KPI data to CSV format"""
    from constants import KPI_LABELS, KPI_UNITS
    
    # Create DataFrame
    df_data = {'Day': days}
    for kpi_key in KPI_LABELS:
        if kpi_key == 'oee':
            df_data[KPI_LABELS[kpi_key]] = kpi_data[kpi_key] * 100  # Convert to percentage
        else:
            df_data[KPI_LABELS[kpi_key]] = kpi_data[kpi_key]
    
    df = pd.DataFrame(df_data)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime(EXPORT_TIMESTAMP_FORMAT)
    filename = f"{EXPORT_FILENAME_PREFIX}_KPI_Data_{timestamp}.csv"
    
    # Convert to CSV string
    csv_string = df.to_csv(index=False)
    
    return csv_string, filename

def export_kpi_data_to_json(kpi_data, days):
    """Export KPI data to JSON format"""
    from constants import KPI_LABELS, KPI_UNITS
    
    # Create structured JSON data
    json_data = {
        "export_timestamp": datetime.now().isoformat(),
        "data_source": "VizBrowser KPI Dashboard",
        "data_type": "time_series",
        "kpi_data": []
    }
    
    # Convert to list of records (one per day)
    for day_idx, day in enumerate(days):
        day_record = {"day": int(day)}
        
        for kpi_key in KPI_LABELS:
            value = kpi_data[kpi_key][day_idx]
            if kpi_key == 'oee':
                value = value * 100  # Convert to percentage
            
            day_record[kpi_key] = {
                "label": KPI_LABELS[kpi_key],
                "value": float(value),
                "unit": KPI_UNITS[kpi_key]
            }
        
        json_data["kpi_data"].append(day_record)
    
    # Add metadata about KPIs
    json_data["kpi_metadata"] = {}
    for kpi_key in KPI_LABELS:
        json_data["kpi_metadata"][kpi_key] = {
            "label": KPI_LABELS[kpi_key],
            "unit": KPI_UNITS[kpi_key],
            "thresholds": get_kpi_thresholds(kpi_key)
        }
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime(EXPORT_TIMESTAMP_FORMAT)
    filename = f"{EXPORT_FILENAME_PREFIX}_KPI_Data_{timestamp}.json"
    
    return json.dumps(json_data, indent=2), filename

def export_kpi_status_to_json(kpi_data, day_idx=-1):
    """Export current KPI status to JSON format"""
    from constants import KPI_LABELS, KPI_UNITS
    
    status_data = {
        "export_timestamp": datetime.now().isoformat(),
        "data_source": "VizBrowser KPI Dashboard",
        "kpi_status": {}
    }
    
    for kpi_key in KPI_LABELS:
        status = calculate_kpi_status(kpi_data, kpi_key, day_idx)
        value = kpi_data[kpi_key][day_idx]
        
        if kpi_key == 'oee':
            value = value * 100  # Convert to percentage
        
        status_data["kpi_status"][kpi_key] = {
            "label": KPI_LABELS[kpi_key],
            "value": float(value),
            "unit": KPI_UNITS[kpi_key],
            "status": status,
            "thresholds": get_kpi_thresholds(kpi_key)
        }
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime(EXPORT_TIMESTAMP_FORMAT)
    filename = f"{EXPORT_FILENAME_PREFIX}_KPI_Status_{timestamp}.json"
    
    return json.dumps(status_data, indent=2), filename

def get_kpi_thresholds(kpi_key):
    """Get KPI thresholds for export"""
    from constants import KPI_THRESHOLDS
    return KPI_THRESHOLDS.get(kpi_key, {})

def export_asset_info_to_json():
    """Export asset information to JSON format"""
    from constants import LAYERED_ASSETS, ASSET_NAME_MAP
    
    asset_data = {
        "export_timestamp": datetime.now().isoformat(),
        "data_source": "VizBrowser Asset Tree",
        "assets": {}
    }
    
    for layer in LAYERED_ASSETS:
        layer_name = layer["layer"]
        asset_data["assets"][layer_name] = {
            "layer_type": layer_name,
            "color": layer["color"],
            "items": []
        }
        
        for item in layer["items"]:
            asset_info = {
                "key": item["key"],
                "name": item["name"],
                "display_name": ASSET_NAME_MAP.get(item["key"], item["name"]),
                "type": layer_name
            }
            asset_data["assets"][layer_name]["items"].append(asset_info)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime(EXPORT_TIMESTAMP_FORMAT)
    filename = f"{EXPORT_FILENAME_PREFIX}_Asset_Info_{timestamp}.json"
    
    return json.dumps(asset_data, indent=2), filename

def create_shareable_view_state(active_view, selected_assets=None, kpi_data=None, day_idx=-1):
    """Create shareable view state"""
    view_state = {
        "export_timestamp": datetime.now().isoformat(),
        "data_source": "VizBrowser Share",
        "view_state": {
            "active_view": active_view,
            "selected_assets": selected_assets or [],
            "kpi_snapshot": None
        }
    }
    
    # Add KPI snapshot if available
    if kpi_data is not None:
        from constants import KPI_LABELS, KPI_UNITS
        kpi_snapshot = {}
        for kpi_key in KPI_LABELS:
            value = kpi_data[kpi_key][day_idx]
            if kpi_key == 'oee':
                value = value * 100
            kpi_snapshot[kpi_key] = {
                "label": KPI_LABELS[kpi_key],
                "value": float(value),
                "unit": KPI_UNITS[kpi_key],
                "status": calculate_kpi_status(kpi_data, kpi_key, day_idx)
            }
        view_state["view_state"]["kpi_snapshot"] = kpi_snapshot
    
    return json.dumps(view_state, indent=2)

def generate_shareable_link(view_state_json):
    """Generate a shareable link (base64 encoded state)"""
    # Encode the view state as base64
    encoded_state = base64.b64encode(view_state_json.encode()).decode()
    
    # In a real application, this would be stored in a database and return a short URL
    # For now, we'll return the encoded state that could be used in a URL parameter
    shareable_link = f"https://vizbrowser.example.com/share?state={encoded_state}"
    
    return shareable_link

# --- Advanced Analytics Functions ---

def calculate_descriptive_statistics(kpi_data, kpi_key):
    """Calculate comprehensive descriptive statistics for a KPI"""
    data = kpi_data[kpi_key]
    
    stats_dict = {
        'count': len(data),
        'mean': float(np.mean(data)),
        'median': float(np.median(data)),
        'std': float(np.std(data)),
        'var': float(np.var(data)),
        'min': float(np.min(data)),
        'max': float(np.max(data)),
        'range': float(np.max(data) - np.min(data)),
        'q25': float(np.percentile(data, 25)),
        'q75': float(np.percentile(data, 75)),
        'iqr': float(np.percentile(data, 75) - np.percentile(data, 25)),
        'skewness': float(stats.skew(data)),
        'kurtosis': float(stats.kurtosis(data)),
        'cv': float(np.std(data) / np.mean(data)) if np.mean(data) != 0 else 0  # Coefficient of variation
    }
    
    return stats_dict

def perform_correlation_analysis(kpi_data):
    """Calculate correlation matrix between all KPIs"""
    # Create DataFrame from KPI data
    df = pd.DataFrame(kpi_data)
    
    # Calculate Pearson correlation matrix
    correlation_matrix = df.corr()
    
    # Convert to dictionary format for easier handling
    corr_dict = {}
    for i, kpi1 in enumerate(KPI_LABELS.keys()):
        corr_dict[kpi1] = {}
        for j, kpi2 in enumerate(KPI_LABELS.keys()):
            corr_dict[kpi1][kpi2] = float(correlation_matrix.iloc[i, j])
    
    return corr_dict

def generate_forecast(kpi_data, kpi_key, forecast_days=7):
    """Generate simple linear regression forecast for a KPI"""
    data = kpi_data[kpi_key]
    days = np.arange(1, len(data) + 1)
    
    # Prepare data for regression
    X = days.reshape(-1, 1)
    y = data
    
    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate forecast
    future_days = np.arange(len(data) + 1, len(data) + forecast_days + 1)
    X_future = future_days.reshape(-1, 1)
    forecast = model.predict(X_future)
    
    # Calculate confidence intervals (simplified)
    residuals = y - model.predict(X)
    std_error = np.std(residuals)
    confidence_interval = 1.96 * std_error  # 95% confidence
    
    forecast_data = {
        'historical_days': days.tolist(),
        'historical_values': data.tolist(),
        'forecast_days': future_days.tolist(),
        'forecast_values': forecast.tolist(),
        'upper_bound': (forecast + confidence_interval).tolist(),
        'lower_bound': (forecast - confidence_interval).tolist(),
        'r_squared': float(model.score(X, y)),
        'slope': float(model.coef_[0]),
        'intercept': float(model.intercept_)
    }
    
    return forecast_data

def detect_anomalies(kpi_data, kpi_key, threshold=2.0):
    """Detect anomalies using Z-score method"""
    data = kpi_data[kpi_key]
    days = np.arange(1, len(data) + 1)
    
    # Calculate Z-scores
    z_scores = np.abs(stats.zscore(data))
    
    # Find anomalies
    anomalies = z_scores > threshold
    anomaly_indices = np.where(anomalies)[0]
    
    anomaly_data = {
        'days': days[anomaly_indices].tolist(),
        'values': data[anomaly_indices].tolist(),
        'z_scores': z_scores[anomaly_indices].tolist(),
        'threshold': threshold,
        'total_anomalies': len(anomaly_indices),
        'anomaly_rate': len(anomaly_indices) / len(data)
    }
    
    return anomaly_data

def calculate_trend_analysis(kpi_data, kpi_key):
    """Calculate trend analysis using linear regression"""
    data = kpi_data[kpi_key]
    
    # Linear trend analysis
    days = np.arange(1, len(data) + 1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(days, data)
    
    # Simple trend detection using first and last values
    first_half = np.mean(data[:len(data)//2])
    second_half = np.mean(data[len(data)//2:])
    trend_strength = (second_half - first_half) / first_half if first_half != 0 else 0
    
    trend_data = {
        'linear_slope': float(slope),
        'linear_r_squared': float(r_value ** 2),
        'linear_pvalue': float(p_value),
        'trend_strength': float(trend_strength),
        'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
        'trend_significance': 'significant' if p_value < 0.05 else 'not significant'
    }
    
    return trend_data
