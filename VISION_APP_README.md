# Object Detection Vision App

A Streamlit application that uses DETR (Detection Transformer) from Hugging Face to detect objects in images with bounding boxes. This solution is optimized for cloud deployment (Streamlit Cloud) and doesn't require system-level dependencies.

## Features

- 🖼️ **Image Upload**: Upload images in various formats (JPG, PNG, BMP, WEBP)
- 🔍 **Object Detection**: Detects 80+ object classes including:
  - People (person)
  - Food items (bottle, cup, bowl, banana, apple, pizza, etc.)
  - Containers (box, bag, backpack, suitcase)
  - Vehicles (car, truck, bus, motorcycle, bicycle)
  - Animals (cat, dog, bird, horse, etc.)
  - Furniture (chair, couch, bed, table)
  - And many more!
- 📦 **Bounding Boxes**: Visual bounding boxes around detected objects
- ⚙️ **Adjustable Confidence**: Slider to adjust detection confidence threshold
- 📊 **Statistics**: Shows count and details of detected objects
- 📥 **Download**: Download annotated images with bounding boxes

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

**Note**: The first time you run the app, the DETR model will automatically download from Hugging Face (~150MB). This is a one-time download and will be cached.

## Usage

Run the Streamlit app:
```bash
streamlit run vision_app.py
```

The app will open in your default web browser. Then:
1. Upload an image using the file uploader
2. Adjust the confidence threshold if needed (default: 0.25)
3. Click "Detect Objects" to process the image
4. View the results with bounding boxes and object statistics
5. Download the annotated image if desired

## Technical Details

- **Model**: DETR-ResNet-50 (Detection Transformer)
- **Framework**: Hugging Face Transformers
- **Dataset**: Pre-trained on COCO dataset
- **Classes**: 91 object classes
- **Cloud-Friendly**: No system dependencies (libGL, OpenCV system libs), works on Streamlit Cloud

## Requirements

- Python 3.8+
- Streamlit
- Transformers (Hugging Face)
- PyTorch
- Pillow (PIL)
- NumPy

## Notes

- The model is cached in memory after first load for faster subsequent detections
- Larger images may take longer to process
- Lower confidence thresholds will detect more objects but may include false positives
- Higher confidence thresholds will be more selective but may miss some objects
- **Cloud Deployment**: This solution is optimized for Streamlit Cloud and doesn't require system libraries like libGL.so.1

