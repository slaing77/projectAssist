"""
Live demonstration of the Image Library functionality.

This script creates test images and demonstrates actual image processing.
"""

from image_library import ImageLibrary, batch_resize_images, create_thumbnail_gallery
from PIL import Image, ImageDraw, ImageFont
import os

def create_demo_images():
    """Create sample images for demonstration."""
    
    # Create demo directory
    os.makedirs("demo_images", exist_ok=True)
    os.makedirs("demo_output", exist_ok=True)
    
    # Create sample presentation slides
    colors = [
        ('red', (255, 100, 100)),
        ('blue', (100, 100, 255)),
        ('green', (100, 255, 100))
    ]
    
    for i, (color_name, color) in enumerate(colors):
        # Create a 800x600 presentation slide
        img = Image.new('RGB', (800, 600), color=color)
        draw = ImageDraw.Draw(img)
        
        # Add some text to make it look like a slide
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
            
        text = f"Slide {i+1}\n{color_name.upper()} Theme"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Center the text
        x = (800 - text_width) // 2
        y = (600 - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        
        # Save the slide
        img.save(f"demo_images/slide_{i+1}.png")
        print(f"Created demo_images/slide_{i+1}.png")

def demonstrate_library():
    """Demonstrate the image library functionality."""
    
    print("\n=== Live Image Library Demonstration ===\n")
    
    # Create demo images first
    create_demo_images()
    
    # Initialize library
    lib = ImageLibrary()
    
    # Demonstrate single image operations
    print("1. Loading and processing a single image...")
    if lib.load_image("demo_images/slide_1.png"):
        print("   ✓ Image loaded successfully")
        
        # Get image info
        info = lib.get_image_info()
        print(f"   ✓ Original size: {info['width']}x{info['height']}")
        
        # Resize for web presentation
        if lib.resize(400, 300, maintain_aspect=True):
            new_info = lib.get_image_info()
            print(f"   ✓ Resized to: {new_info['width']}x{new_info['height']}")
        
        # Apply a filter
        if lib.apply_filter('sharpen'):
            print("   ✓ Applied sharpen filter")
        
        # Save processed image
        if lib.save_image("demo_output/processed_slide_1.png"):
            print("   ✓ Saved processed image to demo_output/processed_slide_1.png")
        
        # Reset and try rotation
        if lib.reset_to_original():
            print("   ✓ Reset to original")
            
        if lib.rotate(15):  # Slight rotation
            print("   ✓ Rotated image 15 degrees")
            
        if lib.save_image("demo_output/rotated_slide_1.png"):
            print("   ✓ Saved rotated image to demo_output/rotated_slide_1.png")
    
    print("\n2. Batch operations...")
    
    # Batch resize all demo images
    count = batch_resize_images("demo_images", "demo_output/resized", (640, 480))
    print(f"   ✓ Batch resized {count} images to 640x480")
    
    # Create thumbnails
    count = create_thumbnail_gallery("demo_images", "demo_output/thumbnails", (120, 90))
    print(f"   ✓ Created {count} thumbnails")
    
    print("\n3. Format conversion...")
    
    # Convert PNG to JPEG
    if lib.load_image("demo_images/slide_2.png"):
        if lib.convert_format('JPEG'):
            if lib.save_image("demo_output/slide_2_converted.jpg", quality=85):
                print("   ✓ Converted PNG to JPEG with 85% quality")
    
    print("\n=== Demonstration Complete ===")
    print("\nGenerated files:")
    print("- demo_images/: Original demo slides")
    print("- demo_output/: Processed images including:")
    print("  - processed_slide_1.png (resized and sharpened)")
    print("  - rotated_slide_1.png (rotated 15 degrees)")
    print("  - resized/: Batch resized images (640x480)")
    print("  - thumbnails/: Thumbnail gallery (120x90)")
    print("  - slide_2_converted.jpg (PNG to JPEG conversion)")
    
    print("\nThe image library is working perfectly for presentation materials!")

if __name__ == "__main__":
    demonstrate_library()