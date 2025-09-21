"""
Image Library for Presentation Materials

A comprehensive image processing library designed for presentation and media handling.
Provides functionality for image loading, saving, transformation, and format conversion.
"""

import os
from typing import Tuple, Optional, Union
from PIL import Image, ImageOps, ImageFilter
import numpy as np


class ImageLibrary:
    """
    A comprehensive image processing library for presentations and media.
    
    Supports common image operations including loading, saving, resizing,
    rotation, cropping, and format conversion.
    """
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    def __init__(self):
        """Initialize the ImageLibrary."""
        self.current_image = None
        self.original_image = None
        
    def load_image(self, file_path: str) -> bool:
        """
        Load an image from file path.
        
        Args:
            file_path (str): Path to the image file
            
        Returns:
            bool: True if image loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Image file not found: {file_path}")
                
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.SUPPORTED_FORMATS:
                raise ValueError(f"Unsupported image format: {file_ext}")
                
            self.current_image = Image.open(file_path)
            self.original_image = self.current_image.copy()
            return True
            
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    
    def save_image(self, file_path: str, quality: int = 95) -> bool:
        """
        Save the current image to file.
        
        Args:
            file_path (str): Output file path
            quality (int): Image quality for JPEG (1-100)
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            if self.current_image is None:
                raise ValueError("No image loaded")
                
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            save_kwargs = {}
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.jpg', '.jpeg']:
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True
                
            self.current_image.save(file_path, **save_kwargs)
            return True
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    def resize(self, width: int, height: int, maintain_aspect: bool = True) -> bool:
        """
        Resize the current image.
        
        Args:
            width (int): Target width
            height (int): Target height
            maintain_aspect (bool): Whether to maintain aspect ratio
            
        Returns:
            bool: True if resized successfully, False otherwise
        """
        try:
            if self.current_image is None:
                raise ValueError("No image loaded")
                
            if maintain_aspect:
                self.current_image.thumbnail((width, height), Image.Resampling.LANCZOS)
            else:
                self.current_image = self.current_image.resize((width, height), Image.Resampling.LANCZOS)
                
            return True
            
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
    
    def rotate(self, angle: float, expand: bool = True) -> bool:
        """
        Rotate the current image.
        
        Args:
            angle (float): Rotation angle in degrees
            expand (bool): Whether to expand image to fit rotated content
            
        Returns:
            bool: True if rotated successfully, False otherwise
        """
        try:
            if self.current_image is None:
                raise ValueError("No image loaded")
                
            self.current_image = self.current_image.rotate(angle, expand=expand, fillcolor='white')
            return True
            
        except Exception as e:
            print(f"Error rotating image: {e}")
            return False
    
    def crop(self, left: int, top: int, right: int, bottom: int) -> bool:
        """
        Crop the current image.
        
        Args:
            left (int): Left coordinate
            top (int): Top coordinate  
            right (int): Right coordinate
            bottom (int): Bottom coordinate
            
        Returns:
            bool: True if cropped successfully, False otherwise
        """
        try:
            if self.current_image is None:
                raise ValueError("No image loaded")
                
            self.current_image = self.current_image.crop((left, top, right, bottom))
            return True
            
        except Exception as e:
            print(f"Error cropping image: {e}")
            return False
    
    def convert_format(self, new_format: str) -> bool:
        """
        Convert image to a different format.
        
        Args:
            new_format (str): Target format (e.g., 'JPEG', 'PNG', 'WEBP')
            
        Returns:
            bool: True if converted successfully, False otherwise
        """
        try:
            if self.current_image is None:
                raise ValueError("No image loaded")
                
            if new_format.upper() == 'JPEG' and self.current_image.mode in ('RGBA', 'LA', 'P'):
                # Convert to RGB for JPEG
                self.current_image = self.current_image.convert('RGB')
            elif new_format.upper() == 'PNG' and self.current_image.mode not in ('RGBA', 'LA', 'P'):
                # Convert to RGBA for PNG with transparency support
                self.current_image = self.current_image.convert('RGBA')
                
            return True
            
        except Exception as e:
            print(f"Error converting format: {e}")
            return False
    
    def get_image_info(self) -> dict:
        """
        Get information about the current image.
        
        Returns:
            dict: Image information including size, format, mode
        """
        if self.current_image is None:
            return {}
            
        return {
            'size': self.current_image.size,
            'width': self.current_image.width,
            'height': self.current_image.height,
            'format': self.current_image.format,
            'mode': self.current_image.mode,
            'has_transparency': self.current_image.mode in ('RGBA', 'LA') or 'transparency' in self.current_image.info
        }
    
    def reset_to_original(self) -> bool:
        """
        Reset current image to the original loaded image.
        
        Returns:
            bool: True if reset successfully, False otherwise
        """
        try:
            if self.original_image is None:
                raise ValueError("No original image available")
                
            self.current_image = self.original_image.copy()
            return True
            
        except Exception as e:
            print(f"Error resetting image: {e}")
            return False
    
    def apply_filter(self, filter_type: str) -> bool:
        """
        Apply a filter to the current image.
        
        Args:
            filter_type (str): Type of filter ('blur', 'sharpen', 'edge_enhance')
            
        Returns:
            bool: True if filter applied successfully, False otherwise
        """
        try:
            if self.current_image is None:
                raise ValueError("No image loaded")
                
            filter_map = {
                'blur': ImageFilter.BLUR,
                'sharpen': ImageFilter.SHARPEN,
                'edge_enhance': ImageFilter.EDGE_ENHANCE,
                'smooth': ImageFilter.SMOOTH
            }
            
            if filter_type not in filter_map:
                raise ValueError(f"Unsupported filter type: {filter_type}")
                
            self.current_image = self.current_image.filter(filter_map[filter_type])
            return True
            
        except Exception as e:
            print(f"Error applying filter: {e}")
            return False


# Utility functions for batch operations
def batch_resize_images(input_dir: str, output_dir: str, target_size: Tuple[int, int]) -> int:
    """
    Batch resize all images in a directory.
    
    Args:
        input_dir (str): Input directory path
        output_dir (str): Output directory path
        target_size (Tuple[int, int]): Target size (width, height)
        
    Returns:
        int: Number of images processed successfully
    """
    if not os.path.exists(input_dir):
        print(f"Input directory not found: {input_dir}")
        return 0
        
    os.makedirs(output_dir, exist_ok=True)
    processed_count = 0
    
    library = ImageLibrary()
    
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext in ImageLibrary.SUPPORTED_FORMATS:
            if library.load_image(file_path):
                if library.resize(target_size[0], target_size[1]):
                    output_path = os.path.join(output_dir, filename)
                    if library.save_image(output_path):
                        processed_count += 1
                        print(f"Processed: {filename}")
                    
    return processed_count


def create_thumbnail_gallery(input_dir: str, output_dir: str, thumb_size: Tuple[int, int] = (150, 150)) -> int:
    """
    Create thumbnail versions of all images in a directory.
    
    Args:
        input_dir (str): Input directory path
        output_dir (str): Output directory path  
        thumb_size (Tuple[int, int]): Thumbnail size (width, height)
        
    Returns:
        int: Number of thumbnails created successfully
    """
    if not os.path.exists(input_dir):
        print(f"Input directory not found: {input_dir}")
        return 0
        
    os.makedirs(output_dir, exist_ok=True)
    created_count = 0
    
    library = ImageLibrary()
    
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext in ImageLibrary.SUPPORTED_FORMATS:
            if library.load_image(file_path):
                if library.resize(thumb_size[0], thumb_size[1], maintain_aspect=True):
                    name, ext = os.path.splitext(filename)
                    thumb_filename = f"{name}_thumb{ext}"
                    output_path = os.path.join(output_dir, thumb_filename)
                    
                    if library.save_image(output_path):
                        created_count += 1
                        print(f"Created thumbnail: {thumb_filename}")
                        
    return created_count