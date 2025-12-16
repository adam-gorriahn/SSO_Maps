#!/usr/bin/env python3
"""
Pre-deploy mesh preprocessing script for Render.com
This script optimizes mesh files before deployment to reduce runtime memory usage.
Run this during the build phase to create pre-optimized mesh files.
"""
import os
import sys
import pyvista as pv
import gc

# Configuration
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
GARCHING_OBJ_PATH = os.path.join(ASSETS_DIR, "garching_cleaned.obj")
GARCHING_OPTIMIZED_PATH = os.path.join(ASSETS_DIR, "garching_optimized.obj")

# Get decimation settings from environment or use defaults
MESH_DECIMATION_FACTOR = float(os.getenv('MESH_DECIMATION_FACTOR', '0.95'))
MAX_MESH_FACES = int(os.getenv('MAX_MESH_FACES', '15000'))

def preprocess_garching_mesh():
    """Pre-process the Garching mesh to reduce file size and memory usage"""
    print("🔧 Starting mesh preprocessing...")
    
    if not os.path.exists(GARCHING_OBJ_PATH):
        print(f"⚠️  Warning: Source mesh not found at {GARCHING_OBJ_PATH}")
        print("   Skipping preprocessing. App will use runtime decimation.")
        return
    
    try:
        # Load original mesh
        print(f"📥 Loading mesh from {GARCHING_OBJ_PATH}")
        mesh = pv.read(GARCHING_OBJ_PATH)
        
        # Ensure triangulated
        if mesh.faces.size > 0 and mesh.faces[0] not in (3, 4):
            print("   Triangulating mesh...")
            mesh = mesh.triangulate()
            gc.collect()
        
        # Count original faces
        try:
            n_faces_original = mesh.n_faces
        except AttributeError:
            n_faces_original = mesh.faces.size // 4 if mesh.faces.size > 0 else 0
        
        print(f"📊 Original mesh: {n_faces_original:,} faces")
        
        # Apply decimation
        if MESH_DECIMATION_FACTOR > 0.0 and n_faces_original > 0:
            target_faces = max(1, int(n_faces_original * (1.0 - MESH_DECIMATION_FACTOR)))
            if target_faces < n_faces_original:
                reduction = 1.0 - (target_faces / n_faces_original)
                reduction = max(0.0, min(0.99, reduction))
                print(f"🔧 Applying decimation: {reduction:.2%} reduction (target: {target_faces:,} faces)")
                mesh = mesh.decimate(reduction)
                gc.collect()
        
        # Apply maximum face limit
        if MAX_MESH_FACES > 0:
            try:
                n_faces_after = mesh.n_faces
            except AttributeError:
                n_faces_after = mesh.faces.size // 4 if mesh.faces.size > 0 else 0
            
            if n_faces_after > MAX_MESH_FACES:
                reduction = 1.0 - (MAX_MESH_FACES / n_faces_after)
                reduction = max(0.0, min(0.99, reduction))
                print(f"🔧 Applying face limit: reducing to {MAX_MESH_FACES:,} faces ({reduction:.2%} reduction)")
                mesh = mesh.decimate(reduction)
                gc.collect()
        
        # Final face count
        try:
            n_faces_final = mesh.n_faces
        except AttributeError:
            n_faces_final = mesh.faces.size // 4 if mesh.faces.size > 0 else 0
        
        reduction_pct = ((n_faces_original - n_faces_final) / n_faces_original * 100) if n_faces_original > 0 else 0
        print(f"✅ Optimized mesh: {n_faces_final:,} faces ({reduction_pct:.1f}% reduction)")
        
        # Save optimized mesh
        print(f"💾 Saving optimized mesh to {GARCHING_OPTIMIZED_PATH}")
        mesh.save(GARCHING_OPTIMIZED_PATH)
        
        # Calculate file size reduction
        original_size = os.path.getsize(GARCHING_OBJ_PATH) / (1024 * 1024)  # MB
        optimized_size = os.path.getsize(GARCHING_OPTIMIZED_PATH) / (1024 * 1024)  # MB
        size_reduction = ((original_size - optimized_size) / original_size * 100) if original_size > 0 else 0
        
        print(f"📦 File size: {original_size:.2f} MB → {optimized_size:.2f} MB ({size_reduction:.1f}% reduction)")
        print("✅ Mesh preprocessing complete!")
        
        # Clean up
        del mesh
        gc.collect()
        
    except MemoryError:
        print("❌ Memory error during preprocessing. Using original mesh.")
        sys.exit(0)  # Don't fail the build, just use original
    except Exception as e:
        print(f"❌ Error preprocessing mesh: {e}")
        print("   App will use runtime decimation instead.")
        sys.exit(0)  # Don't fail the build

if __name__ == "__main__":
    preprocess_garching_mesh()
