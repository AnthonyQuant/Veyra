import math
import colorsys
import struct
import json
import io
import zipfile
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

# Curated reference dictionary of CSS/Standard named colors (RGB -> Human Name)
COLOR_NAMES_DB = [
    ([0, 0, 0], "Black"),
    ([255, 255, 255], "White"),
    ([128, 128, 128], "Gray"),
    ([192, 192, 192], "Silver"),
    ([128, 0, 0], "Maroon"),
    ([255, 0, 0], "Red"),
    ([128, 0, 128], "Purple"),
    ([255, 0, 255], "Fuchsia"),
    ([0, 128, 0], "Green"),
    ([0, 255, 0], "Lime"),
    ([128, 128, 0], "Olive"),
    ([255, 255, 0], "Yellow"),
    ([0, 0, 128], "Navy"),
    ([0, 0, 255], "Blue"),
    ([0, 128, 128], "Teal"),
    ([0, 255, 255], "Aqua"),
    ([240, 248, 255], "Alice Blue"),
    ([250, 235, 215], "Antique White"),
    ([127, 255, 212], "Aquamarine"),
    ([240, 255, 255], "Azure"),
    ([245, 245, 220], "Beige"),
    ([255, 228, 196], "Bisque"),
    ([255, 235, 205], "Blanched Almond"),
    ([138, 43, 226], "Blue Violet"),
    ([165, 42, 42], "Brown"),
    ([222, 184, 135], "Burly Wood"),
    ([95, 158, 160], "Cadet Blue"),
    ([127, 255, 0], "Chartreuse"),
    ([210, 105, 30], "Chocolate"),
    ([255, 127, 80], "Coral"),
    ([100, 149, 237], "Cornflower Blue"),
    ([255, 248, 220], "Cornsilk"),
    ([220, 20, 60], "Crimson"),
    ([0, 255, 255], "Cyan"),
    ([0, 0, 139], "Dark Blue"),
    ([0, 139, 139], "Dark Cyan"),
    ([184, 134, 11], "Dark Goldenrod"),
    ([169, 169, 169], "Dark Gray"),
    ([0, 100, 0], "Dark Green"),
    ([189, 183, 107], "Dark Khaki"),
    ([139, 0, 139], "Dark Magenta"),
    ([85, 107, 47], "Dark Olive Green"),
    ([255, 140, 0], "Dark Orange"),
    ([153, 50, 204], "Dark Orchid"),
    ([139, 0, 0], "Dark Red"),
    ([233, 150, 122], "Dark Salmon"),
    ([143, 188, 143], "Dark Sea Green"),
    ([72, 61, 139], "Dark Slate Blue"),
    ([47, 79, 79], "Dark Slate Gray"),
    ([0, 206, 209], "Dark Turquoise"),
    ([148, 0, 211], "Dark Violet"),
    ([255, 20, 147], "Deep Pink"),
    ([0, 191, 255], "Deep Sky Blue"),
    ([105, 105, 105], "Dim Gray"),
    ([30, 144, 255], "Dodger Blue"),
    ([178, 34, 34], "Firebrick"),
    ([255, 250, 240], "Floral White"),
    ([34, 139, 34], "Forest Green"),
    ([220, 220, 220], "Gainsboro"),
    ([248, 248, 255], "Ghost White"),
    ([255, 215, 0], "Gold"),
    ([218, 165, 32], "Goldenrod"),
    ([173, 255, 47], "Green Yellow"),
    ([240, 255, 240], "Honeydew"),
    ([255, 105, 180], "Hot Pink"),
    ([205, 92, 92], "Indian Red"),
    ([75, 0, 130], "Indigo"),
    ([255, 255, 240], "Ivory"),
    ([240, 230, 140], "Khaki"),
    ([230, 230, 250], "Lavender"),
    ([255, 240, 245], "Lavender Blush"),
    ([124, 252, 0], "Lawn Green"),
    ([255, 250, 205], "Lemon Chiffon"),
    ([173, 216, 230], "Light Blue"),
    ([240, 128, 128], "Light Coral"),
    ([224, 255, 255], "Light Cyan"),
    ([250, 250, 210], "Light Goldenrod Yellow"),
    ([211, 211, 211], "Light Gray"),
    ([144, 238, 144], "Light Green"),
    ([255, 182, 193], "Light Pink"),
    ([255, 160, 122], "Light Salmon"),
    ([32, 178, 170], "Light Sea Green"),
    ([135, 206, 250], "Light Sky Blue"),
    ([119, 136, 153], "Light Slate Gray"),
    ([176, 196, 222], "Light Steel Blue"),
    ([255, 255, 224], "Light Yellow"),
    ([50, 205, 50], "Lime Green"),
    ([250, 240, 230], "Linen"),
    ([102, 205, 170], "Medium Aquamarine"),
    ([0, 0, 205], "Medium Blue"),
    ([186, 85, 211], "Medium Orchid"),
    ([147, 112, 219], "Medium Purple"),
    ([60, 179, 113], "Medium Sea Green"),
    ([123, 104, 238], "Medium Slate Blue"),
    ([0, 250, 154], "Medium Spring Green"),
    ([72, 209, 204], "Medium Turquoise"),
    ([199, 21, 133], "Medium Violet Red"),
    ([25, 25, 112], "Midnight Blue"),
    ([245, 255, 250], "Mint Cream"),
    ([255, 228, 225], "Misty Rose"),
    ([255, 228, 181], "Moccasin"),
    ([255, 222, 173], "Navajo White"),
    ([253, 245, 230], "Old Lace"),
    ([107, 142, 35], "Olive Drab"),
    ([255, 165, 0], "Orange"),
    ([255, 69, 0], "Orange Red"),
    ([218, 112, 214], "Orchid"),
    ([238, 232, 170], "Pale Goldenrod"),
    ([152, 251, 152], "Pale Green"),
    ([175, 238, 238], "Pale Turquoise"),
    ([219, 112, 147], "Pale Violet Red"),
    ([255, 239, 213], "Papaya Whip"),
    ([255, 218, 185], "Peach Puff"),
    ([205, 133, 63], "Peru"),
    ([255, 192, 203], "Pink"),
    ([221, 160, 221], "Plum"),
    ([176, 224, 230], "Powder Blue"),
    ([102, 51, 153], "Rebecca Purple"),
    ([188, 143, 143], "Rosy Brown"),
    ([65, 105, 225], "Royal Blue"),
    ([139, 69, 19], "Saddle Brown"),
    ([250, 128, 114], "Salmon"),
    ([244, 164, 96], "Sandy Brown"),
    ([46, 139, 87], "Sea Green"),
    ([255, 245, 238], "Seashell"),
    ([160, 82, 45], "Sienna"),
    ([135, 206, 235], "Sky Blue"),
    ([106, 90, 205], "Slate Blue"),
    ([112, 128, 144], "Slate Gray"),
    ([255, 250, 250], "Snow"),
    ([0, 255, 127], "Spring Green"),
    ([70, 130, 180], "Steel Blue"),
    ([210, 180, 140], "Tan"),
    ([216, 191, 216], "Thistle"),
    ([255, 99, 71], "Tomato"),
    ([64, 224, 208], "Turquoise"),
    ([238, 130, 238], "Violet"),
    ([245, 222, 179], "Wheat"),
    ([245, 245, 245], "White Smoke"),
    ([154, 205, 50], "Yellow Green")
]

# Step 18: Standard reference brand libraries for CIEDE2000 matching
REFERENCE_LIBRARIES = {
    'tailwind': [
        ([100, 116, 139], "Tailwind Slate 500", "#64748b"),
        ([239, 68, 68], "Tailwind Red 500", "#ef4444"),
        ([249, 115, 22], "Tailwind Orange 500", "#f97316"),
        ([245, 158, 11], "Tailwind Amber 500", "#f59e0b"),
        ([234, 179, 8], "Tailwind Yellow 500", "#eab308"),
        ([132, 204, 22], "Tailwind Lime 500", "#84cc16"),
        ([34, 197, 94], "Tailwind Green 500", "#22c55e"),
        ([16, 185, 129], "Tailwind Emerald 500", "#10b981"),
        ([20, 184, 166], "Tailwind Teal 500", "#14b8a6"),
        ([6, 182, 212], "Tailwind Cyan 500", "#06b6d4"),
        ([14, 165, 233], "Tailwind Sky 500", "#0ea5e9"),
        ([59, 130, 246], "Tailwind Blue 500", "#3b82f6"),
        ([99, 102, 241], "Tailwind Indigo 500", "#6366f1"),
        ([139, 92, 246], "Tailwind Violet 500", "#8b5cf6"),
        ([168, 85, 247], "Tailwind Purple 500", "#a855f7"),
        ([217, 70, 239], "Tailwind Fuchsia 500", "#d946ef"),
        ([236, 72, 153], "Tailwind Pink 500", "#ec4899"),
        ([244, 63, 94], "Tailwind Rose 500", "#f43f5e")
    ],
    'material': [
        ([244, 67, 54], "Material Red 500", "#f44336"),
        ([233, 30, 99], "Material Pink 500", "#e91e63"),
        ([156, 39, 176], "Material Purple 500", "#9c27b0"),
        ([103, 58, 183], "Material Deep Purple 500", "#673ab7"),
        ([63, 81, 181], "Material Indigo 500", "#3f51b5"),
        ([33, 150, 243], "Material Blue 500", "#2196f3"),
        ([3, 169, 244], "Material Light Blue 500", "#03a9f4"),
        ([0, 188, 212], "Material Cyan 500", "#00bcd4"),
        ([0, 150, 136], "Material Teal 500", "#009688"),
        ([76, 175, 80], "Material Green 500", "#4caf50"),
        ([139, 195, 74], "Material Light Green 500", "#8bc34a"),
        ([205, 220, 57], "Material Lime 500", "#cddc39"),
        ([255, 235, 59], "Material Yellow 500", "#ffeb3b"),
        ([255, 193, 7], "Material Amber 500", "#ffc107"),
        ([255, 152, 0], "Material Orange 500", "#ff9800"),
        ([255, 87, 34], "Material Deep Orange 500", "#ff5722"),
        ([121, 85, 72], "Material Brown 500", "#795548"),
        ([158, 158, 158], "Material Grey 500", "#9e9e9e"),
        ([96, 125, 139], "Material Blue Grey 500", "#607d8b")
    ],
    'ios': [
        ([255, 59, 48], "iOS System Red", "#ff3b30"),
        ([255, 149, 0], "iOS System Orange", "#ff9500"),
        ([255, 204, 0], "iOS System Yellow", "#ffcc00"),
        ([52, 199, 89], "iOS System Green", "#34c759"),
        ([0, 199, 190], "iOS System Mint", "#00c7be"),
        ([48, 176, 199], "iOS System Teal", "#30b0c7"),
        ([50, 173, 230], "iOS System Cyan", "#32ade6"),
        ([0, 122, 255], "iOS System Blue", "#007aff"),
        ([88, 86, 214], "iOS System Indigo", "#5856d6"),
        ([175, 82, 222], "iOS System Purple", "#af52de"),
        ([255, 45, 85], "iOS System Pink", "#ff2d55"),
        ([162, 132, 94], "iOS System Brown", "#a2845e"),
        ([142, 142, 147], "iOS System Gray", "#8e8e93")
    ]
}


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return [int(hex_str[i:i + 2], 16) for i in (0, 2, 4)]


def rgb_to_hsl(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return {
        'h': round(h * 360),
        's': round(s * 100),
        'l': round(l * 100)
    }


def rgb_to_lab(rgb):
    """Converts RGB [0..255] to CIELAB (L*, a*, b*) color space."""
    r_arr = [x / 255.0 for x in rgb]
    r_exp = [(x / 12.92) if x <= 0.04045 else (((x + 0.055) / 1.055) ** 2.4) for x in r_arr]

    X = (r_exp[0] * 0.4124564 + r_exp[1] * 0.3575761 + r_exp[2] * 0.1804375) * 100.0
    Y = (r_exp[0] * 0.2126729 + r_exp[1] * 0.7151522 + r_exp[2] * 0.0721750) * 100.0
    Z = (r_exp[0] * 0.0193339 + r_exp[1] * 0.1191920 + r_exp[2] * 0.9503041) * 100.0

    Xn, Yn, Zn = 95.047, 100.000, 108.883
    x, y, z = X / Xn, Y / Yn, Z / Zn

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t) + (16.0 / 116.0)

    fx, fy, fz = f(x), f(y), f(z)

    L = (116.0 * fy) - 16.0
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)

    return (L, a, b)


def rgb_to_lab_vec(pixels):
    """Step 22 Performance Acceleration: Vectorized conversion of (N, 3) RGB array to (N, 3) CIELAB array."""
    if len(pixels) == 0:
        return np.empty((0, 3))

    pixels = np.asarray(pixels, dtype=np.float64)
    r_arr = pixels / 255.0
    r_exp = np.where(r_arr <= 0.04045, r_arr / 12.92, ((r_arr + 0.055) / 1.055) ** 2.4)

    X = (r_exp[:, 0] * 0.4124564 + r_exp[:, 1] * 0.3575761 + r_exp[:, 2] * 0.1804375) * 100.0
    Y = (r_exp[:, 0] * 0.2126729 + r_exp[:, 1] * 0.7151522 + r_exp[:, 2] * 0.0721750) * 100.0
    Z = (r_exp[:, 0] * 0.0193339 + r_exp[:, 1] * 0.1191920 + r_exp[:, 2] * 0.9503041) * 100.0

    Xn, Yn, Zn = 95.047, 100.000, 108.883
    x, y, z = X / Xn, Y / Yn, Z / Zn

    fx = np.where(x > 0.008856, np.cbrt(x), (7.787 * x) + (16.0 / 116.0))
    fy = np.where(y > 0.008856, np.cbrt(y), (7.787 * y) + (16.0 / 116.0))
    fz = np.where(z > 0.008856, np.cbrt(z), (7.787 * z) + (16.0 / 116.0))

    L = (116.0 * fy) - 16.0
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)

    return np.column_stack((L, a, b))


def delta_e_lab(lab1, lab2):
    """Computes CIELAB Delta E Euclidean distance between two Lab colors."""
    dL = lab1[0] - lab2[0]
    da = lab1[1] - lab2[1]
    db = lab1[2] - lab2[2]
    return math.sqrt(dL * dL + da * da + db * db)


def delta_e_ciede2000(lab1, lab2):
    """Computes CIEDE2000 color difference between two CIELAB colors."""
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2

    C1 = math.sqrt(a1 ** 2 + b1 ** 2)
    C2 = math.sqrt(a2 ** 2 + b2 ** 2)
    C_bar = (C1 + C2) / 2.0

    G = 0.5 * (1 - math.sqrt((C_bar ** 7) / (C_bar ** 7 + 25 ** 7)))

    a1_prime = (1 + G) * a1
    a2_prime = (1 + G) * a2

    C1_prime = math.sqrt(a1_prime ** 2 + b1 ** 2)
    C2_prime = math.sqrt(a2_prime ** 2 + b2 ** 2)

    h1_prime = math.degrees(math.atan2(b1, a1_prime)) % 360
    h2_prime = math.degrees(math.atan2(b2, a2_prime)) % 360

    dL_prime = L2 - L1
    dC_prime = C2_prime - C1_prime

    dh_prime = 0
    if C1_prime * C2_prime != 0:
        if abs(h1_prime - h2_prime) <= 180:
            dh_prime = h2_prime - h1_prime
        elif h2_prime <= h1_prime:
            dh_prime = h2_prime - h1_prime + 360
        else:
            dh_prime = h2_prime - h1_prime - 360

    dH_prime = 2 * math.sqrt(C1_prime * C2_prime) * math.sin(math.radians(dh_prime / 2.0))

    L_bar_prime = (L1 + L2) / 2.0
    C_bar_prime = (C1_prime + C2_prime) / 2.0

    if C1_prime * C2_prime == 0:
        h_bar_prime = h1_prime + h2_prime
    elif abs(h1_prime - h2_prime) <= 180:
        h_bar_prime = (h1_prime + h2_prime) / 2.0
    elif (h1_prime + h2_prime) < 360:
        h_bar_prime = (h1_prime + h2_prime + 360) / 2.0
    else:
        h_bar_prime = (h1_prime + h2_prime - 360) / 2.0

    T = (1 - 0.17 * math.cos(math.radians(h_bar_prime - 30)) +
         0.24 * math.cos(math.radians(2 * h_bar_prime)) +
         0.32 * math.cos(math.radians(3 * h_bar_prime + 6)) -
         0.20 * math.cos(math.radians(4 * h_bar_prime - 63)))

    SL = 1 + (0.015 * (L_bar_prime - 50) ** 2) / math.sqrt(20 + (L_bar_prime - 50) ** 2)
    SC = 1 + 0.045 * C_bar_prime
    SH = 1 + 0.015 * C_bar_prime * T

    RT = -2 * math.sqrt((C_bar_prime ** 7) / (C_bar_prime ** 7 + 25 ** 7)) * math.sin(
        math.radians(60 * math.exp(-(((h_bar_prime - 275) / 25) ** 2))))

    delta_e = math.sqrt(
        (dL_prime / SL) ** 2 +
        (dC_prime / SC) ** 2 +
        (dH_prime / SH) ** 2 +
        RT * (dC_prime / SC) * (dH_prime / SH)
    )
    return round(delta_e, 2)


def get_delta_e_interpretation(delta_e):
    """Provides human-readable perceptual interpretation of CIEDE2000 distance value."""
    if delta_e <= 1.0:
        return "Imperceptible Difference (Exact Match)"
    elif delta_e <= 2.0:
        return "Perceptible on Close Inspection"
    elif delta_e <= 10.0:
        return "Perceptible at a Glance"
    elif delta_e <= 49.0:
        return "Distinctly Different Colors"
    else:
        return "Opposite / High Contrast Colors"


def compare_palette_ciede2000(palette, library_name='tailwind', custom_targets=None):
    """Step 18: Calculates CIEDE2000 (ΔE₀₀) perceptual distance between palette swatches and reference brand colors or custom targets, plus intra-palette distance matrix."""
    if not palette:
        return {
            'library_used': library_name,
            'closest_matches': [],
            'intra_palette_matrix': [],
            'avg_intra_delta_e': 0.0
        }

    targets = []
    if custom_targets and isinstance(custom_targets, list) and len(custom_targets) > 0:
        for item in custom_targets:
            if isinstance(item, str):
                hex_clean = item.strip()
                if not hex_clean.startswith('#') and len(hex_clean) == 6:
                    hex_clean = '#' + hex_clean
                rgb = hex_to_rgb(hex_clean)
                targets.append((rgb, f"Custom {hex_clean.upper()}", hex_clean))
            elif isinstance(item, dict):
                hex_val = item.get('hex', '#000000')
                rgb = item.get('rgb_values') or hex_to_rgb(hex_val)
                name = item.get('name', f"Custom {hex_val.upper()}")
                targets.append((rgb, name, hex_val))
    else:
        targets = REFERENCE_LIBRARIES.get(library_name, REFERENCE_LIBRARIES['tailwind'])

    closest_matches = []
    palette_labs = []

    for idx, swatch in enumerate(palette):
        swatch_rgb = swatch.get('rgb_values') or hex_to_rgb(swatch['hex'])
        swatch_lab = rgb_to_lab(swatch_rgb)
        palette_labs.append((swatch, swatch_lab))

        min_delta_e = float('inf')
        best_target_name = "Unknown"
        best_target_hex = "#000000"

        for t_rgb, t_name, t_hex in targets:
            t_lab = rgb_to_lab(t_rgb)
            d_e = delta_e_ciede2000(swatch_lab, t_lab)
            if d_e < min_delta_e:
                min_delta_e = d_e
                best_target_name = t_name
                best_target_hex = t_hex

        closest_matches.append({
            'swatch_index': idx,
            'swatch_name': swatch.get('name', f"Swatch {idx + 1}"),
            'swatch_hex': swatch['hex'],
            'matched_name': best_target_name,
            'matched_hex': best_target_hex,
            'delta_e': min_delta_e,
            'interpretation': get_delta_e_interpretation(min_delta_e)
        })

    # Pairwise intra-palette distance matrix
    intra_matrix = []
    total_d_e = 0.0
    pair_count = 0
    n = len(palette_labs)

    for i in range(n):
        row_distances = []
        for j in range(n):
            if i == j:
                d_e = 0.0
            else:
                d_e = delta_e_ciede2000(palette_labs[i][1], palette_labs[j][1])
                if i < j:
                    total_d_e += d_e
                    pair_count += 1
            row_distances.append(d_e)

        intra_matrix.append({
            'swatch_index': i,
            'swatch_hex': palette_labs[i][0]['hex'],
            'swatch_name': palette_labs[i][0].get('name', f"Swatch {i + 1}"),
            'distances': row_distances
        })

    avg_intra_delta_e = round(total_d_e / pair_count, 2) if pair_count > 0 else 0.0

    return {
        'library_used': library_name if not custom_targets else 'Custom Target Set',
        'closest_matches': closest_matches,
        'intra_palette_matrix': intra_matrix,
        'avg_intra_delta_e': avg_intra_delta_e
    }


def recolor_image(image_stream, original_palette, target_palette):
    """Step 22 Accelerated: Remaps image pixels in CIELAB space using vectorized NumPy matrix transformations."""
    image_stream.seek(0)
    img = Image.open(image_stream).convert('RGB')

    orig_labs = []
    target_rgbs = []
    for i in range(min(len(original_palette), len(target_palette))):
        o_rgb = original_palette[i].get('rgb_values') or hex_to_rgb(original_palette[i]['hex'])
        t_hex = target_palette[i] if isinstance(target_palette[i], str) else target_palette[i].get('hex', '#000000')
        t_rgb = hex_to_rgb(t_hex)
        orig_labs.append(rgb_to_lab(o_rgb))
        target_rgbs.append(t_rgb)

    if not orig_labs:
        output = io.BytesIO()
        img.save(output, format='PNG')
        return output.getvalue()

    np_img = np.array(img)
    h, w, c = np_img.shape
    pixels = np_img.reshape(-1, 3)

    # Step 22 Acceleration: Vectorized RGB -> CIELAB matrix conversion
    pixel_labs = rgb_to_lab_vec(pixels)
    orig_labs_arr = np.array(orig_labs)
    target_rgbs_arr = np.array(target_rgbs, dtype=np.uint8)

    diff = pixel_labs[:, np.newaxis, :] - orig_labs_arr[np.newaxis, :, :]
    dists = np.sqrt(np.sum(diff ** 2, axis=2))
    closest_indices = np.argmin(dists, axis=1)
    min_dists = np.min(dists, axis=1)

    recolored_pixels = pixels.copy()
    mask = min_dists < 48.0
    recolored_pixels[mask] = target_rgbs_arr[closest_indices[mask]]

    recolored_img = Image.fromarray(recolored_pixels.reshape(h, w, c).astype(np.uint8), 'RGB')
    output = io.BytesIO()
    recolored_img.save(output, format='PNG')
    return output.getvalue()


def get_color_name(rgb):
    """Matches an RGB color to its nearest human-readable color name using CIELAB ΔE distance."""
    input_lab = rgb_to_lab(rgb)
    min_dist = float('inf')
    closest_name = "Unknown Color"

    for db_rgb, name in COLOR_NAMES_DB:
        db_lab = rgb_to_lab(db_rgb)
        dist = delta_e_lab(input_lab, db_lab)
        if dist < min_dist:
            min_dist = dist
            closest_name = name

    return closest_name


def calculate_luminance(rgb):
    """Calculates relative luminance for WCAG 2.1 compliance."""
    r_exp = [x / 255.0 for x in rgb]
    r_lin = [(c / 12.92) if c <= 0.04045 else (((c + 0.055) / 1.055) ** 2.4) for c in r_exp]
    return 0.2126 * r_lin[0] + 0.7152 * r_lin[1] + 0.0722 * r_lin[2]


def calculate_contrast_ratio(rgb1, rgb2):
    """Calculates contrast ratio between two RGB colors (1:1 to 21:1)."""
    l1 = calculate_luminance(rgb1)
    l2 = calculate_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def get_wcag_rating(ratio):
    return {
        'ratio': ratio,
        'aa_normal': ratio >= 4.5,
        'aa_large': ratio >= 3.0,
        'aaa_normal': ratio >= 7.0,
        'aaa_large': ratio >= 4.5
    }


def simulate_cvd(rgb, cvd_type):
    """Simulates Color Vision Deficiency (CVD) using linear LMS matrix transformations."""
    r, g, b = [x / 255.0 for x in rgb]
    if cvd_type == 'protanopia':
        r_sim = 0.56667 * r + 0.43333 * g + 0.0 * b
        g_sim = 0.55833 * r + 0.44167 * g + 0.0 * b
        b_sim = 0.0 * r + 0.24167 * g + 0.75833 * b
    elif cvd_type == 'deuteranopia':
        r_sim = 0.625 * r + 0.375 * g + 0.0 * b
        g_sim = 0.7 * r + 0.3 * g + 0.0 * b
        b_sim = 0.0 * r + 0.3 * g + 0.7 * b
    elif cvd_type == 'tritanopia':
        r_sim = 0.95 * r + 0.05 * g + 0.0 * b
        g_sim = 0.0 * r + 0.43333 * g + 0.56667 * b
        b_sim = 0.0 * r + 0.475 * g + 0.525 * b
    elif cvd_type == 'achromatopsia':
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        r_sim = g_sim = b_sim = gray
    else:
        return rgb

    return [
        max(0, min(255, int(r_sim * 255))),
        max(0, min(255, int(g_sim * 255))),
        max(0, min(255, int(b_sim * 255)))
    ]


def generate_color_harmonies(rgb):
    """Generates Complementary, Analogous, Triadic, and Split-Complementary schemes."""
    hsl = rgb_to_hsl(rgb)
    h, s, l = hsl['h'], hsl['s'], hsl['l']

    def hsl_to_rgb_clamped(h_deg, s_pct, l_pct):
        h_norm = (h_deg % 360) / 360.0
        s_norm = max(0, min(100, s_pct)) / 100.0
        l_norm = max(0, min(100, l_pct)) / 100.0
        r, g, b = colorsys.hls_to_rgb(h_norm, l_norm, s_norm)
        return [max(0, min(255, int(r * 255))), max(0, min(255, int(g * 255))), max(0, min(255, int(b * 255)))]

    return {
        'base': format_color_object(rgb),
        'complementary': [
            format_color_object(rgb),
            format_color_object(hsl_to_rgb_clamped(h + 180, s, l))
        ],
        'analogous': [
            format_color_object(hsl_to_rgb_clamped(h - 30, s, l)),
            format_color_object(rgb),
            format_color_object(hsl_to_rgb_clamped(h + 30, s, l))
        ],
        'triadic': [
            format_color_object(rgb),
            format_color_object(hsl_to_rgb_clamped(h + 120, s, l)),
            format_color_object(hsl_to_rgb_clamped(h + 240, s, l))
        ],
        'split_complementary': [
            format_color_object(rgb),
            format_color_object(hsl_to_rgb_clamped(h + 150, s, l)),
            format_color_object(hsl_to_rgb_clamped(h + 210, s, l))
        ]
    }


def generate_css_gradient(palette, gradient_type='linear', angle=90):
    """Generates pure CSS gradient strings from palette colors."""
    if not palette:
        return ""

    colors = [c['hex'] for c in palette]
    if len(colors) == 1:
        return f"background: {colors[0]};"

    step = 100 / (len(colors) - 1)
    stops = [f"{color} {round(i * step, 1)}%" for i, color in enumerate(colors)]
    stops_str = ", ".join(stops)

    if gradient_type == 'radial':
        return f"background: radial-gradient(circle at center, {stops_str});"
    elif gradient_type == 'conic':
        return f"background: conic-gradient(from 0deg at 50% 50%, {stops_str});"
    else:
        return f"background: linear-gradient({angle}deg, {stops_str});"


def filter_perceptually_similar(rgb_colors, target_count, min_delta_e=12.0, existing_labs=None):
    """Filters candidate RGB colors based on CIELAB Delta E perceptual distance."""
    if not rgb_colors:
        return []

    filtered_rgb = []
    filtered_lab = list(existing_labs) if existing_labs else []

    for rgb in rgb_colors:
        lab = rgb_to_lab(rgb)
        is_distinct = True

        for existing in filtered_lab:
            if delta_e_lab(lab, existing) < min_delta_e:
                is_distinct = False
                break

        if is_distinct:
            filtered_rgb.append(rgb)
            filtered_lab.append(lab)
            if len(filtered_rgb) >= target_count:
                break

    if len(filtered_rgb) < target_count and min_delta_e > 4.0:
        return filter_perceptually_similar(rgb_colors, target_count, min_delta_e=min_delta_e * 0.7,
                                           existing_labs=existing_labs)

    return filtered_rgb


def format_color_object(rgb):
    clamped_rgb = [max(0, min(255, int(c))) for c in rgb]
    hex_val = rgb_to_hex(clamped_rgb)
    hsl_val = rgb_to_hsl(clamped_rgb)
    lab_val = rgb_to_lab(clamped_rgb)
    name_val = get_color_name(clamped_rgb)

    white_contrast = calculate_contrast_ratio(clamped_rgb, [255, 255, 255])
    black_contrast = calculate_contrast_ratio(clamped_rgb, [0, 0, 0])

    return {
        'name': name_val,
        'hex': hex_val,
        'rgb': f"rgb({clamped_rgb[0]}, {clamped_rgb[1]}, {clamped_rgb[2]})",
        'rgb_values': clamped_rgb,
        'hsl': f"hsl({hsl_val['h']}, {hsl_val['s']}%, {hsl_val['l']}%)",
        'hsl_values': hsl_val,
        'lab_values': {
            'l': round(lab_val[0], 1),
            'a': round(lab_val[1], 1),
            'b': round(lab_val[2], 1)
        },
        'accessibility': {
            'contrast_white': white_contrast,
            'wcag_white': get_wcag_rating(white_contrast),
            'contrast_black': black_contrast,
            'wcag_black': get_wcag_rating(black_contrast),
            'best_text_color': '#ffffff' if white_contrast >= black_contrast else '#000000'
        },
        'cvd_simulations': {
            'protanopia': rgb_to_hex(simulate_cvd(clamped_rgb, 'protanopia')),
            'deuteranopia': rgb_to_hex(simulate_cvd(clamped_rgb, 'deuteranopia')),
            'tritanopia': rgb_to_hex(simulate_cvd(clamped_rgb, 'tritanopia')),
            'achromatopsia': rgb_to_hex(simulate_cvd(clamped_rgb, 'achromatopsia'))
        }
    }


def extract_colors(image_stream, color_count=5, algorithm='kmeans', region=None, perceptual_filter=True,
                   locked_colors=None):
    img = Image.open(image_stream).convert('RGB')

    if region and all(k in region for k in ('x', 'y', 'width', 'height')):
        w, h = img.size
        rx = max(0, int(region['x'] * w))
        ry = max(0, int(region['y'] * h))
        rw = int(region['width'] * w)
        rh = int(region['height'] * h)
        if rw > 5 and rh > 5:
            img = img.crop((rx, ry, rx + rw, ry + rh))

    img.thumbnail((300, 300))
    np_img = np.array(img)
    pixels = np_img.reshape(-1, 3)

    if len(pixels) == 0:
        return []

    locked_map = {}
    locked_labs = []
    if locked_colors:
        for item in locked_colors:
            idx = item['index']
            rgb = item.get('rgb_values') or hex_to_rgb(item['hex'])
            locked_map[idx] = format_color_object(rgb)
            locked_labs.append(rgb_to_lab(rgb))

    needed_count = color_count - len(locked_map)

    if needed_count <= 0:
        result = []
        for i in range(color_count):
            if i in locked_map:
                color_obj = locked_map[i]
                color_obj['is_locked'] = True
                result.append(color_obj)
        return result

    candidate_k = min((color_count + 5) * 3, len(pixels)) if perceptual_filter else min(color_count + 5, len(pixels))

    colors = []
    if algorithm == 'kmeans':
        k = max(1, candidate_k)
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=None)
        kmeans.fit(pixels)
        centers = kmeans.cluster_centers_.astype(int)

        labels, counts = np.unique(kmeans.labels_, return_counts=True)
        sorted_indices = np.argsort(-counts)
        colors = [centers[i].tolist() for i in sorted_indices]
    else:
        quantized = img.quantize(colors=candidate_k, method=Image.Quantize.MEDIANCUT)
        palette = quantized.getpalette()[:candidate_k * 3]
        colors = [palette[i:i + 3] for i in range(0, len(palette), 3)]

    if perceptual_filter:
        new_rgb_candidates = filter_perceptually_similar(colors, target_count=needed_count, min_delta_e=12.0,
                                                         existing_labs=locked_labs)
    else:
        new_rgb_candidates = []
        for c in colors:
            c_rgb = [int(x) for x in c]
            if not any(hex_to_rgb(item['hex']) == c_rgb for item in locked_colors or []):
                new_rgb_candidates.append(c_rgb)
            if len(new_rgb_candidates) >= needed_count:
                break

    final_palette = []
    candidate_iter = iter(new_rgb_candidates)

    for i in range(color_count):
        if i in locked_map:
            color_obj = locked_map[i]
            color_obj['is_locked'] = True
            final_palette.append(color_obj)
        else:
            try:
                next_rgb = next(candidate_iter)
                color_obj = format_color_object(next_rgb)
                color_obj['is_locked'] = False
                final_palette.append(color_obj)
            except StopIteration:
                fallback_rgb = [np.random.randint(0, 256) for _ in range(3)]
                color_obj = format_color_object(fallback_rgb)
                color_obj['is_locked'] = False
                final_palette.append(color_obj)

    return final_palette


def analyze_palette_character(palette):
    """Computes palette mood character profile, tonal metrics, and dominant hue spectrum breakdown."""
    if not palette:
        return {
            'profile': 'Empty Palette',
            'description': 'No swatches available for analysis.',
            'avg_saturation': 0,
            'avg_lightness': 0,
            'lightness_range': 0,
            'dominant_hue_name': 'None',
            'hue_distribution': []
        }

    hues = []
    sats = []
    lights = []

    for c in palette:
        hsl_vals = c.get('hsl_values')
        if not hsl_vals and 'hex' in c:
            rgb = c.get('rgb_values') or hex_to_rgb(c['hex'])
            hsl_vals = rgb_to_hsl(rgb)
        if hsl_vals:
            hues.append(hsl_vals['h'])
            sats.append(hsl_vals['s'])
            lights.append(hsl_vals['l'])

    if not hues:
        return {
            'profile': 'Standard Palette',
            'description': 'General color distribution.',
            'avg_saturation': 50,
            'avg_lightness': 50,
            'lightness_range': 0,
            'dominant_hue_name': 'Balanced',
            'hue_distribution': []
        }

    avg_s = int(round(float(np.mean(sats))))
    avg_l = int(round(float(np.mean(lights))))
    min_l = min(lights)
    max_l = max(lights)
    l_range = max_l - min_l

    warm_count = 0
    cool_count = 0
    neutral_count = 0

    hue_bins = {
        'Red': {'count': 0, 'sample': '#ef4444'},
        'Orange': {'count': 0, 'sample': '#f97316'},
        'Yellow': {'count': 0, 'sample': '#eab308'},
        'Green': {'count': 0, 'sample': '#22c55e'},
        'Teal/Cyan': {'count': 0, 'sample': '#06b6d4'},
        'Blue': {'count': 0, 'sample': '#3b82f6'},
        'Purple': {'count': 0, 'sample': '#a855f7'},
        'Pink': {'count': 0, 'sample': '#ec4899'},
        'Neutral': {'count': 0, 'sample': '#64748b'}
    }

    for idx, h in enumerate(hues):
        s = sats[idx]
        l = lights[idx]

        if s < 18 or l < 12 or l > 88:
            neutral_count += 1
            hue_bins['Neutral']['count'] += 1
        else:
            if (h >= 0 and h <= 60) or (h >= 300 and h <= 360):
                warm_count += 1
            elif h > 60 and h < 270:
                cool_count += 1

            if (h >= 345 or h < 15):
                hue_bins['Red']['count'] += 1
            elif 15 <= h < 45:
                hue_bins['Orange']['count'] += 1
            elif 45 <= h < 75:
                hue_bins['Yellow']['count'] += 1
            elif 75 <= h < 165:
                hue_bins['Green']['count'] += 1
            elif 165 <= h < 195:
                hue_bins['Teal/Cyan']['count'] += 1
            elif 195 <= h < 255:
                hue_bins['Blue']['count'] += 1
            elif 255 <= h < 285:
                hue_bins['Purple']['count'] += 1
            elif 285 <= h < 345:
                hue_bins['Pink']['count'] += 1

    total_swatches = len(palette)

    if avg_l > 70 and avg_s < 60 and avg_s > 10:
        profile = "Pastel & Delicate"
        description = "Soft, airy tones with high lightness and gentle saturation suitable for modern, minimalist designs."
    elif avg_s < 28:
        profile = "Muted & Earthy"
        description = "Subdued and understated tones with low chromatic intensity, ideal for organic and relaxed themes."
    elif avg_l < 32:
        profile = "Dark & Moody"
        description = "Deep, rich tones with low lightness, creating a dramatic, mysterious, or high-contrast atmosphere."
    elif warm_count >= cool_count and warm_count > neutral_count:
        profile = "Warm & Energetic"
        description = "Inviting warm hues radiating energy, comfort, and vibrancy."
    elif cool_count > warm_count and cool_count > neutral_count:
        profile = "Cool & Serene"
        description = "Calming blue, green, and purple hues evoking tranquility, professionalism, and clarity."
    elif l_range > 50 and avg_s > 45:
        profile = "High Contrast & Dynamic"
        description = "Bold contrast across lightness levels and vibrant saturation for maximum visual impact."
    else:
        profile = "Balanced & Versatile"
        description = "A well-rounded mixture of hues and tonal values suitable for diverse UI and visual media applications."

    distribution = []
    max_hue_count = 0
    dominant_hue = "Neutral"

    for name, data in hue_bins.items():
        if data['count'] > 0:
            pct = round((data['count'] / total_swatches) * 100)
            distribution.append({
                'name': name,
                'count': data['count'],
                'percentage': pct,
                'sample': data['sample']
            })
            if data['count'] > max_hue_count and name != 'Neutral':
                max_hue_count = data['count']
                dominant_hue = name

    distribution.sort(key=lambda x: x['count'], reverse=True)

    return {
        'profile': profile,
        'description': description,
        'avg_saturation': avg_s,
        'avg_lightness': avg_l,
        'lightness_range': l_range,
        'dominant_hue_name': dominant_hue,
        'hue_distribution': distribution
    }


def calculate_spatial_distribution(image_stream, palette, region=None):
    """Step 22 Accelerated: Computes exact percentage spatial area coverage using vectorized pixel Lab distance matrix."""
    if not palette:
        return []

    image_stream.seek(0)
    img = Image.open(image_stream).convert('RGB')

    if region and all(k in region for k in ('x', 'y', 'width', 'height')):
        w, h = img.size
        rx = max(0, int(region['x'] * w))
        ry = max(0, int(region['y'] * h))
        rw = int(region['width'] * w)
        rh = int(region['height'] * h)
        if rw > 5 and rh > 5:
            img = img.crop((rx, ry, rx + rw, ry + rh))

    img_small = img.resize((160, 160), Image.Resampling.LANCZOS)
    np_img = np.array(img_small)
    h_small, w_small, _ = np_img.shape
    pixels = np_img.reshape(-1, 3)
    total_pixels = len(pixels)

    if total_pixels == 0:
        return []

    palette_rgbs = [c.get('rgb_values') or hex_to_rgb(c['hex']) for c in palette]
    palette_labs = rgb_to_lab_vec(palette_rgbs)

    # Step 22 Acceleration: Vectorized pixel conversion
    pixel_labs = rgb_to_lab_vec(pixels)

    diff = pixel_labs[:, np.newaxis, :] - palette_labs[np.newaxis, :, :]
    dists = np.sqrt(np.sum(diff ** 2, axis=2))
    closest_indices = np.argmin(dists, axis=1)

    distribution = []
    for idx, color in enumerate(palette):
        mask = (closest_indices == idx)
        pixel_count = int(np.sum(mask))
        percentage = round((pixel_count / total_pixels) * 100, 1)

        if pixel_count > 0:
            y_indices, x_indices = np.unravel_index(np.where(mask)[0], (h_small, w_small))
            centroid_x = round(float(np.mean(x_indices) / w_small) * 100, 1)
            centroid_y = round(float(np.mean(y_indices) / h_small) * 100, 1)
        else:
            centroid_x, centroid_y = 50.0, 50.0

        if percentage >= 35.0:
            role_label = "Dominant Background / Primary Area"
        elif percentage >= 15.0:
            role_label = "Secondary Tonal Element"
        elif percentage >= 5.0:
            role_label = "Mid-tone Fill / Regional Swatch"
        else:
            role_label = "Accent / Focal Highlight"

        distribution.append({
            'swatch_index': idx,
            'hex': color['hex'],
            'name': color.get('name', f'Swatch {idx + 1}'),
            'pixel_count': pixel_count,
            'percentage': percentage,
            'role_label': role_label,
            'centroid': {'x': centroid_x, 'y': centroid_y}
        })

    distribution.sort(key=lambda x: x['percentage'], reverse=True)
    return distribution


def generate_ase_file(palette):
    """Generates Adobe Swatch Exchange (.ase) binary byte stream."""
    buffer = bytearray(b'ASEF')
    buffer.extend(struct.pack('>HH', 1, 0))
    buffer.extend(struct.pack('>I', len(palette)))

    for idx, color in enumerate(palette):
        name = color.get('name') or f"Swatch {idx + 1} ({color['hex']})"
        name_utf16 = name.encode('utf-16-be') + b'\x00\x00'
        name_len = len(name) + 1

        rgb = color.get('rgb_values') or hex_to_rgb(color['hex'])
        r_float, g_float, b_float = [c / 255.0 for c in rgb]

        block_data = bytearray()
        block_data.extend(struct.pack('>H', name_len))
        block_data.extend(name_utf16)
        block_data.extend(b'RGB ')
        block_data.extend(struct.pack('>fff', r_float, g_float, b_float))
        block_data.extend(struct.pack('>H', 0))

        buffer.extend(struct.pack('>H', 0x0001))
        buffer.extend(struct.pack('>I', len(block_data)))
        buffer.extend(block_data)

    return bytes(buffer)


def generate_svg_palette(palette):
    """Generates a clean vector SVG graphic card of the palette."""
    swatch_width = 130
    swatch_height = 170
    padding = 20
    header_height = 60
    footer_height = 30
    num_colors = len(palette)
    total_width = padding * 2 + num_colors * swatch_width
    total_height = header_height + swatch_height + footer_height + padding

    rects_svg = []
    for i, c in enumerate(palette):
        x = padding + i * swatch_width
        y = header_height
        hex_code = c['hex'].upper()
        name_str = c.get('name', f"Color {i + 1}")
        rects_svg.append(f'''
        <g transform="translate({x}, {y})">
            <rect width="{swatch_width - 8}" height="{swatch_height - 50}" rx="6" fill="{c['hex']}" />
            <rect y="{swatch_height - 50}" width="{swatch_width - 8}" height="50" rx="0 0 6 6" fill="#1e293b" />
            <text x="{(swatch_width - 8) / 2}" y="{swatch_height - 30}" fill="#8b5cf6" font-family="Segoe UI, sans-serif" font-size="10" font-weight="bold" text-anchor="middle">{name_str}</text>
            <text x="{(swatch_width - 8) / 2}" y="{swatch_height - 12}" fill="#f8fafc" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">{hex_code}</text>
        </g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} {total_height}" width="{total_width}" height="{total_height}">
    <rect width="100%" height="100%" fill="#0f172a" rx="12"/>
    <text x="{padding}" y="38" fill="#8b5cf6" font-family="Segoe UI, sans-serif" font-size="20" font-weight="bold">VEYRA PALETTE STUDIO</text>
    {''.join(rects_svg)}
    <text x="{padding}" y="{total_height - 15}" fill="#64748b" font-family="Segoe UI, sans-serif" font-size="11">Generated with Veyra Palette Studio</text>
</svg>'''


def generate_tailwind_config(palette):
    """Generates Tailwind CSS theme configuration snippet."""
    colors_dict = {
        (c.get('name', f"color-{i + 1}").lower().replace(' ', '-')): c['hex']
        for i, c in enumerate(palette)
    }
    colors_json = json.dumps(colors_dict, indent=4)
    return f"module.exports = {{\n  theme: {{\n    extend: {{\n      colors: {colors_json}\n    }}\n  }}\n}};"


def generate_scss_variables(palette):
    """Generates SCSS variable list with color names."""
    lines = [
        f"${c.get('name', f'color-{i + 1}').lower().replace(' ', '-')}: {c['hex']};"
        for i, c in enumerate(palette)
    ]
    return "\n".join(lines)


def generate_figma_tokens(palette):
    """Generates W3C / Figma Design Tokens JSON format."""
    tokens = {"color": {}}
    for i, c in enumerate(palette):
        key_name = c.get('name', f"swatch-{i + 1}").lower().replace(' ', '-')
        tokens["color"][key_name] = {
            "value": c['hex'],
            "type": "color",
            "description": f"{c.get('name', 'Swatch')} - {c.get('rgb', '')}"
        }
    return json.dumps(tokens, indent=2)


# Step 23 Exporters: GIMP GPL, Adobe ACO, Procreate Swatches, Style Dictionary Tokens

def generate_gpl_palette(palette):
    """Generates GIMP / Inkscape (.gpl) text palette format."""
    lines = [
        "GIMP Palette",
        "Name: Veyra Extracted Palette",
        "Columns: 4",
        "#"
    ]
    for idx, c in enumerate(palette):
        rgb = c.get('rgb_values') or hex_to_rgb(c['hex'])
        name = c.get('name') or f"Swatch {idx + 1}"
        lines.append(f"{rgb[0]:3d} {rgb[1]:3d} {rgb[2]:3d}\t{name}")
    return "\n".join(lines)


def generate_aco_file(palette):
    """Generates Adobe Color Swatch (.aco) v1 and v2 binary stream."""
    buffer = bytearray()
    n_colors = len(palette)

    # Version 1 Header
    buffer.extend(struct.pack('>HH', 1, n_colors))
    for c in palette:
        rgb = c.get('rgb_values') or hex_to_rgb(c['hex'])
        r = rgb[0] * 257
        g = rgb[1] * 257
        b = rgb[2] * 257
        buffer.extend(struct.pack('>HHHHH', 0, r, g, b, 0))

    # Version 2 Header
    buffer.extend(struct.pack('>HH', 2, n_colors))
    for idx, c in enumerate(palette):
        rgb = c.get('rgb_values') or hex_to_rgb(c['hex'])
        r = rgb[0] * 257
        g = rgb[1] * 257
        b = rgb[2] * 257
        buffer.extend(struct.pack('>HHHHH', 0, r, g, b, 0))

        name = c.get('name') or f"Swatch {idx + 1}"
        name_len = len(name) + 1
        name_bytes = name.encode('utf-16-be') + b'\x00\x00'
        buffer.extend(struct.pack('>I', name_len))
        buffer.extend(name_bytes)

    return bytes(buffer)


def generate_procreate_swatches(palette):
    """Generates Procreate (.swatches) zip archive containing swatches.json."""
    swatches_list = []
    for c in palette:
        rgb = c.get('rgb_values') or hex_to_rgb(c['hex'])
        r, g, b = [x / 255.0 for x in rgb]
        v = max(r, g, b)
        diff = v - min(r, g, b)
        s = 0.0 if v == 0 else diff / v
        hsl_h = c.get('hsl_values', {}).get('h', 0)
        h = (hsl_h % 360) / 360.0

        swatches_list.append({
            "hue": h,
            "saturation": s,
            "brightness": v,
            "colorSpace": 0
        })

    json_payload = json.dumps([{"name": "Veyra Palette", "swatches": swatches_list}], indent=2)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('swatches.json', json_payload)

    return zip_buffer.getvalue()


def generate_style_dictionary_tokens(palette):
    """Generates W3C Style Dictionary Design Tokens JSON structure."""
    tokens = {
        "color": {
            "veyra": {}
        }
    }
    for idx, c in enumerate(palette):
        name_slug = (c.get('name') or f"swatch-{idx + 1}").lower().replace(' ', '-')
        tokens["color"]["veyra"][name_slug] = {
            "value": c['hex'],
            "type": "color",
            "comment": f"{c.get('name', 'Swatch')} ({c.get('rgb', '')})",
            "attributes": {
                "category": "color",
                "type": "veyra",
                "item": name_slug
            }
        }
    return json.dumps(tokens, indent=2)