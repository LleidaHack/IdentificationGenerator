from typing import List, Any
from PIL import Image
from io import BytesIO

class CardGeneratorService:
    """Service for generating identification cards and converting them to various formats"""
    
    def generate_card_image(self, user: Any) -> Image.Image:
        """Generate a card image for a single user"""
        user.generate_card()
        if not user.card:
            raise ValueError(f"Failed to generate card for user {user.id}")
        return user.card
    
    def generate_card_png_bytes(self, user: Any) -> bytes:
        """Generate a card and return it as PNG bytes"""
        card_image = self.generate_card_image(user)
        img_byte_arr = BytesIO()
        card_image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def generate_multiple_cards(self, users: List[Any]) -> List[Image.Image]:
        """Generate cards for multiple users and return list of images"""
        if not users:
            raise ValueError("No users provided")
        
        images = []
        for user in users:
            try:
                card = self.generate_card_image(user)
                images.append(card)
            except ValueError:
                # Skip users that fail to generate cards
                continue
        
        if not images:
            raise ValueError("Failed to generate any card images")
        
        return images
