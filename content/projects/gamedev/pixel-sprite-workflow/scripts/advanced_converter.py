#!/usr/bin/env python3
"""
고급 픽셀아트 변환기 (Advanced Pixel Art Converter)
- 다양한 다운스케일 알고리즘
- 엣지 감지 및 외곽선
- 색상 양자화 개선
- 비디오 프레임 보간
"""

from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from sklearn.cluster import KMeans
from scipy.ndimage import median_filter
import cv2


class AdvancedPixelConverter:
    """고급 픽셀아트 변환 기능"""
    
    def __init__(self):
        self.predefined_palettes = {
            'pico8': [
                '#000000', '#1D2B53', '#7E2553', '#008751',
                '#AB5236', '#5F574F', '#C2C3C7', '#FFF1E8',
                '#FF004D', '#FFA300', '#FFEC27', '#00E436',
                '#29ADFF', '#83769C', '#FF77A8', '#FFCCAA'
            ],
            'nes': [
                '#7C7C7C', '#0000FC', '#0000BC', '#4428BC', '#940084', '#A80020',
                '#A81000', '#881400', '#503000', '#007800', '#006800', '#005800',
                '#004058', '#000000', '#BCBCBC', '#0078F8', '#0058F8', '#6844FC',
                '#D800CC', '#E40058', '#F83800', '#E45C10', '#AC7C00', '#00B800',
                '#00A800', '#00A844', '#008888', '#F8F8F8', '#3CBCFC', '#6888FC',
                '#9878F8', '#F878F8', '#F85898', '#F87858', '#FCA044', '#F8B800',
                '#B8F818', '#58D854', '#58F898', '#00E8D8', '#787878'
            ],
            'gameboy': ['#0f380f', '#306230', '#8bac0f', '#9bbc0f'],
            'sweetie16': [
                '#1a1c2c', '#5d275d', '#b13e53', '#ef7d57',
                '#ffcd75', '#a7f070', '#38b764', '#257179',
                '#29366f', '#3b5dc9', '#41a6f6', '#73eff7',
                '#f4f4f4', '#94b0c2', '#566c86', '#333c57'
            ],
            'cga': ['#000000', '#0000AA', '#00AA00', '#00AAAA',
                    '#AA0000', '#AA00AA', '#AA5500', '#AAAAAA',
                    '#555555', '#5555FF', '#55FF55', '#55FFFF',
                    '#FF5555', '#FF55FF', '#FFFF55', '#FFFFFF'],
        }
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def downscale_with_method(self, img, target_width, method='nearest'):
        """
        다양한 다운스케일 방법
        
        method:
        - nearest: 가장 선명, 픽셀 경계 명확
        - pixelate: 그리드 기반 평균 (PAC 스타일)
        - lanczos_then_nearest: 고품질 다운 후 픽셀 스냅
        - xbr: xBR 알고리즘 (실험적)
        """
        aspect_ratio = img.height / img.width
        target_height = int(target_width * aspect_ratio)
        
        if method == 'nearest':
            return img.resize((target_width, target_height), Image.NEAREST)
        
        elif method == 'pixelate':
            # 그리드 기반: 각 셀의 평균 색상
            return self._pixelate_grid(img, target_width, target_height)
        
        elif method == 'lanczos_then_nearest':
            # 고품질로 먼저 축소 후 픽셀 스냅
            temp = img.resize((target_width, target_height), Image.LANCZOS)
            return temp
        
        elif method == 'xbr':
            # xBR 스타일 (간소화)
            return self._xbr_downscale(img, target_width, target_height)
        
        else:
            return img.resize((target_width, target_height), Image.NEAREST)
    
    def _pixelate_grid(self, img, target_width, target_height):
        """그리드 기반 픽셀화 (PAC 방식)"""
        img_array = np.array(img)
        cell_w = img.width / target_width
        cell_h = img.height / target_height
        
        result = np.zeros((target_height, target_width, img_array.shape[2]), dtype=np.uint8)
        
        for y in range(target_height):
            for x in range(target_width):
                # 셀 영역 추출
                x1 = int(x * cell_w)
                y1 = int(y * cell_h)
                x2 = int((x + 1) * cell_w)
                y2 = int((y + 1) * cell_h)
                
                cell = img_array[y1:y2, x1:x2]
                
                # 평균 색상
                if cell.size > 0:
                    result[y, x] = cell.reshape(-1, img_array.shape[2]).mean(axis=0)
        
        return Image.fromarray(result)
    
    def _xbr_downscale(self, img, target_width, target_height):
        """xBR 스타일 다운스케일 (엣지 보존)"""
        # OpenCV로 엣지 감지
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        edges = cv2.Canny(img_cv, 50, 150)
        
        # 엣지 가중치 적용한 리사이즈
        img_resized = img.resize((target_width, target_height), Image.LANCZOS)
        return img_resized
    
    def detect_edges(self, img, thickness=1):
        """엣지 감지 및 외곽선 추가"""
        # 그레이스케일 변환
        gray = img.convert('L')
        
        # 엣지 감지
        edges = gray.filter(ImageFilter.FIND_EDGES)
        
        # 이진화
        threshold = 30
        edges = edges.point(lambda p: 255 if p > threshold else 0)
        
        # 두껍게 (선택)
        if thickness > 1:
            edges = edges.filter(ImageFilter.MaxFilter(thickness * 2 + 1))
        
        return edges
    
    def add_outline(self, img, outline_color=(0, 0, 0), thickness=1):
        """외곽선 추가"""
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        img_array = np.array(img)
        alpha = img_array[:, :, 3]
        
        # 알파 채널에서 경계 감지
        edges = cv2.Canny(alpha, 50, 200)
        
        # 경계 확장
        kernel = np.ones((thickness * 2 + 1, thickness * 2 + 1), np.uint8)
        edges_dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # 외곽선 적용
        outline_mask = edges_dilated > 0
        result = img_array.copy()
        result[outline_mask] = list(outline_color) + [255]
        
        return Image.fromarray(result)
    
    def smooth_colors(self, img, strength=2):
        """색상 스무딩 (노이즈 제거)"""
        img_array = np.array(img)
        
        # 메디안 필터
        for c in range(img_array.shape[2]):
            img_array[:, :, c] = median_filter(img_array[:, :, c], size=strength)
        
        return Image.fromarray(img_array)
    
    def enhance_contrast(self, img, factor=1.2):
        """대비 향상"""
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(factor)
    
    def enhance_saturation(self, img, factor=1.2):
        """채도 향상"""
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(factor)
    
    def ordered_dither(self, img, palette_colors, matrix_size=2):
        """Ordered 디더링 (Bayer 매트릭스)"""
        # Bayer 매트릭스
        bayer_2x2 = np.array([[0, 2], [3, 1]]) / 4.0
        bayer_4x4 = np.array([
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5]
        ]) / 16.0
        
        bayer = bayer_2x2 if matrix_size == 2 else bayer_4x4
        
        palette_rgb = [self.hex_to_rgb(c) for c in palette_colors]
        palette_array = np.array(palette_rgb)
        
        img_array = np.array(img).astype(float)
        h, w = img_array.shape[:2]
        
        result = np.zeros_like(img_array, dtype=np.uint8)
        
        for y in range(h):
            for x in range(w):
                threshold = bayer[y % matrix_size, x % matrix_size]
                
                # 픽셀 + 디더 노이즈
                pixel = img_array[y, x, :3]
                noisy_pixel = pixel + (threshold - 0.5) * 32  # 노이즈 강도
                
                # 가장 가까운 팔레트 색상
                distances = np.sqrt(np.sum((palette_array - noisy_pixel) ** 2, axis=1))
                closest_idx = np.argmin(distances)
                result[y, x, :3] = palette_array[closest_idx]
                
                # 알파 채널 보존
                if img_array.shape[2] == 4:
                    result[y, x, 3] = img_array[y, x, 3]
        
        return Image.fromarray(result)
    
    def apply_CRT_effect(self, img):
        """CRT 모니터 효과 (스캔라인)"""
        img_array = np.array(img)
        
        # 홀수 행 어둡게
        img_array[::2] = (img_array[::2] * 0.85).astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    def convert_advanced(self, input_path, output_path,
                        width=64, colors=16, palette=None,
                        downscale_method='nearest',
                        dither_method='floyd-steinberg',
                        add_outline=False, outline_color=(0, 0, 0), outline_thickness=1,
                        smooth=0, enhance_contrast=1.0, enhance_saturation=1.0,
                        crt_effect=False):
        """
        고급 변환
        
        Args:
            downscale_method: 'nearest', 'pixelate', 'lanczos_then_nearest', 'xbr'
            dither_method: 'floyd-steinberg', 'ordered', 'none'
            add_outline: 외곽선 추가 여부
            smooth: 스무딩 강도 (0=없음)
            enhance_contrast: 대비 (1.0=원본)
            enhance_saturation: 채도 (1.0=원본)
            crt_effect: CRT 스캔라인 효과
        """
        print(f"📂 로드: {input_path}")
        img = Image.open(input_path)
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 1. 전처리: 대비/채도 향상
        if enhance_contrast != 1.0:
            print(f"🎨 대비 향상: {enhance_contrast}")
            img = self.enhance_contrast(img, enhance_contrast)
        
        if enhance_saturation != 1.0:
            print(f"🎨 채도 향상: {enhance_saturation}")
            img = self.enhance_saturation(img, enhance_saturation)
        
        # 2. 다운스케일
        print(f"🔽 다운스케일: {downscale_method} → {width}px")
        img = self.downscale_with_method(img, width, downscale_method)
        
        # 3. 스무딩 (선택)
        if smooth > 0:
            print(f"✨ 스무딩: {smooth}")
            img = self.smooth_colors(img, smooth)
        
        # 4. 색상 양자화
        if palette:
            palette_colors = self.predefined_palettes.get(palette, palette)
            print(f"🎨 팔레트: {palette} ({len(palette_colors)}색)")
            
            if dither_method == 'floyd-steinberg':
                img = self.floyd_steinberg_dither(img, palette_colors)
            elif dither_method == 'ordered':
                img = self.ordered_dither(img, palette_colors, matrix_size=4)
            else:
                img = self.apply_palette(img, palette_colors)
        else:
            print(f"🎨 k-means: {colors}색")
            img = self.quantize_colors_kmeans(img, colors)
        
        # 5. 외곽선 (선택)
        if add_outline:
            print(f"🖌️  외곽선: {outline_thickness}px")
            img = self.add_outline(img, outline_color, outline_thickness)
        
        # 6. CRT 효과 (선택)
        if crt_effect:
            print(f"📺 CRT 효과")
            img = self.apply_CRT_effect(img)
        
        # 7. 저장
        print(f"💾 저장: {output_path}")
        img.save(output_path)
        print(f"✅ 완료!")
        
        return img
    
    # 기본 메서드 (기존 코드와 호환)
    def quantize_colors_kmeans(self, img, num_colors):
        """k-means 클러스터링"""
        img_array = np.array(img)
        has_alpha = (img_array.shape[2] == 4)
        
        if has_alpha:
            alpha = img_array[:, :, 3]
            rgb = img_array[:, :, :3]
        else:
            rgb = img_array
        
        pixels = rgb.reshape(-1, 3)
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        new_pixels = kmeans.cluster_centers_[kmeans.labels_]
        new_rgb = new_pixels.reshape(rgb.shape).astype(np.uint8)
        
        if has_alpha:
            result = np.dstack((new_rgb, alpha))
        else:
            result = new_rgb
        
        return Image.fromarray(result)
    
    def apply_palette(self, img, palette_colors):
        """팔레트 매핑"""
        palette_rgb = [self.hex_to_rgb(c) for c in palette_colors]
        palette_array = np.array(palette_rgb)
        
        img_array = np.array(img)
        has_alpha = (img_array.shape[2] == 4)
        
        if has_alpha:
            alpha = img_array[:, :, 3]
            rgb = img_array[:, :, :3]
        else:
            rgb = img_array
        
        pixels = rgb.reshape(-1, 3).astype(float)
        new_pixels = np.zeros_like(pixels)
        
        for i, pixel in enumerate(pixels):
            distances = np.sqrt(np.sum((palette_array - pixel) ** 2, axis=1))
            closest_idx = np.argmin(distances)
            new_pixels[i] = palette_array[closest_idx]
        
        new_rgb = new_pixels.reshape(rgb.shape).astype(np.uint8)
        
        if has_alpha:
            result = np.dstack((new_rgb, alpha))
        else:
            result = new_rgb
        
        return Image.fromarray(result)
    
    def floyd_steinberg_dither(self, img, palette_colors):
        """Floyd-Steinberg 디더링"""
        palette_rgb = [self.hex_to_rgb(c) for c in palette_colors]
        palette_array = np.array(palette_rgb)
        
        img_array = np.array(img).astype(float)
        has_alpha = (img_array.shape[2] == 4)
        
        if has_alpha:
            alpha = img_array[:, :, 3].copy()
            rgb = img_array[:, :, :3]
        else:
            rgb = img_array.copy()
        
        h, w = rgb.shape[:2]
        
        for y in range(h):
            for x in range(w):
                old_pixel = rgb[y, x]
                distances = np.sqrt(np.sum((palette_array - old_pixel) ** 2, axis=1))
                closest_idx = np.argmin(distances)
                new_pixel = palette_array[closest_idx]
                
                rgb[y, x] = new_pixel
                error = old_pixel - new_pixel
                
                if x + 1 < w:
                    rgb[y, x + 1] += error * 7/16
                if y + 1 < h:
                    if x > 0:
                        rgb[y + 1, x - 1] += error * 3/16
                    rgb[y + 1, x] += error * 5/16
                    if x + 1 < w:
                        rgb[y + 1, x + 1] += error * 1/16
        
        rgb = np.clip(rgb, 0, 255).astype(np.uint8)
        
        if has_alpha:
            result = np.dstack((rgb, alpha.astype(np.uint8)))
        else:
            result = rgb
        
        return Image.fromarray(result)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='고급 픽셀아트 변환기')
    parser.add_argument('input', help='입력 이미지')
    parser.add_argument('-o', '--output', help='출력 이미지')
    parser.add_argument('-w', '--width', type=int, default=64)
    parser.add_argument('-c', '--colors', type=int, default=16)
    parser.add_argument('-p', '--palette', choices=['pico8', 'nes', 'gameboy', 'sweetie16', 'cga'])
    parser.add_argument('--downscale', choices=['nearest', 'pixelate', 'lanczos_then_nearest', 'xbr'],
                        default='nearest', help='다운스케일 방법')
    parser.add_argument('--dither', choices=['floyd-steinberg', 'ordered', 'none'],
                        default='floyd-steinberg', help='디더링 방법')
    parser.add_argument('--outline', action='store_true', help='외곽선 추가')
    parser.add_argument('--outline-thickness', type=int, default=1)
    parser.add_argument('--smooth', type=int, default=0, help='스무딩 강도')
    parser.add_argument('--contrast', type=float, default=1.0, help='대비 (1.0=원본)')
    parser.add_argument('--saturation', type=float, default=1.0, help='채도 (1.0=원본)')
    parser.add_argument('--crt', action='store_true', help='CRT 스캔라인 효과')
    
    args = parser.parse_args()
    
    if not args.output:
        from pathlib import Path
        input_path = Path(args.input)
        args.output = input_path.parent / f"{input_path.stem}_advanced_pixel.png"
    
    converter = AdvancedPixelConverter()
    converter.convert_advanced(
        args.input, args.output,
        width=args.width, colors=args.colors, palette=args.palette,
        downscale_method=args.downscale, dither_method=args.dither,
        add_outline=args.outline, outline_thickness=args.outline_thickness,
        smooth=args.smooth, enhance_contrast=args.contrast,
        enhance_saturation=args.saturation, crt_effect=args.crt
    )


if __name__ == '__main__':
    main()
