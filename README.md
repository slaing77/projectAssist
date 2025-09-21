# projectAssist
Materials for presentation

## Image Library

A comprehensive Python image processing library designed for presentation materials and media handling. This library provides an easy-to-use interface for common image operations including loading, saving, transformation, and format conversion.

### Features

- **Image Loading & Saving**: Support for multiple formats (JPEG, PNG, BMP, GIF, TIFF, WebP)
- **Image Transformations**: Resize, rotate, crop with intelligent aspect ratio handling
- **Format Conversion**: Convert between different image formats with proper color space handling
- **Filters**: Apply common filters like blur, sharpen, and edge enhancement
- **Batch Operations**: Process multiple images at once for presentations
- **Thumbnail Generation**: Create thumbnail galleries for quick previews
- **Metadata Handling**: Extract and manage image information

### Installation

```bash
pip install -r requirements.txt
```

### Quick Start

```python
from image_library import ImageLibrary

# Initialize library
lib = ImageLibrary()

# Load an image
lib.load_image('presentation_slide.jpg')

# Resize for presentation (maintain aspect ratio)
lib.resize(1920, 1080, maintain_aspect=True)

# Apply enhancement filter
lib.apply_filter('sharpen')

# Save processed image
lib.save_image('output/enhanced_slide.jpg')
```

### Batch Operations

```python
from image_library import batch_resize_images, create_thumbnail_gallery

# Resize all images in a directory
batch_resize_images('slides/', 'resized_slides/', (800, 600))

# Create thumbnail gallery
create_thumbnail_gallery('slides/', 'thumbnails/', (150, 150))
```

### Usage Examples

See `example_usage.py` for comprehensive examples of all library features.

### Testing

Run the test suite to verify functionality:

```bash
python test_image_library.py
```

### Supported Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)
- WebP (.webp)

This library is perfect for preparing images for presentations, creating slide decks, and managing media assets for educational or business materials.
