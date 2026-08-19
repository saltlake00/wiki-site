#!/usr/bin/env python3
"""
고급 픽셀아트 변환기 GUI (Advanced Version)
- 다운스케일 방법 선택
- 디더링 방법 선택
- 외곽선, 대비/채도 조정
- CRT 효과
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from advanced_converter import AdvancedPixelConverter
from PIL import Image, ImageTk


class AdvancedPixelConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("고급 픽셀아트 변환기")
        self.root.geometry("900x1000")
        
        self.converter = AdvancedPixelConverter()
        self.input_path = None
        self.output_path = None
        self.preview_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 타이틀
        title = ttk.Label(main_frame, text="🎨 고급 픽셀아트 변환기", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # === 입력/출력 파일 ===
        ttk.Label(main_frame, text="입력 파일:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.input_label = ttk.Label(main_frame, text="파일을 선택하세요", relief=tk.SUNKEN, width=50)
        self.input_label.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="찾아보기", command=self.select_input).grid(row=1, column=2, padx=5)
        
        ttk.Label(main_frame, text="출력 경로:", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_label = ttk.Label(main_frame, text="자동 생성", relief=tk.SUNKEN, width=50)
        self.output_label.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="변경", command=self.select_output).grid(row=2, column=2, padx=5)
        
        # === 기본 설정 ===
        basic_frame = ttk.LabelFrame(main_frame, text="기본 설정", padding="10")
        basic_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(basic_frame, text="픽셀 너비:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.width_var = tk.IntVar(value=64)
        ttk.Spinbox(basic_frame, from_=16, to=256, textvariable=self.width_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(basic_frame, text="색상 수:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.colors_var = tk.IntVar(value=16)
        ttk.Spinbox(basic_frame, from_=4, to=256, textvariable=self.colors_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(basic_frame, text="팔레트:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.palette_var = tk.StringVar(value="없음")
        ttk.Combobox(basic_frame, textvariable=self.palette_var, 
                     values=["없음", "pico8", "nes", "gameboy", "sweetie16", "cga"],
                     state="readonly", width=15).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # === 고급 설정 ===
        advanced_frame = ttk.LabelFrame(main_frame, text="고급 설정", padding="10")
        advanced_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 다운스케일 방법
        ttk.Label(advanced_frame, text="다운스케일:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.downscale_var = tk.StringVar(value="nearest")
        downscale_combo = ttk.Combobox(advanced_frame, textvariable=self.downscale_var,
                                       values=["nearest", "pixelate", "lanczos_then_nearest", "xbr"],
                                       state="readonly", width=18)
        downscale_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Label(advanced_frame, text="(nearest=선명, pixelate=그리드평균)", font=("Arial", 8)).grid(row=0, column=2, sticky=tk.W)
        
        # 디더링 방법
        ttk.Label(advanced_frame, text="디더링:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dither_var = tk.StringVar(value="floyd-steinberg")
        dither_combo = ttk.Combobox(advanced_frame, textvariable=self.dither_var,
                                    values=["floyd-steinberg", "ordered", "none"],
                                    state="readonly", width=18)
        dither_combo.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # 외곽선
        self.outline_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(advanced_frame, text="외곽선", variable=self.outline_var).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(advanced_frame, text="두께:").grid(row=2, column=1, sticky=tk.W)
        self.outline_thickness_var = tk.IntVar(value=1)
        ttk.Spinbox(advanced_frame, from_=1, to=5, textvariable=self.outline_thickness_var, width=5).grid(row=2, column=2, sticky=tk.W)
        
        # 스무딩
        ttk.Label(advanced_frame, text="스무딩:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.smooth_var = tk.IntVar(value=0)
        ttk.Scale(advanced_frame, from_=0, to=5, variable=self.smooth_var, orient=tk.HORIZONTAL, length=150).grid(row=3, column=1, columnspan=2, sticky=tk.W, padx=5)
        
        # 대비
        ttk.Label(advanced_frame, text="대비:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.contrast_var = tk.DoubleVar(value=1.0)
        ttk.Scale(advanced_frame, from_=0.5, to=2.0, variable=self.contrast_var, orient=tk.HORIZONTAL, length=150).grid(row=4, column=1, columnspan=2, sticky=tk.W, padx=5)
        
        # 채도
        ttk.Label(advanced_frame, text="채도:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.saturation_var = tk.DoubleVar(value=1.0)
        ttk.Scale(advanced_frame, from_=0.5, to=2.0, variable=self.saturation_var, orient=tk.HORIZONTAL, length=150).grid(row=5, column=1, columnspan=2, sticky=tk.W, padx=5)
        
        # CRT 효과
        self.crt_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(advanced_frame, text="CRT 스캔라인 효과", variable=self.crt_var).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # === 프리뷰 ===
        preview_frame = ttk.LabelFrame(main_frame, text="미리보기", padding="10")
        preview_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.preview_canvas = tk.Canvas(preview_frame, width=700, height=400, bg="white")
        self.preview_canvas.pack()
        
        # === 진행 상태 ===
        self.progress_var = tk.StringVar(value="대기 중...")
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var, font=("Arial", 10))
        self.progress_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # === 버튼 ===
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="변환 시작", command=self.convert, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="미리보기", command=self.preview, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="설정 초기화", command=self.reset_settings, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="종료", command=self.root.quit, width=15).pack(side=tk.LEFT, padx=5)
        
        # 그리드 가중치
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
    
    def reset_settings(self):
        """설정 초기화"""
        self.width_var.set(64)
        self.colors_var.set(16)
        self.palette_var.set("없음")
        self.downscale_var.set("nearest")
        self.dither_var.set("floyd-steinberg")
        self.outline_var.set(False)
        self.outline_thickness_var.set(1)
        self.smooth_var.set(0)
        self.contrast_var.set(1.0)
        self.saturation_var.set(1.0)
        self.crt_var.set(False)
        messagebox.showinfo("초기화", "설정이 초기화되었습니다.")
    
    def select_input(self):
        filename = filedialog.askopenfilename(
            title="입력 파일 선택",
            filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"), ("모든 파일", "*.*")]
        )
        if filename:
            self.input_path = Path(filename)
            self.input_label.config(text=self.input_path.name)
            if not self.output_path:
                self.output_path = self.input_path.parent / f"{self.input_path.stem}_advanced_pixel.png"
                self.output_label.config(text=self.output_path.name)
    
    def select_output(self):
        filename = filedialog.asksaveasfilename(
            title="출력 파일 저장",
            defaultextension=".png",
            filetypes=[("PNG 이미지", "*.png")]
        )
        if filename:
            self.output_path = Path(filename)
            self.output_label.config(text=self.output_path.name)
    
    def preview(self):
        if not self.input_path:
            messagebox.showwarning("경고", "먼저 입력 파일을 선택하세요!")
            return
        
        self.progress_var.set("미리보기 생성 중...")
        self.progress_bar.start()
        
        def _preview():
            try:
                temp_output = Path("temp_advanced_preview.png")
                palette = None if self.palette_var.get() == "없음" else self.palette_var.get()
                
                self.converter.convert_advanced(
                    str(self.input_path), str(temp_output),
                    width=self.width_var.get(), colors=self.colors_var.get(), palette=palette,
                    downscale_method=self.downscale_var.get(), dither_method=self.dither_var.get(),
                    add_outline=self.outline_var.get(), outline_thickness=self.outline_thickness_var.get(),
                    smooth=self.smooth_var.get(), enhance_contrast=self.contrast_var.get(),
                    enhance_saturation=self.saturation_var.get(), crt_effect=self.crt_var.get()
                )
                
                self.show_preview(temp_output)
                temp_output.unlink()
                self.progress_var.set("미리보기 완료!")
            except Exception as e:
                messagebox.showerror("오류", f"미리보기 실패:\n{e}")
                self.progress_var.set("미리보기 실패")
            finally:
                self.progress_bar.stop()
        
        threading.Thread(target=_preview, daemon=True).start()
    
    def show_preview(self, image_path):
        img = Image.open(image_path)
        canvas_width, canvas_height = 700, 400
        img_ratio = img.width / img.height
        canvas_ratio = canvas_width / canvas_height
        
        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)
        
        img_resized = img.resize((new_width, new_height), Image.NEAREST)
        self.preview_image = ImageTk.PhotoImage(img_resized)
        
        self.preview_canvas.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.preview_canvas.create_image(x, y, image=self.preview_image, anchor=tk.NW)
    
    def convert(self):
        if not self.input_path:
            messagebox.showwarning("경고", "먼저 입력 파일을 선택하세요!")
            return
        if not self.output_path:
            messagebox.showwarning("경고", "출력 경로가 설정되지 않았습니다!")
            return
        
        self.progress_var.set("변환 중...")
        self.progress_bar.start()
        
        def _convert():
            try:
                palette = None if self.palette_var.get() == "없음" else self.palette_var.get()
                
                self.converter.convert_advanced(
                    str(self.input_path), str(self.output_path),
                    width=self.width_var.get(), colors=self.colors_var.get(), palette=palette,
                    downscale_method=self.downscale_var.get(), dither_method=self.dither_var.get(),
                    add_outline=self.outline_var.get(), outline_thickness=self.outline_thickness_var.get(),
                    smooth=self.smooth_var.get(), enhance_contrast=self.contrast_var.get(),
                    enhance_saturation=self.saturation_var.get(), crt_effect=self.crt_var.get()
                )
                
                self.progress_var.set(f"✅ 완료: {self.output_path.name}")
                messagebox.showinfo("완료", f"변환 완료!\n저장 위치: {self.output_path}")
                self.show_preview(self.output_path)
            except Exception as e:
                messagebox.showerror("오류", f"변환 실패:\n{e}")
                self.progress_var.set("변환 실패")
            finally:
                self.progress_bar.stop()
        
        threading.Thread(target=_convert, daemon=True).start()


def main():
    root = tk.Tk()
    app = AdvancedPixelConverterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
