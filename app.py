import os
import io
import json
from flask import Flask, render_template, jsonify, request, send_file
from utils.extraction import (
    extract_colors, generate_color_harmonies, hex_to_rgb,
    generate_ase_file, generate_svg_palette, generate_tailwind_config,
    generate_scss_variables, generate_figma_tokens, get_color_name,
    analyze_palette_character, calculate_spatial_distribution,
    generate_css_gradient, delta_e_ciede2000, compare_palette_ciede2000,
    recolor_image, generate_gpl_palette, generate_aco_file,
    generate_procreate_swatches, generate_style_dictionary_tokens
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload limit

SAMPLE_PRESETS = [
    {
        "id": "sunset_glow",
        "name": "Sunset Glow",
        "category": "Nature & Warmth",
        "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><defs><linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#f97316"/><stop offset="50%" stop-color="#ec4899"/><stop offset="100%" stop-color="#6366f1"/></linearGradient></defs><rect width="400" height="300" fill="url(#g1)"/><circle cx="200" cy="150" r="80" fill="#fde047" opacity="0.85"/></svg>'
    },
    {
        "id": "neon_cyberpunk",
        "name": "Neon Cyberpunk",
        "category": "Vibrant & Dark",
        "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><rect width="400" height="300" fill="#090d16"/><circle cx="120" cy="150" r="90" fill="#06b6d4" opacity="0.8"/><circle cx="280" cy="150" r="90" fill="#d946ef" opacity="0.85"/><polygon points="200,60 250,220 150,220" fill="#facc15"/></svg>'
    },
    {
        "id": "forest_pine",
        "name": "Pine & Earth",
        "category": "Organic",
        "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><rect width="400" height="300" fill="#14532d"/><rect x="50" y="50" width="140" height="200" fill="#15803d" rx="10"/><rect x="210" y="50" width="140" height="200" fill="#a16207" rx="10"/><circle cx="200" cy="150" r="45" fill="#fef08a"/></svg>'
    },
    {
        "id": "pastel_dream",
        "name": "Pastel Studio",
        "category": "Soft & Minimal",
        "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><rect width="400" height="300" fill="#f8fafc"/><circle cx="100" cy="150" r="70" fill="#fbcfe8"/><circle cx="200" cy="150" r="70" fill="#bfdbfe"/><circle cx="300" cy="150" r="70" fill="#bbf7d0"/></svg>'
    }
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "app": "Veyra Palette Studio"})


@app.route('/api/samples', methods=['GET'])
def get_samples():
    return jsonify({"success": True, "samples": SAMPLE_PRESETS})


@app.route('/api/extract', methods=['POST'])
def extract_palette():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['image']
    color_count = int(request.form.get('color_count', 5))
    algorithm = request.form.get('algorithm', 'kmeans')
    perceptual_filter = request.form.get('perceptual_filter', 'true').lower() == 'true'

    region_raw = request.form.get('region')
    region = json.loads(region_raw) if region_raw else None

    locked_raw = request.form.get('locked_colors')
    locked_colors = json.loads(locked_raw) if locked_raw else None

    try:
        palette = extract_colors(
            image_stream=file.stream,
            color_count=color_count,
            algorithm=algorithm,
            region=region,
            perceptual_filter=perceptual_filter,
            locked_colors=locked_colors
        )
        analytics = analyze_palette_character(palette)

        file.stream.seek(0)
        spatial_distribution = calculate_spatial_distribution(
            image_stream=file.stream,
            palette=palette,
            region=region
        )

        return jsonify({
            'success': True,
            'palette': palette,
            'analytics': analytics,
            'spatial_distribution': spatial_distribution
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/recolor', methods=['POST'])
def recolor():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['image']
    orig_raw = request.form.get('original_palette')
    target_raw = request.form.get('target_palette')

    original_palette = json.loads(orig_raw) if orig_raw else []
    target_palette = json.loads(target_raw) if target_raw else []

    if not original_palette or not target_palette:
        return jsonify({'error': 'Both original and target palettes required'}), 400

    try:
        recolored_bytes = recolor_image(file.stream, original_palette, target_palette)
        return send_file(
            io.BytesIO(recolored_bytes),
            mimetype='image/png',
            as_attachment=True,
            download_name='veyra-recolored.png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics', methods=['POST'])
def get_analytics():
    data = request.get_json() or {}
    palette = data.get('palette', [])

    if not palette:
        return jsonify({'error': 'Palette data required'}), 400

    try:
        analytics = analyze_palette_character(palette)
        return jsonify({'success': True, 'analytics': analytics})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/spatial', methods=['POST'])
def get_spatial_analysis():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['image']
    palette_raw = request.form.get('palette')
    palette = json.loads(palette_raw) if palette_raw else []

    region_raw = request.form.get('region')
    region = json.loads(region_raw) if region_raw else None

    if not palette:
        return jsonify({'error': 'Palette data required'}), 400

    try:
        spatial_distribution = calculate_spatial_distribution(
            image_stream=file.stream,
            palette=palette,
            region=region
        )
        return jsonify({'success': True, 'spatial_distribution': spatial_distribution})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/gradient', methods=['POST'])
def get_gradient():
    data = request.get_json() or {}
    palette = data.get('palette', [])
    gradient_type = data.get('type', 'linear')
    angle = int(data.get('angle', 90))

    if not palette:
        return jsonify({'error': 'Palette data required'}), 400

    try:
        css_gradient = generate_css_gradient(palette, gradient_type=gradient_type, angle=angle)
        return jsonify({'success': True, 'css': css_gradient})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/compare_ciede2000', methods=['POST'])
def compare_ciede2000():
    data = request.get_json() or {}
    palette = data.get('palette', [])
    library_name = data.get('library', 'tailwind')
    custom_targets = data.get('custom_targets', None)

    if not palette:
        return jsonify({'error': 'Palette data required'}), 400

    try:
        comparison_results = compare_palette_ciede2000(
            palette=palette,
            library_name=library_name,
            custom_targets=custom_targets
        )
        return jsonify({'success': True, 'comparison': comparison_results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/name', methods=['POST'])
def name_color():
    data = request.get_json() or {}
    rgb = data.get('rgb_values')
    hex_val = data.get('hex')

    if not rgb and hex_val:
        rgb = hex_to_rgb(hex_val)

    if not rgb:
        return jsonify({'error': 'RGB or HEX value required'}), 400

    try:
        name = get_color_name(rgb)
        return jsonify({'success': True, 'name': name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/harmonies', methods=['POST'])
def get_harmonies():
    data = request.get_json() or {}
    hex_val = data.get('hex')
    rgb = data.get('rgb_values')

    if not rgb and hex_val:
        rgb = hex_to_rgb(hex_val)

    if not rgb:
        return jsonify({'error': 'RGB or HEX value required'}), 400

    try:
        harmonies = generate_color_harmonies(rgb)
        return jsonify({'success': True, 'harmonies': harmonies})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/<fmt>', methods=['POST'])
def export_palette(fmt):
    data = request.get_json() or {}
    palette = data.get('palette', [])

    if not palette:
        return jsonify({'error': 'Palette data required'}), 400

    try:
        if fmt == 'ase':
            ase_bytes = generate_ase_file(palette)
            return send_file(
                io.BytesIO(ase_bytes),
                mimetype='application/octet-stream',
                as_attachment=True,
                download_name='veyra-palette.ase'
            )
        elif fmt == 'aco':
            aco_bytes = generate_aco_file(palette)
            return send_file(
                io.BytesIO(aco_bytes),
                mimetype='application/octet-stream',
                as_attachment=True,
                download_name='veyra-palette.aco'
            )
        elif fmt == 'swatches' or fmt == 'procreate':
            swatches_bytes = generate_procreate_swatches(palette)
            return send_file(
                io.BytesIO(swatches_bytes),
                mimetype='application/zip',
                as_attachment=True,
                download_name='veyra-palette.swatches'
            )
        elif fmt == 'gpl':
            gpl_str = generate_gpl_palette(palette)
            return send_file(
                io.BytesIO(gpl_str.encode('utf-8')),
                mimetype='text/plain',
                as_attachment=True,
                download_name='veyra-palette.gpl'
            )
        elif fmt == 'svg':
            svg_str = generate_svg_palette(palette)
            return send_file(
                io.BytesIO(svg_str.encode('utf-8')),
                mimetype='image/svg+xml',
                as_attachment=True,
                download_name='veyra-palette.svg'
            )
        elif fmt == 'tailwind':
            return jsonify({'success': True, 'content': generate_tailwind_config(palette)})
        elif fmt == 'scss':
            return jsonify({'success': True, 'content': generate_scss_variables(palette)})
        elif fmt == 'figma':
            return jsonify({'success': True, 'content': generate_figma_tokens(palette)})
        elif fmt == 'tokens' or fmt == 'styledictionary':
            return jsonify({'success': True, 'content': generate_style_dictionary_tokens(palette)})
        else:
            return jsonify({'error': f'Unsupported export format: {fmt}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)