"""
Example usage of the Image Library for Presentation Materials

This script demonstrates the key features of the image library.
"""

from image_library import ImageLibrary, batch_resize_images, create_thumbnail_gallery
import os

def main():
    """Demonstrate image library functionality."""
    
    print("=== Image Library Demo ===\n")
    
    # Initialize the library
    lib = ImageLibrary()
    
    # Create a sample directory structure for demonstration
    os.makedirs("sample_images", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    print("Image Library initialized successfully!")
    print(f"Supported formats: {', '.join(lib.SUPPORTED_FORMATS)}")
    
    # Example 1: Basic image operations (would work with actual image files)
    print("\n=== Example Usage ===")
    print("# Load an image")
    print("lib = ImageLibrary()")
    print("lib.load_image('presentation_slide.jpg')")
    print()
    
    print("# Get image information")
    print("info = lib.get_image_info()")
    print("print(f'Image size: {info[\"width\"]}x{info[\"height\"]}')")
    print()
    
    print("# Resize image for presentation")
    print("lib.resize(1920, 1080, maintain_aspect=True)")
    print()
    
    print("# Rotate image")
    print("lib.rotate(90)")
    print()
    
    print("# Apply filter")
    print("lib.apply_filter('sharpen')")
    print()
    
    print("# Save processed image")
    print("lib.save_image('output/processed_slide.jpg')")
    print()
    
    print("# Convert format")
    print("lib.convert_format('PNG')")
    print("lib.save_image('output/slide.png')")
    print()
    
    # Example 2: Batch operations
    print("=== Batch Operations ===")
    print("# Batch resize all images in a directory")
    print("count = batch_resize_images('slides/', 'resized_slides/', (800, 600))")
    print("print(f'Processed {count} images')")
    print()
    
    print("# Create thumbnail gallery")
    print("count = create_thumbnail_gallery('slides/', 'thumbnails/', (150, 150))")
    print("print(f'Created {count} thumbnails')")
    print()
    
    # Example 3: Advanced operations
    print("=== Advanced Operations ===")
    print("# Crop image for specific aspect ratio")
    print("lib.crop(100, 50, 700, 500)")
    print()
    
    print("# Reset to original")
    print("lib.reset_to_original()")
    print()
    
    print("# Chain operations")
    print("lib.resize(1024, 768)")
    print("lib.apply_filter('edge_enhance')")
    print("lib.save_image('output/enhanced_image.png')")
    
    print("\n=== Demo Complete ===")
    print("The image library is ready for use with your presentation materials!")

if __name__ == "__main__":
    main()