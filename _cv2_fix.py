"""
OpenCV import fix module.
This module ensures opencv-python-headless is used instead of opencv-python.
It must be imported before any module that imports cv2 (like ultralytics).
"""
import subprocess
import sys
import os

def ensure_headless_opencv():
    """
    Ensure opencv-python-headless is used instead of opencv-python.
    This function uninstalls opencv-python if present and pre-loads cv2 from headless.
    Returns True if successful, False otherwise.
    """
    max_attempts = 3
    for attempt in range(max_attempts):
        # Uninstall opencv-python if it exists
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'uninstall', 'opencv-python', '-y', '--quiet'],
                capture_output=True,
                timeout=30,
                check=False
            )
        except Exception:
            pass
        
        # Clear any existing cv2 imports from cache
        cv2_modules = [k for k in list(sys.modules.keys()) if k.startswith('cv2')]
        for mod in cv2_modules:
            try:
                del sys.modules[mod]
            except KeyError:
                pass
        
        # Pre-import cv2 to ensure headless version is loaded
        # This must succeed before ultralytics tries to import it
        try:
            import cv2
            # Verify the import worked by checking a basic attribute
            # If it's the problematic opencv-python, it would have failed with OpenGL error
            # If we get here, cv2 is imported successfully from headless
            return True
        except (ImportError, OSError) as e:
            error_str = str(e)
            if 'libGL.so.1' in error_str or 'OpenGL' in error_str:
                # Still have the problematic version - will retry
                if attempt < max_attempts - 1:
                    continue
                else:
                    return False
            else:
                # Different error - might be that opencv-python-headless isn't installed
                # Re-raise to see the actual error
                raise
    
    return False

# Run the fix when this module is imported
_cv2_fixed = ensure_headless_opencv()

