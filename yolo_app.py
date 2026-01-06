# PERMANENT FIX: Import cv2 fix module FIRST to ensure opencv-python-headless is used
# This must happen before any other imports that might trigger cv2 import
try:
    import _cv2_fix  # This module handles the OpenCV dependency fix
except Exception:
    # If the fix module fails, we'll handle it below
    pass

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Now import ultralytics - cv2 should already be loaded from headless
import sys
try:
    from ultralytics import YOLO
except (ImportError, OSError) as e:
    error_msg = str(e)
    if 'libGL.so.1' in error_msg or 'OpenGL' in error_msg or 'cv2' in error_msg.lower():
        # Last resort: try to fix and reload using the fix module
        try:
            # Re-run the fix
            import _cv2_fix
            _cv2_fix.ensure_headless_opencv()
            # Clear ultralytics modules
            ultralytics_modules = [k for k in list(sys.modules.keys()) if 'ultralytics' in k]
            for mod in ultralytics_modules:
                del sys.modules[mod]
            # Try importing again
            from ultralytics import YOLO
        except Exception as final_error:
            st.error(f"""
            **⚠️ OpenCV OpenGL Dependency Error**
            
            The `opencv-python` package requires OpenGL libraries (`libGL.so.1`) that are not available.
            
            **Automatic fix attempted but failed.**
            
            **Permanent Solution for Streamlit Cloud:**
            
            You need to configure your deployment to uninstall `opencv-python` after installation.
            
            **Option 1:** Contact Streamlit Cloud support and ask them to add this post-install command:
            ```bash
            pip uninstall opencv-python -y
            ```
            
            **Option 2:** If Streamlit Cloud supports advanced settings, add the above command as a post-install step.
            
            **Error:** {str(final_error)}
            """)
            st.stop()
    else:
        raise

import io

# Page configuration
st.set_page_config(
    page_title="Object Detection App",
    page_icon="🔍",
    layout="wide"
)

# Title
st.title("🔍 Food Product Detection with YOLO")
st.markdown("Upload an image to detect food product categories using YOLO model!")

# Initialize session state for model
@st.cache_resource
def load_model():
    """Load YOLO model (cached to avoid reloading)"""
    try:
        # Load the custom YOLO model
        model = YOLO("my_model.pt")
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Load model
model = load_model()

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.05,
        help="Minimum confidence score for detected objects"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Supported Objects")
    st.markdown("""
    The YOLO model can detect the following 6 classes:
    - **Produce**
    - **Prepared - Trays**
    - **Prepared - Individually Packaged**
    - **Non-Perishable**
    - **Meat & Protein**
    - **Dairy**
    - **Baked Goods**
    """)

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.header("📤 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['jpg', 'jpeg', 'png', 'bmp', 'webp'],
        help="Upload an image file to detect objects"
    )
    
    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_container_width=True)
        
        # Detection button
        if st.button("🔍 Detect Objects", type="primary"):
            if model is not None:
                with st.spinner("🔄 Processing image and detecting objects..."):
                    try:
                        # Convert PIL image to numpy array for YOLO
                        image_array = np.array(image)
                        
                        # Run YOLO inference
                        results = model.predict(
                            source=image_array,
                            conf=confidence_threshold,
                            verbose=False
                        )
                        
                        # Process results
                        annotated_image = image.copy()
                        draw = ImageDraw.Draw(annotated_image)
                        detected_objects = []
                        
                        # Get the first result (since we're processing a single image)
                        result = results[0]
                        
                        # Process bounding boxes
                        if result.boxes is not None and len(result.boxes) > 0:
                            boxes = result.boxes
                            
                            for i in range(len(boxes)):
                                # Get box coordinates (xyxy format)
                                box = boxes.xyxy[i].cpu().numpy()
                                confidence = float(boxes.conf[i].cpu().numpy())
                                class_id = int(boxes.cls[i].cpu().numpy())
                                
                                # Get class name
                                class_name = result.names[class_id]
                                
                                # Convert box coordinates to list
                                box_coords = [float(box[0]), float(box[1]), float(box[2]), float(box[3])]
                                
                                # Draw rectangle
                                draw.rectangle(box_coords, outline="red", width=3)
                                
                                # Prepare label text
                                label_text = f"{class_name}: {confidence:.3f}"
                                
                                # Get text dimensions
                                bbox = draw.textbbox((0, 0), label_text)
                                text_width = bbox[2] - bbox[0]
                                text_height = bbox[3] - bbox[1]
                                
                                # Draw text background
                                draw.rectangle(
                                    [box_coords[0], box_coords[1] - text_height - 4, 
                                     box_coords[0] + text_width + 4, box_coords[1]],
                                    fill="red"
                                )
                                
                                # Draw text
                                draw.text(
                                    (box_coords[0] + 2, box_coords[1] - text_height - 2), 
                                    label_text, 
                                    fill="white"
                                )
                                
                                detected_objects.append({
                                    'label': class_name,
                                    'score': confidence,
                                    'box': box_coords
                                })
                        
                        # Store results in session state
                        st.session_state.detection_results = {
                            'image': annotated_image,
                            'objects': detected_objects,
                            'count': len(detected_objects)
                        }
                        
                    except Exception as e:
                        st.error(f"❌ Error during detection: {str(e)}")
                        st.session_state.detection_results = None
            else:
                st.error("Model not loaded. Please check the error message above.")

with col2:
    st.header("📊 Detection Results")
    
    if 'detection_results' in st.session_state and st.session_state.detection_results is not None:
        results = st.session_state.detection_results
        
        # Display annotated image
        st.image(results['image'], caption="Detected Objects", use_container_width=True)
        
        # Display statistics
        st.success(f"✅ Detected {results['count']} object(s)")
        
        # Display detected objects list
        if results['count'] > 0:
            st.markdown("### 📋 Detected Objects:")
            
            # Count objects by class
            detected_classes = {}
            for obj in results['objects']:
                class_name = obj['label']
                confidence = obj['score']
                
                if class_name not in detected_classes:
                    detected_classes[class_name] = []
                detected_classes[class_name].append(confidence)
            
            # Display in a nice format
            for class_name, confidences in sorted(detected_classes.items()):
                count = len(confidences)
                avg_conf = np.mean(confidences)
                st.markdown(f"**{class_name.capitalize()}**: {count} detected (avg confidence: {avg_conf:.2%})")
            
            # Download button for annotated image
            img_buffer = io.BytesIO()
            results['image'].save(img_buffer, format='PNG')
            st.download_button(
                label="📥 Download Annotated Image",
                data=img_buffer.getvalue(),
                file_name="detected_objects.png",
                mime="image/png"
            )
        else:
            st.info("No objects detected. Try lowering the confidence threshold or upload a different image.")
    else:
        st.info("👈 Upload an image and click 'Detect Objects' to see results here.")

# Footer
st.markdown("---")
st.markdown("### ℹ️ About")
st.markdown("""
This app uses **YOLO** (You Only Look Once) from Ultralytics, a state-of-the-art object detection model.
The model is trained to detect 6 specific food product categories with high accuracy and speed.

**Model**: Custom YOLO Model (my_model.pt)
**Framework**: Ultralytics YOLO
**Classes**: Produce, Prepared - Trays, Prepared - Individually Packaged, Non-Perishable, Meat & Protein, Dairy, Baked Goods
""")

