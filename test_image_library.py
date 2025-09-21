"""
Test suite for the Image Library

Comprehensive tests to validate the functionality of the image library.
"""

import unittest
import os
import tempfile
from PIL import Image
from image_library import ImageLibrary, batch_resize_images, create_thumbnail_gallery


class TestImageLibrary(unittest.TestCase):
    """Test cases for ImageLibrary class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lib = ImageLibrary()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a test image
        self.test_image_path = os.path.join(self.temp_dir, "test_image.png")
        test_img = Image.new('RGB', (100, 100), color='red')
        test_img.save(self.test_image_path)
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_load_image_success(self):
        """Test successful image loading."""
        result = self.lib.load_image(self.test_image_path)
        self.assertTrue(result)
        self.assertIsNotNone(self.lib.current_image)
        self.assertIsNotNone(self.lib.original_image)
    
    def test_load_image_file_not_found(self):
        """Test loading non-existent file."""
        result = self.lib.load_image("nonexistent.jpg")
        self.assertFalse(result)
        self.assertIsNone(self.lib.current_image)
    
    def test_load_image_unsupported_format(self):
        """Test loading unsupported format."""
        unsupported_path = os.path.join(self.temp_dir, "test.xyz")
        with open(unsupported_path, 'w') as f:
            f.write("not an image")
        
        result = self.lib.load_image(unsupported_path)
        self.assertFalse(result)
    
    def test_save_image_success(self):
        """Test successful image saving."""
        self.lib.load_image(self.test_image_path)
        output_path = os.path.join(self.temp_dir, "output.jpg")
        
        result = self.lib.save_image(output_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
    
    def test_save_image_no_image_loaded(self):
        """Test saving when no image is loaded."""
        output_path = os.path.join(self.temp_dir, "output.jpg")
        result = self.lib.save_image(output_path)
        self.assertFalse(result)
    
    def test_resize_maintain_aspect(self):
        """Test resizing with aspect ratio maintained."""
        self.lib.load_image(self.test_image_path)
        original_size = self.lib.current_image.size
        
        result = self.lib.resize(50, 50, maintain_aspect=True)
        self.assertTrue(result)
        
        # Should be smaller than original but maintain proportions
        new_size = self.lib.current_image.size
        self.assertLessEqual(max(new_size), 50)
    
    def test_resize_exact_dimensions(self):
        """Test resizing to exact dimensions."""
        self.lib.load_image(self.test_image_path)
        
        result = self.lib.resize(75, 50, maintain_aspect=False)
        self.assertTrue(result)
        
        self.assertEqual(self.lib.current_image.size, (75, 50))
    
    def test_rotate(self):
        """Test image rotation."""
        self.lib.load_image(self.test_image_path)
        original_size = self.lib.current_image.size
        
        result = self.lib.rotate(90)
        self.assertTrue(result)
        
        # After 90-degree rotation, dimensions should be swapped
        new_size = self.lib.current_image.size
        self.assertEqual(new_size, (original_size[1], original_size[0]))
    
    def test_crop(self):
        """Test image cropping."""
        self.lib.load_image(self.test_image_path)
        
        result = self.lib.crop(10, 10, 60, 60)
        self.assertTrue(result)
        
        self.assertEqual(self.lib.current_image.size, (50, 50))
    
    def test_convert_format_to_jpeg(self):
        """Test format conversion to JPEG."""
        # Create RGBA image
        rgba_path = os.path.join(self.temp_dir, "rgba_test.png")
        rgba_img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        rgba_img.save(rgba_path)
        
        self.lib.load_image(rgba_path)
        result = self.lib.convert_format('JPEG')
        self.assertTrue(result)
        self.assertEqual(self.lib.current_image.mode, 'RGB')
    
    def test_convert_format_to_png(self):
        """Test format conversion to PNG."""
        self.lib.load_image(self.test_image_path)
        result = self.lib.convert_format('PNG')
        self.assertTrue(result)
        self.assertEqual(self.lib.current_image.mode, 'RGBA')
    
    def test_get_image_info(self):
        """Test getting image information."""
        self.lib.load_image(self.test_image_path)
        info = self.lib.get_image_info()
        
        self.assertIn('size', info)
        self.assertIn('width', info)
        self.assertIn('height', info)
        self.assertIn('format', info)
        self.assertIn('mode', info)
        self.assertEqual(info['size'], (100, 100))
        self.assertEqual(info['width'], 100)
        self.assertEqual(info['height'], 100)
    
    def test_get_image_info_no_image(self):
        """Test getting info when no image is loaded."""
        info = self.lib.get_image_info()
        self.assertEqual(info, {})
    
    def test_reset_to_original(self):
        """Test resetting to original image."""
        self.lib.load_image(self.test_image_path)
        original_size = self.lib.current_image.size
        
        # Modify image
        self.lib.resize(50, 50)
        modified_size = self.lib.current_image.size
        
        # Reset
        result = self.lib.reset_to_original()
        self.assertTrue(result)
        self.assertEqual(self.lib.current_image.size, original_size)
        self.assertNotEqual(self.lib.current_image.size, modified_size)
    
    def test_apply_filter(self):
        """Test applying image filters."""
        self.lib.load_image(self.test_image_path)
        
        # Test valid filter
        result = self.lib.apply_filter('blur')
        self.assertTrue(result)
        
        # Test invalid filter
        result = self.lib.apply_filter('invalid_filter')
        self.assertFalse(result)


class TestBatchOperations(unittest.TestCase):
    """Test cases for batch operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.temp_dir, "input")
        self.output_dir = os.path.join(self.temp_dir, "output")
        
        os.makedirs(self.input_dir)
        
        # Create test images
        for i in range(3):
            img = Image.new('RGB', (200, 200), color=(i * 80, 100, 150))
            img.save(os.path.join(self.input_dir, f"test_{i}.png"))
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_batch_resize_images(self):
        """Test batch resizing of images."""
        count = batch_resize_images(self.input_dir, self.output_dir, (100, 100))
        
        self.assertEqual(count, 3)
        self.assertTrue(os.path.exists(self.output_dir))
        
        # Check that output files exist
        output_files = os.listdir(self.output_dir)
        self.assertEqual(len(output_files), 3)
    
    def test_batch_resize_nonexistent_dir(self):
        """Test batch resize with non-existent input directory."""
        count = batch_resize_images("nonexistent", self.output_dir, (100, 100))
        self.assertEqual(count, 0)
    
    def test_create_thumbnail_gallery(self):
        """Test creating thumbnail gallery."""
        count = create_thumbnail_gallery(self.input_dir, self.output_dir, (50, 50))
        
        self.assertEqual(count, 3)
        self.assertTrue(os.path.exists(self.output_dir))
        
        # Check that thumbnail files exist with correct naming
        output_files = os.listdir(self.output_dir)
        self.assertEqual(len(output_files), 3)
        
        for filename in output_files:
            self.assertIn('_thumb', filename)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)