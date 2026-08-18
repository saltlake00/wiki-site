#!/usr/bin/env python3
"""
비디오 → 픽셀 스프라이트시트 변환기
Video to Pixel Art Sprite Sheet Converter

AI 생성 비디오에서 프레임을 추출하고 픽셀아트 스프라이트시트로 변환

사용법:
    python video_to_spritesheet.py walk.mp4 -fps 8 -w 64 -p pico8
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import argparse
from pixel_converter import PixelArtConverter
import math


class VideoToSpriteSheet:
    """비디오를 픽셀 스프라이트시트로 변환"""
    
    def __init__(self):
        self.converter = PixelArtConverter()
    
    def extract_frames(self, video_path, target_fps=None, max_frames=None):
        """
        비디오에서 프레임 추출
        
        Args:
            video_path: 비디오 파일 경로
            target_fps: 목표 FPS (None이면 원본 FPS)
            max_frames: 최대 프레임 수 (None이면 전체)
        
        Returns:
            frames: PIL Image 리스트
            original_fps: 원본 비디오 FPS
        """
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            raise ValueError(f"비디오를 열 수 없습니다: {video_path}")
        
        # 비디오 정보
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"📹 비디오 정보:")
        print(f"   - FPS: {original_fps:.2f}")
        print(f"   - 총 프레임: {total_frames}")
        print(f"   - 길이: {total_frames/original_fps:.2f}초")
        
        # 프레임 샘플링 간격 계산
        if target_fps is None:
            frame_interval = 1
            effective_fps = original_fps
        else:
            frame_interval = max(1, int(original_fps / target_fps))
            effective_fps = original_fps / frame_interval
        
        print(f"🎯 추출 설정:")
        print(f"   - 목표 FPS: {target_fps if target_fps else original_fps:.2f}")
        print(f"   - 프레임 간격: {frame_interval}")
        print(f"   - 실제 FPS: {effective_fps:.2f}")
        
        # 프레임 추출
        frames = []
        frame_idx = 0
        extracted_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 지정된 간격으로 프레임 추출
            if frame_idx % frame_interval == 0:
                # BGR → RGB 변환
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_frame = Image.fromarray(rgb_frame)
                frames.append(pil_frame)
                extracted_count += 1
                
                # 최대 프레임 수 체크
                if max_frames and extracted_count >= max_frames:
                    print(f"⚠️  최대 프레임 수 도달: {max_frames}")
                    break
            
            frame_idx += 1
        
        cap.release()
        
        print(f"✅ 추출 완료: {len(frames)}개 프레임")
        return frames, original_fps
    
    def remove_background(self, frames, threshold=240, crop=True):
        """
        배경 제거 (단색 배경 가정)
        
        Args:
            frames: PIL Image 리스트
            threshold: 배경 임계값 (밝은 배경 제거)
            crop: 투명 영역 자동 크롭
        """
        processed = []
        
        for frame in frames:
            # RGBA로 변환
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')
            
            img_array = np.array(frame)
            
            # 그레이스케일로 밝기 계산
            gray = np.mean(img_array[:, :, :3], axis=2)
            
            # 밝은 배경을 투명하게
            mask = gray < threshold
            img_array[:, :, 3] = (mask * 255).astype(np.uint8)
            
            result = Image.fromarray(img_array)
            
            # 크롭 (투명 영역 제거)
            if crop:
                bbox = result.getbbox()
                if bbox:
                    result = result.crop(bbox)
            
            processed.append(result)
        
        return processed
    
    def normalize_frame_size(self, frames, target_size=None, anchor='bottom-center'):
        """
        모든 프레임을 동일한 캔버스 크기로 정규화
        
        Args:
            frames: PIL Image 리스트
            target_size: (width, height) 또는 None (자동 계산)
            anchor: 정렬 위치
        """
        if target_size is None:
            # 최대 크기 찾기
            max_width = max(f.width for f in frames)
            max_height = max(f.height for f in frames)
            # 2의 제곱수로 올림 (선택)
            # target_size = (2**math.ceil(math.log2(max_width)), 
            #                2**math.ceil(math.log2(max_height)))
            target_size = (max_width, max_height)
        
        print(f"📐 프레임 정규화: {target_size}")
        
        normalized = []
        for frame in frames:
            # 투명 캔버스 생성
            canvas = Image.new('RGBA', target_size, (0, 0, 0, 0))
            
            # 정렬 위치 계산
            if anchor == 'bottom-center':
                x = (target_size[0] - frame.width) // 2
                y = target_size[1] - frame.height
            elif anchor == 'center':
                x = (target_size[0] - frame.width) // 2
                y = (target_size[1] - frame.height) // 2
            elif anchor == 'top-left':
                x, y = 0, 0
            else:
                x, y = 0, 0
            
            # 프레임 붙여넣기
            canvas.paste(frame, (x, y), frame if frame.mode == 'RGBA' else None)
            normalized.append(canvas)
        
        return normalized
    
    def create_sprite_sheet(self, frames, columns=None, spacing=0):
        """
        프레임들을 스프라이트시트로 결합
        
        Args:
            frames: PIL Image 리스트 (모두 같은 크기)
            columns: 열 개수 (None이면 자동 계산)
            spacing: 프레임 간 간격 (픽셀)
        """
        if not frames:
            raise ValueError("프레임이 없습니다")
        
        num_frames = len(frames)
        frame_width, frame_height = frames[0].size
        
        # 열/행 계산
        if columns is None:
            columns = math.ceil(math.sqrt(num_frames))
        rows = math.ceil(num_frames / columns)
        
        # 스프라이트시트 크기
        sheet_width = columns * frame_width + (columns - 1) * spacing
        sheet_height = rows * frame_height + (rows - 1) * spacing
        
        print(f"📄 스프라이트시트 생성:")
        print(f"   - 프레임 크기: {frame_width}x{frame_height}")
        print(f"   - 그리드: {columns}x{rows} ({num_frames}개)")
        print(f"   - 시트 크기: {sheet_width}x{sheet_height}")
        
        # 투명 캔버스 생성
        sprite_sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
        
        # 프레임 배치
        for idx, frame in enumerate(frames):
            row = idx // columns
            col = idx % columns
            
            x = col * (frame_width + spacing)
            y = row * (frame_height + spacing)
            
            sprite_sheet.paste(frame, (x, y), frame)
        
        return sprite_sheet
    
    def convert(self, video_path, output_path, 
                target_fps=8, pixel_width=64, colors=16, palette=None,
                dither=False, remove_bg=False, bg_threshold=240,
                columns=None, spacing=0, max_frames=None,
                anchor='bottom-center'):
        """
        비디오를 픽셀 스프라이트시트로 변환
        
        Args:
            video_path: 입력 비디오
            output_path: 출력 PNG
            target_fps: 추출 FPS
            pixel_width: 픽셀아트 너비
            colors: 색상 수
            palette: 팔레트 이름
            dither: 디더링 여부
            remove_bg: 배경 제거 여부
            bg_threshold: 배경 임계값
            columns: 스프라이트시트 열 수
            spacing: 프레임 간격
            max_frames: 최대 프레임 수
            anchor: 정렬 위치
        """
        print(f"🎬 비디오 → 픽셀 스프라이트시트 변환")
        print(f"📂 입력: {video_path}")
        print()
        
        # 1. 프레임 추출
        frames, original_fps = self.extract_frames(
            video_path, 
            target_fps=target_fps,
            max_frames=max_frames
        )
        print()
        
        # 2. 배경 제거 (선택)
        if remove_bg:
            print(f"🎨 배경 제거 중... (임계값: {bg_threshold})")
            frames = self.remove_background(frames, threshold=bg_threshold)
            print()
        
        # 3. 프레임 정규화 (동일한 크기)
        frames = self.normalize_frame_size(frames, anchor=anchor)
        print()
        
        # 4. 각 프레임을 픽셀아트로 변환
        print(f"🎨 픽셀아트 변환 중... ({pixel_width}px, {colors}색)")
        pixel_frames = []
        
        for idx, frame in enumerate(frames):
            # 임시 저장 경로
            temp_input = Path("temp_frame.png")
            temp_output = Path("temp_pixel.png")
            
            frame.save(temp_input)
            
            # 픽셀 변환
            self.converter.convert(
                str(temp_input),
                str(temp_output),
                width=pixel_width,
                colors=colors,
                palette=palette,
                dither=dither
            )
            
            pixel_frame = Image.open(temp_output)
            pixel_frames.append(pixel_frame)
            
            # 임시 파일 삭제
            temp_input.unlink()
            temp_output.unlink()
            
            print(f"   [{idx+1}/{len(frames)}] 완료", end='\r')
        
        print()
        print()
        
        # 5. 스프라이트시트 생성
        sprite_sheet = self.create_sprite_sheet(
            pixel_frames,
            columns=columns,
            spacing=spacing
        )
        print()
        
        # 6. 저장
        print(f"💾 저장: {output_path}")
        sprite_sheet.save(output_path)
        
        print()
        print(f"✅ 완료!")
        print(f"📊 결과:")
        print(f"   - 프레임 수: {len(pixel_frames)}")
        print(f"   - 프레임 크기: {pixel_frames[0].size}")
        print(f"   - 시트 크기: {sprite_sheet.size}")
        
        return sprite_sheet


def main():
    parser = argparse.ArgumentParser(
        description='비디오를 픽셀 스프라이트시트로 변환',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  # 기본 (8 FPS, 64px, 16색)
  python video_to_spritesheet.py walk.mp4

  # PICO-8 스타일, 배경 제거
  python video_to_spritesheet.py character.mp4 -fps 12 -w 64 -p pico8 --remove-bg

  # 고해상도, 많은 색상
  python video_to_spritesheet.py attack.mp4 -fps 10 -w 128 -c 32 --columns 8

  # 디더링, 최대 24프레임만
  python video_to_spritesheet.py jump.mp4 -p nes -d --max-frames 24
        """
    )
    
    parser.add_argument('video', help='입력 비디오 파일')
    parser.add_argument('-o', '--output', help='출력 PNG (기본: video_spritesheet.png)')
    parser.add_argument('-fps', '--target-fps', type=float, default=8,
                        help='추출 FPS (기본: 8)')
    parser.add_argument('-w', '--width', type=int, default=64,
                        help='픽셀 너비 (기본: 64)')
    parser.add_argument('-c', '--colors', type=int, default=16,
                        help='색상 수 (기본: 16)')
    parser.add_argument('-p', '--palette', 
                        choices=['pico8', 'nes', 'gameboy', 'sweetie16'],
                        help='프리셋 팔레트')
    parser.add_argument('-d', '--dither', action='store_true',
                        help='디더링 적용')
    parser.add_argument('--remove-bg', action='store_true',
                        help='배경 제거 (밝은 단색 배경)')
    parser.add_argument('--bg-threshold', type=int, default=240,
                        help='배경 임계값 (기본: 240)')
    parser.add_argument('--columns', type=int,
                        help='스프라이트시트 열 수 (기본: 자동)')
    parser.add_argument('--spacing', type=int, default=0,
                        help='프레임 간 간격 (기본: 0)')
    parser.add_argument('--max-frames', type=int,
                        help='최대 프레임 수')
    parser.add_argument('--anchor', 
                        choices=['bottom-center', 'center', 'top-left'],
                        default='bottom-center',
                        help='프레임 정렬 위치 (기본: bottom-center)')
    
    args = parser.parse_args()
    
    # 출력 경로 자동 생성
    if not args.output:
        video_path = Path(args.video)
        args.output = video_path.parent / f"{video_path.stem}_spritesheet.png"
    
    # 변환 실행
    converter = VideoToSpriteSheet()
    converter.convert(
        args.video,
        args.output,
        target_fps=args.target_fps,
        pixel_width=args.width,
        colors=args.colors,
        palette=args.palette,
        dither=args.dither,
        remove_bg=args.remove_bg,
        bg_threshold=args.bg_threshold,
        columns=args.columns,
        spacing=args.spacing,
        max_frames=args.max_frames,
        anchor=args.anchor
    )


if __name__ == '__main__':
    main()
