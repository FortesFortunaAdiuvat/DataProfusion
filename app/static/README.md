# Static Assets for Data Profusion

This directory contains the static assets for the Data Profusion application.

## Directory Structure

```
static/
├── css/
│   └── style.css          # Additional CSS styles
├── js/
│   ├── jquery.particleground.js  # Particle animation library
│   └── demo.js            # Initialization and interaction scripts
├── images/
│   └── background.jpeg    # Background image (you need to add this)
└── README.md              # This file
```

## Required Assets

### Background Image
You need to add a background image at `app/static/images/background.jpeg`. This should be a high-quality image that works well with the gold/forest green color scheme.

Recommended specifications:
- Format: JPEG or PNG
- Resolution: At least 1920x1080
- Colors: Gold/warm tones that contrast well with forest green (#228B22)
- File size: Optimized for web (< 2MB recommended)

## JavaScript Libraries

### jquery.particleground.js
A simplified particle system that creates animated background particles. Features:
- Configurable particle density and movement
- Mouse parallax effects
- Responsive design
- Forest green color scheme to match the application

### demo.js
Application-specific JavaScript that:
- Initializes the particle background
- Adds hover effects to chart navigation links
- Provides loading states for external links
- Implements keyboard navigation support
- Adds accessibility features

## CSS Styling

### style.css
Additional styles that complement the main template styles:
- Custom scrollbar styling
- Loading animations
- Accessibility improvements
- Print styles
- Responsive design enhancements

## Color Scheme

The application uses a consistent color palette:
- **Primary Green**: #228B22 (Forest Green)
- **Accent Green**: #32CD32 (Lime Green)
- **Background**: Gold/warm tones from background image
- **Text**: White and forest green for contrast
- **Transparency**: Various alpha levels for glass-morphism effects

## Browser Compatibility

The static assets are designed to work with:
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

Fallbacks are provided for older browsers where possible.