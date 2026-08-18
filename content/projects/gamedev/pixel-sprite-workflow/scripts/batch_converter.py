#!/usr/bin/env python3
"""
배치 픽셀아트 변환기 (Batch Pixel Art Converter)
폴더 내 모든 이미지를 픽셀아트로 일괄 변환

사용법:
    python batch_converter.py input_folder/ -o output_folder/ -w 64 -p pico8
"""

import argparse
from pathlib import Path
from pixel_converter import PixelArtConverter
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def process_image(converter, input_path, output_folder, width, colors, palette, dither):
    """단일 이미지 처리"""
    try:
        output_path = output_folder / f"{input_path.stem}_pixel.png"
        converter.convert(
            str(input_path),
            str(output_path),
            width=width,
            colors=colors,
            palette=palette,
            dither=dither
        )
        return True, input_path.name
    except Exception as e:
        return False, f"{input_path.name}: {e}"


def main():
    parser = argparse.ArgumentParser(description='폴더 내 이미지 일괄 픽셀아트 변환')
    parser.add_argument('input_folder', help='입력 폴더 경로')
    parser.add_argument('-o', '--output', help='출력 폴더 (기본: input_folder_pixel/)')
    parser.add_argument('-w', '--width', type=int, default=64, help='목표 너비 (기본: 64)')
    parser.add_argument('-c', '--colors', type=int, default=16, help='색상 수 (기본: 16)')
    parser.add_argument('-p', '--palette', choices=['pico8', 'nes', 'gameboy', 'sweetie16'],
                        help='프리셋 팔레트')
    parser.add_argument('-d', '--dither', action='store_true', help='디더링 적용')
    parser.add_argument('-j', '--jobs', type=int, default=4, help='병렬 처리 수 (기본: 4)')
    
    args = parser.parse_args()
    
    input_folder = Path(args.input_folder)
    if not input_folder.exists():
        print(f"❌ 폴더가 없습니다: {input_folder}")
        return
    
    # 출력 폴더 생성
    if not args.output:
        output_folder = input_folder.parent / f"{input_folder.name}_pixel"
    else:
        output_folder = Path(args.output)
    
    output_folder.mkdir(exist_ok=True, parents=True)
    
    # 이미지 파일 찾기
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    image_files = [f for f in input_folder.iterdir() 
                   if f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"❌ 이미지가 없습니다: {input_folder}")
        return
    
    print(f"📂 입력: {input_folder}")
    print(f"📂 출력: {output_folder}")
    print(f"🖼️  이미지 수: {len(image_files)}")
    print(f"⚙️  설정: {args.width}px, {args.colors}색" + 
          (f", {args.palette} 팔레트" if args.palette else "") +
          (", 디더링" if args.dither else ""))
    print(f"🚀 병렬 처리: {args.jobs}개")
    print()
    
    # 변환 실행
    converter = PixelArtConverter()
    success_count = 0
    failed = []
    
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(
                process_image, converter, img, output_folder,
                args.width, args.colors, args.palette, args.dither
            ): img for img in image_files
        }
        
        with tqdm(total=len(image_files), desc="변환 중") as pbar:
            for future in as_completed(futures):
                success, result = future.result()
                if success:
                    success_count += 1
                else:
                    failed.append(result)
                pbar.update(1)
    
    print()
    print(f"✅ 성공: {success_count}/{len(image_files)}")
    if failed:
        print(f"❌ 실패: {len(failed)}")
        for err in failed:
            print(f"   - {err}")


if __name__ == '__main__':
    main()
