from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os
import random
from datetime import datetime
import math

app = Flask(__name__)

class LogoGenerator:
    def __init__(self):
        # Industry-based color schemes
        self.industry_colors = {
            'tech': ['#00D4FF', '#0099CC', '#0066CC', '#003D7A', '#001A3D'],
            'healthcare': ['#4CAF50', '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107'],
            'finance': ['#2C3E50', '#34495E', '#7F8C8D', '#BDC3C7', '#ECF0F1'],
            'food': ['#FF6B6B', '#FF8E53', '#FF6B9D', '#C44569', '#F8B500'],
            'fashion': ['#8E44AD', '#E67E22', '#1ABC9C', '#E91E63', '#9B59B6'],
            'education': ['#3498DB', '#2980B9', '#5DADE2', '#85C1E9', '#AED6F1'],
            'real_estate': ['#D4AC0D', '#B7950B', '#F4D03F', '#F7DC6F', '#FCF3CF'],
            'consulting': ['#2C3E50', '#34495E', '#7F8C8D', '#BDC3C7', '#ECF0F1'],
            'creative': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            'luxury': ['#FFD700', '#FFA500', '#FF8C00', '#FF7F50', '#FF6347']
        }
        
        # Logo templates with different styles
        self.logo_templates = {
            'badge': {
                'name': 'Badge Style',
                'description': 'Professional badge with border and icon',
                'industry_suitable': ['tech', 'consulting', 'finance']
            },
            'minimal': {
                'name': 'Minimal Style', 
                'description': 'Clean and simple design',
                'industry_suitable': ['tech', 'consulting', 'education']
            },
            'vibrant': {
                'name': 'Vibrant Style',
                'description': 'Colorful and energetic design',
                'industry_suitable': ['creative', 'food', 'fashion']
            },
            'elegant': {
                'name': 'Elegant Style',
                'description': 'Sophisticated and premium design',
                'industry_suitable': ['luxury', 'fashion', 'real_estate']
            },
            'modern': {
                'name': 'Modern Style',
                'description': 'Contemporary and sleek design',
                'industry_suitable': ['tech', 'consulting', 'education']
            },
            'organic': {
                'name': 'Organic Style',
                'description': 'Natural and flowing design',
                'industry_suitable': ['healthcare', 'food', 'education']
            }
        }
        
        self.fonts = {
            'bold': 'arial.ttf',
            'elegant': 'times.ttf',
            'modern': 'calibri.ttf'
        }
        
        # AI-powered industry detection keywords
        self.industry_keywords = {
            'tech': ['tech', 'software', 'app', 'digital', 'data', 'ai', 'computer', 'code', 'programming'],
            'healthcare': ['health', 'medical', 'doctor', 'clinic', 'hospital', 'pharmacy', 'wellness', 'care'],
            'finance': ['bank', 'finance', 'investment', 'money', 'capital', 'fund', 'credit', 'loan', 'insurance'],
            'food': ['food', 'restaurant', 'cafe', 'bakery', 'cooking', 'chef', 'dining', 'kitchen', 'catering'],
            'fashion': ['fashion', 'style', 'clothing', 'design', 'boutique', 'apparel', 'wear', 'trend'],
            'education': ['school', 'education', 'learning', 'academy', 'university', 'college', 'study', 'knowledge'],
            'real_estate': ['real estate', 'property', 'home', 'house', 'apartment', 'building', 'construction'],
            'consulting': ['consulting', 'business', 'strategy', 'management', 'advisory', 'professional'],
            'creative': ['creative', 'design', 'art', 'studio', 'agency', 'marketing', 'advertising'],
            'luxury': ['luxury', 'premium', 'exclusive', 'elite', 'high-end', 'boutique', 'sophisticated']
        }

    def create_icon(self, icon_type, size, color):
        """Create simple icons for logos"""
        icon = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(icon)
        
        if icon_type == 'star':
            # Create a star
            points = []
            for i in range(10):
                angle = i * math.pi / 5
                if i % 2 == 0:
                    radius = size // 2 - 5
                else:
                    radius = size // 4
                x = size // 2 + radius * math.cos(angle - math.pi / 2)
                y = size // 2 + radius * math.sin(angle - math.pi / 2)
                points.append((x, y))
            draw.polygon(points, fill=color)
            
        elif icon_type == 'circle':
            # Create a circle
            draw.ellipse([5, 5, size-5, size-5], fill=color)
            
        elif icon_type == 'square':
            # Create a square
            draw.rectangle([5, 5, size-5, size-5], fill=color)
            
        elif icon_type == 'triangle':
            # Create a triangle
            points = [(size//2, 5), (5, size-5), (size-5, size-5)]
            draw.polygon(points, fill=color)
            
        elif icon_type == 'diamond':
            # Create a diamond
            points = [(size//2, 5), (size-5, size//2), (size//2, size-5), (5, size//2)]
            draw.polygon(points, fill=color)
            
        elif icon_type == 'heart':
            # Create a heart shape
            heart_size = size // 3
            center_x, center_y = size // 2, size // 2
            # Left lobe
            draw.ellipse([center_x - heart_size, center_y - heart_size//2, 
                         center_x, center_y + heart_size//2], fill=color)
            # Right lobe
            draw.ellipse([center_x, center_y - heart_size//2, 
                         center_x + heart_size, center_y + heart_size//2], fill=color)
            # Bottom point
            points = [(center_x - heart_size, center_y), 
                     (center_x + heart_size, center_y),
                     (center_x, center_y + heart_size)]
            draw.polygon(points, fill=color)
            
        return icon

    def detect_industry(self, text):
        """AI-powered industry detection based on company name"""
        text_lower = text.lower()
        industry_scores = {}
        
        for industry, keywords in self.industry_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            industry_scores[industry] = score
        
        # Return industry with highest score, or 'creative' as default
        best_industry = max(industry_scores, key=industry_scores.get)
        return best_industry if industry_scores[best_industry] > 0 else 'creative'

    def get_suitable_templates(self, industry):
        """Get logo templates suitable for the detected industry"""
        suitable_templates = []
        for template_id, template_info in self.logo_templates.items():
            if industry in template_info['industry_suitable']:
                suitable_templates.append(template_id)
        
        # If no specific templates found, return all templates
        return suitable_templates if suitable_templates else list(self.logo_templates.keys())

    def generate_logo(self, text, template='modern', industry='creative', size=(400, 200)):
        """Generate a logo with the given text and style"""
        # Create image with transparent background
        img = Image.new('RGBA', size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Get colors for the industry
        color_palette = self.industry_colors.get(industry, self.industry_colors['creative'])
        primary_color = color_palette[0]
        secondary_color = color_palette[1] if len(color_palette) > 1 else primary_color
        
        # Use only first 2 letters of the text
        logo_text = text[:2].upper() if len(text) >= 2 else text.upper()
        
        # Try to load font, fallback to default if not available
        try:
            font_size = 80  # Larger font for 2 letters
            font = ImageFont.truetype(self.fonts['bold'], font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), logo_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        if template == 'badge':
            # Modern style with clean text, subtle shadow, and icon
            icon = self.create_icon('circle', 40, primary_color)
            img.paste(icon, (x - 50, y + text_height//2 - 20), icon)
            draw.text((x+2, y+2), logo_text, fill=(0, 0, 0, 50), font=font)
            draw.text((x, y), logo_text, fill=primary_color, font=font)
            
        elif template == 'vibrant':
            # Vibrant style with background circle, gradient effect, and star icon
            circle_radius = max(text_width, text_height) // 2 + 20
            circle_center = (size[0] // 2, size[1] // 2)
            # Outer circle
            draw.ellipse([circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                         circle_center[0] + circle_radius, circle_center[1] + circle_radius],
                        fill=secondary_color)
            # Inner circle
            draw.ellipse([circle_center[0] - circle_radius + 10, circle_center[1] - circle_radius + 10,
                         circle_center[0] + circle_radius - 10, circle_center[1] + circle_radius - 10],
                        fill=primary_color)
            # Add star icon
            icon = self.create_icon('star', 30, 'white')
            img.paste(icon, (x - 40, y + text_height//2 - 15), icon)
            draw.text((x, y), logo_text, fill='white', font=font)
            
        elif template == 'minimal':
            # Professional style with underline, border, and square icon
            # Add border rectangle
            border_padding = 10
            draw.rectangle([x - border_padding, y - border_padding, 
                          x + text_width + border_padding, y + text_height + border_padding + 10],
                          outline=secondary_color, width=2)
            # Add square icon
            icon = self.create_icon('square', 35, primary_color)
            img.paste(icon, (x - 50, y + text_height//2 - 17), icon)
            draw.text((x, y), logo_text, fill=primary_color, font=font)
            underline_y = y + text_height + 5
            draw.rectangle([x, underline_y, x + text_width, underline_y + 3], fill=secondary_color)
            
        elif template == 'elegant':
            # Creative style with gradient effect, decorative elements, and diamond icon
            # Add diamond icon
            icon = self.create_icon('diamond', 40, color_palette[0])
            img.paste(icon, (x - 50, y + text_height//2 - 20), icon)
            for i, char in enumerate(logo_text):
                char_x = x + (i * text_width // len(logo_text))
                color = color_palette[i % len(color_palette)]
                draw.text((char_x, y), char, fill=color, font=font)
            # Add decorative dots
            for i in range(3):
                dot_x = x + (i * text_width // 2)
                dot_y = y + text_height + 15
                draw.ellipse([dot_x, dot_y, dot_x + 8, dot_y + 8], fill=color_palette[i % len(color_palette)])
                
        elif template == 'modern':
            # Elegant style with gold accents, serif-like appearance, and heart icon
            # Add heart icon
            icon = self.create_icon('heart', 35, primary_color)
            img.paste(icon, (x - 50, y + text_height//2 - 17), icon)
            # Background rectangle
            draw.rectangle([x - 15, y - 10, x + text_width + 15, y + text_height + 10], 
                          fill=(255, 215, 0, 20), outline=primary_color, width=2)
            draw.text((x, y), logo_text, fill=primary_color, font=font)
            # Add elegant corner decorations
            corner_size = 15
            draw.rectangle([x - 15, y - 10, x - 15 + corner_size, y - 10 + 3], fill=secondary_color)
            draw.rectangle([x + text_width + 15 - corner_size, y - 10, x + text_width + 15, y - 10 + 3], fill=secondary_color)
            
        elif template == 'organic':
            # Tech style with geometric elements, futuristic look, and triangle icon
            # Add triangle icon
            icon = self.create_icon('triangle', 40, 'white')
            img.paste(icon, (x - 50, y + text_height//2 - 20), icon)
            # Hexagon background
            hex_size = max(text_width, text_height) // 2 + 30
            hex_center = (size[0] // 2, size[1] // 2)
            hex_points = [
                (hex_center[0], hex_center[1] - hex_size),
                (hex_center[0] + hex_size * 0.866, hex_center[1] - hex_size // 2),
                (hex_center[0] + hex_size * 0.866, hex_center[1] + hex_size // 2),
                (hex_center[0], hex_center[1] + hex_size),
                (hex_center[0] - hex_size * 0.866, hex_center[1] + hex_size // 2),
                (hex_center[0] - hex_size * 0.866, hex_center[1] - hex_size // 2)
            ]
            draw.polygon(hex_points, fill=secondary_color, outline=primary_color, width=2)
            draw.text((x, y), logo_text, fill='white', font=font)
            
        else:  # Default to minimal style
            # Simple clean design
            draw.text((x, y), logo_text, fill=primary_color, font=font)
        
        return img

    def generate_multiple_logos(self, text, num_logos=5):
        """Generate multiple logo variations using AI-powered industry detection"""
        # Detect industry based on company name
        detected_industry = self.detect_industry(text)
        
        # Get suitable templates for the industry
        suitable_templates = self.get_suitable_templates(detected_industry)
        
        # Select templates (prefer industry-suitable ones)
        if len(suitable_templates) >= num_logos:
            selected_templates = random.sample(suitable_templates, num_logos)
        else:
            # Mix suitable templates with others if needed
            all_templates = list(self.logo_templates.keys())
            remaining_needed = num_logos - len(suitable_templates)
            other_templates = [t for t in all_templates if t not in suitable_templates]
            selected_templates = suitable_templates + random.sample(other_templates, min(remaining_needed, len(other_templates)))
        
        logos = []
        for i, template in enumerate(selected_templates):
            logo = self.generate_logo(text, template, detected_industry)
            template_info = self.logo_templates[template]
            logos.append({
                'template': template,
                'template_name': template_info['name'],
                'description': template_info['description'],
                'industry': detected_industry,
                'image': logo,
                'filename': f'logo_{template}_{i+1}.png'
            })
        
        return logos

# Initialize logo generator
logo_gen = LogoGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_logos():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Please enter a name'}), 400
        
        # Generate logos
        logos = logo_gen.generate_multiple_logos(text, 5)
        
        # Save logos temporarily and return file paths
        logo_data = []
        for logo in logos:
            # Save to memory buffer
            img_buffer = io.BytesIO()
            logo['image'].save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Encode as base64 for frontend display
            import base64
            img_str = base64.b64encode(img_buffer.getvalue()).decode()
            
            logo_data.append({
                'template': logo['template'],
                'template_name': logo['template_name'],
                'description': logo['description'],
                'industry': logo['industry'],
                'image_data': f'data:image/png;base64,{img_str}',
                'filename': logo['filename']
            })
        
        return jsonify({'logos': logo_data})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<style>')
def download_logo(style):
    try:
        text = request.args.get('text', 'Logo')
        logo = logo_gen.generate_logo(text, style)
        
        # Save to memory buffer
        img_buffer = io.BytesIO()
        logo.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return send_file(
            img_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'{text}_{style}_logo.png'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
