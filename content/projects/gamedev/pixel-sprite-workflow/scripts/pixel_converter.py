#!/usr/bin/env python3
"""
픽셀아트 변환기 (Pixel Art Converter)
AI 생성 이미지를 True Pixel Art로 변환

사용법:
    python pixel_converter.py input.png -o output.png -w 64 -c 16
"""

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import argparse
from pathlib import Path


class PixelArtConverter:
    """픽셀아트 변환 클래스"""
    
    def __init__(self):
        self.predefined_palettes = {
            'pico8': [
                '#000000', '#1D2B53', '#7E2553', '#008751',
                '#AB5236', '#5F574F', '#C2C3C7', '#FFF1E8',
                '#FF004D', '#FFA300', '#FFEC27', '#00E436',
                '#29ADFF', '#83769C', '#FF77A8', '#FFCCAA'
            ],
            'nes': [
                '#7C7C7C', '#0000FC', '#0000BC', '#4428BC',
                '#940084', '#A80020', '#A81000', '#881400',
                '#503000', '#007800', '#006800', '#005800',
                '#004058', '#000000', '#000000', '#000000',
                '#BCBCBC', '#0078F8', '#0058F8', '#6844FC',
                '#D800CC', '#E40058', '#F83800', '#E45C10',
                '#AC7C00', '#00B800', '#00A800', '#00A844',
                '#008888', '#000000', '#000000', '#000000',
                '#F8F8F8', '#3CBCFC', '#6888FC', '#9878F8',
                '#F878F8', '#F85898', '#F87858', '#FCA044',
                '#F8B800', '#B8F818', '#58D854', '#58F898',
                '#00E8D8', '#787878', '#000000', '#000000'
            ],
            'gameboy': ['#0f380f', '#306230', '#8bac0f', '#9bbc0f'],
            'sweetie16': [
                '#1a1c2c', '#5d275d', '#b13e53', '#ef7d57',
                '#ffcd75', '#a7f070', '#38b764', '#257179',
                '#29366f', '#3b5dc9', '#41a6f6', '#73eff7',
                '#f4f4f4', '#94b0c2', '#566c86', '#333c57'
            ]
        }
    
    def hex_to_rgb(self, hex_color):
        """HEX 색상을 RGB로 변환"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb):
        """RGB를 HEX로 변환"""
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    def resize_nearest_neighbor(self, img, target_width):
        """Nearest Neighbor 리사이즈 (픽셀 경계 선명)"""
        aspect_ratio = img.height / img.width
        target_height = int(target_width * aspect_ratio)
        return img.resize((target_width, target_height), Image.NEAREST)
    
    def quantize_colors_kmeans(self, img, num_colors):
        """k-means 클러스터링으로 색상 축소"""
        # 이미지를 numpy 배열로 변환
        img_array = np.array(img)
        original_shape = img_array.shape
        
        # 알파 채널 분리
        has_alpha = (img_array.shape[2] == 4)
        if has_alpha:
            alpha = img_array[:, :, 3]
            rgb = img_array[:, :, :3]
        else:
            rgb = img_array
        
        # 픽셀을 1D 배열로 변환
        pixels = rgb.reshape(-1, 3)
        
        # k-means 클러스터링
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # 각 픽셀을 가장 가까운 클러스터 중심으로 교체
        new_pixels = kmeans.cluster_centers_[kmeans.labels_]
        
        # 원본 형태로 복원
        new_rgb = new_pixels.reshape(original_shape[:2] + (3,)).astype(np.uint8)
        
        # 알파 채널 복원
        if has_alpha:
            new_img_array = np.dstack((new_rgb, alpha))
        else:
            new_img_array = new_rgb
        
        return Image.fromarray(new_img_array)
    
    def apply_palette(self, img, palette_colors):
        """특정 팔레트로 색상 매핑"""
        # 팔레트를 RGB로 변환
        palette_rgb = [self.hex_to_rgb(c) for c in palette_colors]
        palette_array = np.array(palette_rgb)
        
        # 이미지를 numpy 배열로
        img_array = np.array(img)
        original_shape = img_array.shape
        
        has_alpha = (img_array.shape[2] == 4)
        if has_alpha:
            alpha = img_array[:, :, 3]
            rgb = img_array[:, :, :3]
        else:
            rgb = img_array
        
        pixels = rgb.reshape(-1, 3).astype(float)
        
        # 각 픽셀을 가장 가까운 팔레트 색상으로 매핑
        new_pixels = np.zeros_like(pixels)
        for i, pixel in enumerate(pixels):
            distances = np.sqrt(np.sum((palette_array - pixel) ** 2, axis=1))
            closest_idx = np.argmin(distances)
            new_pixels[i] = palette_array[closest_idx]
        
        new_rgb = new_pixels.reshape(original_shape[:2] + (3,)).astype(np.uint8)
        
        if has_alpha:
            new_img_array = np.dstack((new_rgb, alpha))
        else:
            new_img_array = new_rgb
        
        return Image.fromarray(new_img_array)
    
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
        
        height, width = rgb.shape[:2]
        
        for y in range(height):
            for x in range(width):
                old_pixel = rgb[y, x]
                
                # 가장 가까운 팔레트 색상 찾기
                distances = np.sqrt(np.sum((palette_array - old_pixel) ** 2, axis=1))
                closest_idx = np.argmin(distances)
                new_pixel = palette_array[closest_idx]
                
                rgb[y, x] = new_pixel
                error = old_pixel - new_pixel
                
                # 오차 확산
                if x + 1 < width:
                    rgb[y, x + 1] += error * 7/16
                if y + 1 < height:
                    if x > 0:
                        rgb[y + 1, x - 1] += error * 3/16
                    rgb[y + 1, x] += error * 5/16
                    if x + 1 < width:
                        rgb[y + 1, x + 1] += error * 1/16
        
        rgb = np.clip(rgb, 0, 255).astype(np.uint8)
        
        if has_alpha:
            result = np.dstack((rgb, alpha.astype(np.uint8)))
        else:
            result = rgb
        
        return Image.fromarray(result)
    
    def convert(self, input_path, output_path, width=64, colors=16, 
                palette=None, dither=False, keep_aspect=True):
        """
        이미지를 픽셀아트로 변환
        
        Args:
            input_path: 입력 이미지 경로
            output_path: 출력 이미지 경로
            width: 목표 너비 (픽셀)
            colors: 색상 수 (palette 지정 시 무시)
            palette: 팔레트 이름 또는 HEX 색상 리스트
            dither: 디더링 적용 여부
            keep_aspect: 종횡비 유지
        """
        print(f"📂 로드: {input_path}")
        img = Image.open(input_path)
        
        # RGBA로 변환 (투명도 보존)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 1. 리사이즈 (Nearest Neighbor)
        print(f"🔽 리사이즈: {img.size} → {width}px 너비")
        img = self.resize_nearest_neighbor(img, width)
        
        # 2. 색상 축소
        if palette:
            # 팔레트가 문자열이면 프리셋 사용
            if isinstance(palette, str) and palette in self.predefined_palettes:
                palette_colors = self.predefined_palettes[palette]
                print(f"🎨 팔레트: {palette} ({len(palette_colors)}색)")
            else:
                palette_colors = palette
                print(f"🎨 커스텀 팔레트: {len(palette_colors)}색")
            
            if dither:
                print(f"✨ Floyd-Steinberg 디더링 적용")
                img = self.floyd_steinberg_dither(img, palette_colors)
            else:
                img = self.apply_palette(img, palette_colors)
        else:
            print(f"🎨 k-means 색상 축소: {colors}색")
            img = self.quantize_colors_kmeans(img, colors)
        
        # 3. 저장
        print(f"💾 저장: {output_path}")
        img.save(output_path)
        print(f"✅ 완료! ({img.size[0]}x{img.size[1]} 픽셀)")
        
        return img


def main():
    parser = argparse.ArgumentParser(description='AI 이미지를 픽셀아트로 변환')
    parser.add_argument('input', help='입력 이미지 경로')
    parser.add_argument('-o', '--output', help='출력 이미지 경로 (기본: input_pixel.png)')
    parser.add_argument('-w', '--width', type=int, default=64, help='목표 너비 (기본: 64)')
    parser.add_argument('-c', '--colors', type=int, default=16, help='색상 수 (기본: 16)')
    parser.add_argument('-p', '--palette', choices=['pico8', 'nes', 'gameboy', 'sweetie16'],
                        help='프리셋 팔레트')
    parser.add_argument('-d', '--dither', action='store_true', help='디더링 적용')
    
    args = parser.parse_args()
    
    # 출력 경로 자동 생성
    if not args.output:
        input_path = Path(args.input)
        args.output = input_path.parent / f"{input_path.stem}_pixel.png"
    
    # 변환 실행
    converter = PixelArtConverter()
    converter.convert(
        args.input,
        args.output,
        width=args.width,
        colors=args.colors,
        palette=args.palette,
        dither=args.dither
    )


if __name__ == '__main__':
    main()
