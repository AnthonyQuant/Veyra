Veyra — Intelligent Color Palette Studio

An image-driven color design studio that extracts perceptually distinct palettes, provides intelligent color refinement and accessibility analysis, and transforms images into ready-to-use design systems.

OVERVIEW

Veyra is a full-stack web application designed for UI/UX designers, quantitative visual researchers, and visual artists. Unlike basic color extraction tools that return simple RGB averages, Veyra combines machine learning clustering algorithms (K-Means and Median Cut) with perceptual color science (CIELAB color space conversions and CIEDE2000 distance metrics).

The application provides a complete workflow: from targeted image region extraction to real-time image recoloring, WCAG 2.1 accessibility auditing, color blindness simulation, and automated exporter generation for major design software (Adobe Photoshop/Illustrator, Procreate, GIMP, Figma, Tailwind CSS, and Style Dictionary).

KEY FEATURES & CAPABILITIES

1. Image Processing & Intelligent Extraction

• Multi-Format Input: Drag-and-drop interface, file browser, clipboard (Ctrl + V) paste integration, and curated preset image cards. Supports PNG, JPG, JPEG, WebP, and SVG formats up to 16MB.

• Dual Clustering Algorithms:
  - K-Means Clustering: Statistically partitions image pixels into optimal color centroids.
  - Median Cut Quantization: Preserves color spectrum diversity across distinct color spaces.

• Perceptual Filtering (ΔE Filter): Filters out visually duplicate swatches by enforcing minimum perceptual distance thresholds in the CIELAB color space.

• Interactive Region Sampler: HTML5 Canvas drag-to-select bounding box allowing users to restrict extraction to specific areas of an uploaded image.

• In-Memory Operations: Privacy-focused server pipeline that processes image byte streams entirely in-memory (io.BytesIO) without writing temporary files to server storage.

2. Palette Refinement & Color Science

• Swatch Locking & Selective Regeneration: Lock specific swatches and regenerate only the unlocked swatches to craft cohesive palettes.

• Live Color Editing: Adjust swatches using native browser color pickers or direct hex code inputs, triggering immediate server-side color name lookups.

• CIELAB Color Name Matching: Automatically assigns human-readable color names based on nearest perceptual distance within a curated reference database.

• Interactive Reordering & Custom Swatches: Rearrange swatch ordering or add custom colors manually (up to 12 swatches per palette).

3. Real-Time Image Recolor & Palette Swap Simulator

• Live Canvas Pixel Remapping: Remap original palette colors to target colors directly on an HTML5 canvas element.

• Luminance Preservation Engine: Option to transfer hue and saturation while maintaining the original image's light and shadow dynamics.

• Throttled Processing: Client-side execution optimized with requestAnimationFrame and debounce controllers for smooth slider interactions.

4. Advanced Palette Analytics & CIEDE2000 Matching

• CIEDE2000 (ΔE00) Perceptual Matcher: Measures precise perceptual differences between extracted swatches and standardized design libraries (Tailwind CSS 500, Google Material Design 500, Apple iOS System Colors) or custom target hex inputs.

• Intra-Palette Distance Matrix: Generates a pairwise distance matrix displaying perceptual contrast across all swatches in the active palette.

• Spatial Coverage & Pixel Distribution: Calculates exact surface area percentage coverage, centroid coordinates (X, Y), and structural role labels (Dominant Background, Secondary Tonal Element, Mid-tone Fill, Accent Highlight).

• Mood & Character Analysis: Classifies palette tone profiles (Pastel & Delicate, Muted & Earthy, Dark & Moody, Warm & Energetic, Cool & Serene, High Contrast & Dynamic) alongside average saturation, lightness, and dominant hue distributions.

5. Accessibility & Visual Simulation

• WCAG 2.1 Text Legibility Matrix: Evaluates contrast ratios against #FFFFFF (White) and #000000 (Black) text, providing explicit AA and AAA compliance flags.

• Color Vision Deficiency (CVD) Simulator: Simulates palette appearance under Protanopia (red-blind), Deuteranopia (green-blind), Tritanopia (blue-blind), and Achromatopsia (monochrome) conditions.

• Color Harmonies Studio: Generates Complementary, Analogous, Triadic, and Split-Complementary schemes from any selected base swatch.

• Interactive UI Component Sandbox (NovaUI Studio): Maps palette swatches to live UI element roles (Primary CTA, Surface, Accent Badge, Background, Text) for real-time interface testing.

6. Multi-Format Exporters & Design Tokens

• Digital Painting Formats:
  - Adobe Swatch Exchange (.ASE): Binary color palette stream compatible with Photoshop, Illustrator, and InDesign.
  - Adobe Color Swatch (.ACO): Binary palette header structure (v1 and v2) for legacy Photoshop brush and swatches workflows.
  - Procreate Swatches (.swatches): Native ZIP archive containing structured swatches.json payload for Procreate on iPad.
  - GIMP/Inkscape (.GPL): Plain-text RGB palette representation for GIMP, Inkscape, and Krita.

• Graphic & Code Tokens:
  - Vector SVG Graphic Card: Scalable SVG output rendered with swatch geometry, hex codes, and typography.
  - HTML5 Canvas PNG Card: Downloadable high-resolution palette presentation card.
  - Tailwind CSS Config: Exportable module.exports theme extension block.
  - SCSS Variables: Standardized SCSS color definitions.
  - Figma Tokens JSON: W3C/Figma Design Token compatible JSON data.
  - Style Dictionary JSON: W3C Style Dictionary structured design tokens.

• Local History & Favorites Manager: Saves extracted palettes to browser LocalStorage with favoriting, load-to-studio actions, and filtering capabilities.


SYSTEM ARCHITECTURE & COMPONENTS

The application follows a modular, client-server architecture designed to keep heavy mathematical operations on the backend while maintaining responsive user interaction on the frontend.

VEYRA PALETTE STUDIO

- app.py                  # Flask Application Server & API Routing
- utils/
  - extraction.py         # Color Science, Clustering & Export Logic
- templates/
  - index.html            # Single Page Application DOM Structure
- static/
  - css/
    - style.css           # Custom CSS Dark Theme & Responsive Layout
  - js/
    - app.js              # State Management, Canvas Manipulation & API Handling

Component Breakdown

Component: app.py
Language / Stack: Python 3 (Flask)
Primary Responsibilities:
Serves web pages, validates incoming file payloads (16MB limit), routes API endpoints (/api/extract, /api/recolor, /api/export/<fmt>, etc.), and streams binary/text exporter responses.

Component: utils/extraction.py
Language / Stack: Python (NumPy, PIL, Scikit-Learn)
Primary Responsibilities:
Handles image downsampling, K-Means clustering, RGB/HSL/CIELAB conversion math, CIEDE2000 calculation vectors, spatial coverage analysis, image pixel recoloring, and binary packing (struct/zipfile) for ASE, ACO, and Procreate exporters.

Component: templates/index.html
Language / Stack: HTML5 (Jinja2)
Primary Responsibilities:
Defines the layout structure, upload dropzone, region cropping canvas, swatch controls, and 12 distinct studio feature tabs.

Component: static/css/style.css
Language / Stack: CSS3
Primary Responsibilities:
Implements custom CSS design tokens, modern dark theme styles, flexible grid systems (auto-fit / minmax), animations, and responsive breakpoints.

Component: static/js/app.js
Language / Stack: Vanilla JS (ES6+)
Primary Responsibilities:
Manages application state, handles drag-and-drop/clipboard events, drives region selection drawing, coordinates throttled canvas recoloring, calls REST endpoints, and handles browser localStorage persistence.


TECHNOLOGY STACK

• Backend Framework: Flask (Python 3.10+)

• Data Processing & Machine Learning: NumPy, Scikit-Learn (KMeans), Pillow (PIL)

• Frontend Architecture: Vanilla JavaScript (ES6+), HTML5 Canvas API, CSS3

• Icons & Fonts: FontAwesome 6, System UI / Monospace Fonts

• Storage: Browser LocalStorage (Client-Side), InMemory Processing Stream (BytesIO)


INSTALLATION & SETUP GUIDE

Prerequisites

• Python 3.9 or higher
• pip (Python Package Installer)

1. Clone the Repository

git clone https://github.com/AnthonyQuant/veyra.git

cd veyra

2. Set Up a Virtual Environment

Bash

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

3. Install Dependencies

Bash

pip install -r requirements.txt

Note: Key dependencies include Flask, NumPy, Scikit-Learn, and Pillow.

4. Run the Application

Bash

python app.py

Open your browser and navigate to:
http://127.0.0.1:5001


REST API REFERENCE

Veyra exposes a set of JSON and binary REST endpoints:

Endpoint: /api/health
Method: GET
Payload / Parameters: None
Description: Returns application health status.

Endpoint: /api/samples
Method: GET
Payload / Parameters: None
Description: Returns built-in sample preset graphics.

Endpoint: /api/extract
Method: POST
Payload / Parameters: multipart/form-data (image, color_count, algorithm, perceptual_filter, region, locked_colors)
Description: Extracts color palette, analytics, and spatial coverage from uploaded image stream.

Endpoint: /api/recolor
Method: POST
Payload / Parameters: multipart/form-data (image, original_palette, target_palette)
Description: Returns server-side recolored PNG binary image stream.

Endpoint: /api/analytics
Method: POST
Payload / Parameters: JSON (palette)
Description: Computes mood profile, tonal metrics, and hue distribution.

Endpoint: /api/spatial
Method: POST
Payload / Parameters: multipart/form-data (image, palette, region)
Description: Computes pixel spatial coverage percentage and centroid data.

Endpoint: /api/gradient
Method: POST
Payload / Parameters: JSON (palette, type, angle)
Description: Generates pure CSS background gradient strings.

Endpoint: /api/compare_ciede2000
Method: POST
Payload / Parameters: JSON (palette, library, custom_targets)
Description: Calculates ΔE00 distance against brand libraries and generates intra-palette distance matrix.

Endpoint: /api/name
Method: POST
Payload / Parameters: JSON (rgb_values or hex)
Description: Returns nearest human color name using CIELAB distance.

Endpoint: /api/harmonies
Method: POST
Payload / Parameters: JSON (rgb_values or hex)
Description: Generates complementary, triadic, split-complementary, and analogous color schemes.

Endpoint: /api/export/<fmt>
Method: POST
Payload / Parameters: JSON (palette), where <fmt> is ase, aco, swatches, gpl, svg, JSON/text token definitions, tailwind, scss, figma, or tokens.
Description: Returns compiled binary download streams or JSON/text token definitions.


STRENGTHS & STRATEGIC ADVANTAGES

1. Privacy-First In-Memory Processing:
Uploaded images are read into memory streams (io.BytesIO) and destroyed post-execution. No user data or images are saved to disk storage.

2. Sub-Second Vectorized Execution:
Heavy color math operations (such as RGB → CIELAB conversions and spatial pixel mapping) leverage NumPy vectorized array broadcasting for fast processing speeds.

3. Comprehensive Exporter Ecosystem:
Native export support covering code libraries (Tailwind, SCSS, Figma, Style Dictionary) and digital painting applications (Adobe Photoshop, Illustrator, Procreate, GIMP, Krita).

4. Professional Color Science Engine:
Employs CIEDE2000 (ΔE00) distance metrics and WCAG 2.1 AA/AAA compliance checks, providing actionable color contrast feedback rather than arbitrary color suggestions.

5. Zero External Frontend Framework Dependencies:
Built with pure Vanilla JS and CSS variables, minimizing client asset overhead and avoiding framework bloat.


LIMITATIONS & TECHNICAL WEAKNESSES

1. Single-Threaded CPU Clustering:
Heavy K-Means calculations on un-sampled large images run synchronously inside Python's single thread. While images are downsampled to 300 x 300 pixels before clustering to mitigate latency, high multi-tenant request loads require a WSGI server (such as Gunicorn or Uvicorn) with asynchronous task queues (Celery/Redis).

2. Browser Client Memory & Recolor Boundaries:
Real-time client-side image recoloring operates directly on raw HTML5 Canvas pixel arrays (ImageData). Processing high-resolution images (e.g., 4K+ resolution) inside the browser canvas can cause temporary client-side RAM spikes.

3. Local Storage Capacity Caps:
Palette history is stored inside browser LocalStorage. Browsers typically enforce a 5MB storage ceiling, which limits maximum offline saved history entries to approximately 25–30 full palette objects before older entries require purging.

4. Development Server Default:
The default app.run(debug=True, port=5001) configuration is intended strictly for local development and testing. Production deployments require setting debug=False behind an Nginx reverse proxy.


ROADMAP & FUTURE ENHANCEMENTS

• WebAssembly (Wasm) Integration:
Shift CIELAB conversion vectors and K-Means matrix loops to Rust-compiled WebAssembly for client-side processing.

• Async Worker Queue:
Integrate Celery and Redis to handle batch palette extraction for large image sets asynchronously.

• Cloud Palette Sync:
Add database integration (PostgreSQL / SQLAlchemy) to sync saved palettes across devices alongside LocalStorage.