# 🎨 Logo Generator

A beautiful web application that generates multiple logo variations for any company or brand name using Python and HTML. Simply enter a name and get 2-3 professionally designed logo suggestions instantly!

## ✨ Features

- **Multiple Logo Styles**: Generate logos in 4 different styles:
  - **Modern**: Clean, minimalist design
  - **Vibrant**: Colorful with background elements
  - **Professional**: Business-focused with underlines
  - **Creative**: Multi-color gradient text effects

- **Instant Generation**: Get 2-3 logo variations in seconds
- **Download Ready**: Download any logo as PNG file
- **Responsive Design**: Works perfectly on desktop and mobile
- **Beautiful UI**: Modern, gradient-based interface

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this project**
   ```bash
   # If you have git installed
   git clone <repository-url>
   cd logo-design
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
logo-design/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    └── index.html        # Frontend HTML template
```

## 🎯 How to Use

1. **Enter Company Name**: Type your company, brand, or personal name in the input field
2. **Generate Logos**: Click the "Generate Logos" button
3. **View Results**: See 2-3 different logo variations
4. **Download**: Click "Download" on any logo you like

## 🎨 Logo Styles Explained

### Modern Style
- Clean, minimalist design
- Single color text
- Perfect for tech companies and startups

### Vibrant Style
- Colorful circular background
- White text on colored background
- Great for creative agencies and lifestyle brands

### Professional Style
- Business-focused design
- Text with underline accent
- Ideal for law firms, consulting, and corporate brands

### Creative Style
- Multi-color gradient text
- Each letter in different color
- Perfect for creative agencies and artistic brands

## 🛠️ Technical Details

### Backend (Python/Flask)
- **Flask**: Web framework for API endpoints
- **Pillow (PIL)**: Image processing and logo generation
- **JSON API**: RESTful endpoints for logo generation

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Mobile-first approach
- **Modern CSS**: Gradients, animations, and hover effects
- **Vanilla JavaScript**: No external dependencies
- **Base64 Images**: Direct image display without file storage

### API Endpoints

- `GET /`: Main application page
- `POST /generate`: Generate logos for given text
- `GET /download/<style>`: Download specific logo style

## 🔧 Customization

### Adding New Logo Styles

1. **Add color palette** in `app.py`:
   ```python
   self.colors = {
       'your_style': ['#color1', '#color2', '#color3']
   }
   ```

2. **Add style logic** in `generate_logo()` method:
   ```python
   elif style == 'your_style':
       # Your custom logo generation code
   ```

### Changing Logo Size

Modify the `size` parameter in the `generate_logo()` method:
```python
logo = self.generate_logo(text, style, size=(600, 300))  # Width x Height
```

### Custom Fonts

Add your own fonts by placing `.ttf` files in the project directory and updating the `fonts` dictionary in `app.py`.

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" error**
   - Make sure you've installed requirements: `pip install -r requirements.txt`

2. **Font not loading**
   - The app will fall back to default fonts if custom fonts aren't available

3. **Port already in use**
   - Change the port in `app.py`: `app.run(port=5001)`

4. **Images not displaying**
   - Check browser console for errors
   - Ensure Flask server is running

### System Requirements

- **Windows**: Python 3.7+, pip
- **macOS**: Python 3.7+, pip
- **Linux**: Python 3.7+, pip

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this logo generator!

## 📞 Support

If you encounter any issues or have questions, please check the troubleshooting section above or create an issue in the project repository.

---

**Happy Logo Creating! 🎨✨**
