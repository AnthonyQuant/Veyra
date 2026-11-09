import io
import unittest
import numpy as np
from PIL import Image

from utils.extraction import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsl,
    rgb_to_lab,
    delta_e_ciede2000,
    get_delta_e_interpretation,
    extract_colors,
    analyze_palette_character,
    calculate_spatial_distribution,
    compare_palette_ciede2000,
    generate_color_harmonies,
    generate_css_gradient,
    recolor_image
)


class TestExtractionUtils(unittest.TestCase):

    def setUp(self):
        # Create a synthetic 100x100 RGB image (half red, half blue) for testing
        self.test_img = Image.new('RGB', (100, 100))
        pixels = self.test_img.load()
        for x in range(100):
            for y in range(100):
                if x < 50:
                    pixels[x, y] = (255, 0, 0)  # Pure Red
                else:
                    pixels[x, y] = (0, 0, 255)  # Pure Blue

        self.img_bytes = io.BytesIO()
        self.test_img.save(self.img_bytes, format='PNG')
        self.img_bytes.seek(0)

    def test_color_conversions(self):
        rgb = [139, 92, 246]
        hex_val = rgb_to_hex(rgb)
        self.assertEqual(hex_val, '#8b5cf6')
        self.assertEqual(hex_to_rgb(hex_val), rgb)

        hsl = rgb_to_hsl(rgb)
        self.assertIn('h', hsl)
        self.assertIn('s', hsl)
        self.assertIn('l', hsl)

        lab = rgb_to_lab(rgb)
        self.assertEqual(len(lab), 3)

    def test_ciede2000_delta_e(self):
        lab1 = rgb_to_lab([255, 0, 0])
        lab2 = rgb_to_lab([255, 0, 0])
        lab3 = rgb_to_lab([0, 0, 255])

        # Identical colors must yield 0.0 ΔE₀₀
        self.assertEqual(delta_e_ciede2000(lab1, lab2), 0.0)

        # Distinct colors must yield non-zero ΔE₀₀
        delta_e = delta_e_ciede2000(lab1, lab3)
        self.assertGreater(delta_e, 10.0)
        self.assertIsInstance(get_delta_e_interpretation(delta_e), str)

    def test_extract_colors_kmeans(self):
        self.img_bytes.seek(0)
        palette = extract_colors(
            image_stream=self.img_bytes,
            color_count=2,
            algorithm='kmeans',
            perceptual_filter=False
        )

        self.assertEqual(len(palette), 2)
        self.assertIn('hex', palette[0])
        self.assertIn('accessibility', palette[0])

    def test_extract_colors_with_locked_swatches(self):
        self.img_bytes.seek(0)
        locked = [{'index': 0, 'hex': '#00ff00', 'rgb_values': [0, 255, 0]}]
        palette = extract_colors(
            image_stream=self.img_bytes,
            color_count=3,
            algorithm='kmeans',
            locked_colors=locked
        )

        self.assertEqual(len(palette), 3)
        self.assertTrue(palette[0]['is_locked'])
        self.assertEqual(palette[0]['hex'], '#00ff00')

    def test_analyze_palette_character(self):
        mock_palette = [
            {'hex': '#ef4444', 'rgb_values': [239, 68, 68], 'hsl_values': {'h': 0, 's': 84, 'l': 60}},
            {'hex': '#3b82f6', 'rgb_values': [59, 130, 246], 'hsl_values': {'h': 217, 's': 91, 'l': 60}}
        ]
        analytics = analyze_palette_character(mock_palette)
        self.assertIn('profile', analytics)
        self.assertIn('avg_saturation', analytics)
        self.assertIn('dominant_hue_name', analytics)

    def test_calculate_spatial_distribution(self):
        self.img_bytes.seek(0)
        palette = [
            {'hex': '#ff0000', 'rgb_values': [255, 0, 0], 'name': 'Red'},
            {'hex': '#0000ff', 'rgb_values': [0, 0, 255], 'name': 'Blue'}
        ]
        spatial = calculate_spatial_distribution(self.img_bytes, palette)
        self.assertEqual(len(spatial), 2)
        # In a 50/50 red-blue split image, coverage percentages should be near 50%
        self.assertAlmostEqual(spatial[0]['percentage'], 50.0, delta=10.0)

    def test_compare_palette_ciede2000(self):
        mock_palette = [
            {'hex': '#ef4444', 'rgb_values': [239, 68, 68], 'name': 'Red Swatch'},
            {'hex': '#3b82f6', 'rgb_values': [59, 130, 246], 'name': 'Blue Swatch'}
        ]
        result = compare_palette_ciede2000(mock_palette, library_name='tailwind')
        self.assertIn('closest_matches', result)
        self.assertIn('intra_palette_matrix', result)
        self.assertEqual(len(result['closest_matches']), 2)

    def test_generate_color_harmonies(self):
        harmonies = generate_color_harmonies([139, 92, 246])
        self.assertIn('complementary', harmonies)
        self.assertIn('analogous', harmonies)
        self.assertIn('triadic', harmonies)
        self.assertIn('split_complementary', harmonies)

    def test_generate_css_gradient(self):
        mock_palette = [{'hex': '#8b5cf6'}, {'hex': '#ec4899'}]
        linear = generate_css_gradient(mock_palette, gradient_type='linear', angle=45)
        radial = generate_css_gradient(mock_palette, gradient_type='radial')

        self.assertTrue(linear.startswith('background: linear-gradient(45deg,'))
        self.assertTrue(radial.startswith('background: radial-gradient('))

    def test_recolor_image(self):
        self.img_bytes.seek(0)
        orig_pal = [{'hex': '#ff0000', 'rgb_values': [255, 0, 0]}]
        target_pal = [{'hex': '#00ff00', 'rgb_values': [0, 255, 0]}]

        recolored_bytes = recolor_image(self.img_bytes, orig_pal, target_pal)
        self.assertIsInstance(recolored_bytes, bytes)
        self.assertGreater(len(recolored_bytes), 0)


if __name__ == '__main__':
    unittest.main()