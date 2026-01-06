# Streamlit Cloud Setup Instructions

## OpenCV Dependency Fix

This app requires `opencv-python-headless` but `ultralytics` installs `opencv-python` as a dependency, which causes OpenGL library errors in headless environments.

### Solution for Streamlit Cloud

**Option 1: Use Streamlit Cloud's Advanced Settings (Recommended)**

1. Go to your Streamlit Cloud app settings
2. Look for "Advanced settings" or "Dependencies" section
3. Add a post-install command:
   ```bash
   pip uninstall opencv-python -y
   ```
4. Save and redeploy

**Option 2: Modify requirements.txt installation**

If Streamlit Cloud supports it, you can chain the installation:
```bash
pip install -r requirements.txt && pip uninstall opencv-python -y
```

**Option 3: Use a custom installation script**

Create a file called `post_install.sh`:
```bash
#!/bin/bash
pip install -r requirements.txt
pip uninstall opencv-python -y
```

Then configure Streamlit Cloud to run this script instead of directly installing requirements.txt.

### Verification

After deployment, the app should load without the OpenGL error. The app code will also attempt to automatically fix this issue on startup, but the installation-level fix is more reliable.

