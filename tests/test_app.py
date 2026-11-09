import io
import json
import unittest
from PIL import Image
from app import app


class TestFlaskAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Generate mock test image
        test_img = Image.new('RGB', (60, 60), color=(139, 92, 246))
        self.img_bytes = io.BytesIO()
        test_img.save(self.img_bytes, format='PNG')
        self.img_bytes.seek(0)

    def test_health_check(self):
        res = self.app.get('/api/health')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'healthy')

    def test_get_samples(self):
        res = self.app.get('/api/samples')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['samples']), 0)

    def test_extract_endpoint(self):
        self.img_bytes.seek(0)
        data = {
            'image': (self.img_bytes, 'test.png'),
            'color_count': '4',
            'algorithm': 'kmeans',
            'perceptual_filter': 'true'
        }
        res = self.app.post('/api/extract', data=data, content_type='multipart/form-data')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_data['success'])
        self.assertEqual(len(res_data['palette']), 4)
        self.assertIn('analytics', res_data)
        self.assertIn('spatial_distribution', res_data)

    def test_recolor_endpoint(self):
        self.img_bytes.seek(0)
        orig_pal = json.dumps([{'hex': '#8b5cf6', 'rgb_values': [139, 92, 246]}])
        target_pal = json.dumps([{'hex': '#10b981', 'rgb_values': [16, 185, 129]}])

        data = {
            'image': (self.img_bytes, 'test.png'),
            'original_palette': orig_pal,
            'target_palette': target_pal
        }
        res = self.app.post('/api/recolor', data=data, content_type='multipart/form-data')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'image/png')

    def test_compare_ciede2000_endpoint(self):
        payload = {
            'palette': [{'hex': '#8b5cf6', 'rgb_values': [139, 92, 246]}],
            'library': 'tailwind'
        }
        res = self.app.post('/api/compare_ciede2000', json=payload)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_data['success'])
        self.assertIn('comparison', res_data)

    def test_gradient_endpoint(self):
        payload = {
            'palette': [{'hex': '#8b5cf6'}, {'hex': '#ec4899'}],
            'type': 'linear',
            'angle': 90
        }
        res = self.app.post('/api/gradient', json=payload)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_data['success'])
        self.assertIn('css', res_data)

    def test_export_snippets_endpoint(self):
        payload = {
            'palette': [{'hex': '#8b5cf6', 'name': 'Violet'}]
        }
        for fmt in ['tailwind', 'scss', 'figma']:
            res = self.app.post(f'/api/export/{fmt}', json=payload)
            res_data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(res_data['success'])
            self.assertIn('content', res_data)

    def test_export_ase_file_endpoint(self):
        payload = {
            'palette': [{'hex': '#8b5cf6', 'name': 'Violet', 'rgb_values': [139, 92, 246]}]
        }
        res = self.app.post('/api/export/ase', json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'application/octet-stream')


if __name__ == '__main__':
    unittest.main()