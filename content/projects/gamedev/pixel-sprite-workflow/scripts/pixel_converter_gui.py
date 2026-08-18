#!/usr/bin/env python3
"""
픽셀아트 변환기 GUI
Pixel Art Converter GUI

tkinter 기반 간편한 GUI 인터페이스
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from pixel_converter import PixelArtConverter
from PIL import Image, ImageTk
import sys


class PixelConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("픽셀아트 변환기")
        self.root.geometry("800x900")
        
        self.converter = PixelArtConverter()
        self.input_path = None
        self.output_path = None
        self.preview_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 타이틀
        title = ttk.Label(main_frame, text="🎨 픽셀아트 변환기", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # === 입력 파일 ===
        ttk.Label(main_frame, text="입력 파일:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.input_label = ttk.Label(main_frame, text="파일을 선택하세요", relief=tk.SUNKEN, width=50)
        self.input_label.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Button(main_frame, text="찾아보기", command=self.select_input).grid(row=1, column=2, padx=5)
        
        # === 출력 경로 ===
        ttk.Label(main_frame, text="출력 경로:", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.output_label = ttk.Label(main_frame, text="자동 생성", relief=tk.SUNKEN, width=50)
        self.output_label.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Button(main_frame, text="변경", command=self.select_output).grid(row=2, column=2, padx=5)
        
        # === 설정 프레임 ===
        settings_frame = ttk.LabelFrame(main_frame, text="변환 설정", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 너비
        ttk.Label(settings_frame, text="픽셀 너비:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.width_var = tk.IntVar(value=64)
        width_spinbox = ttk.Spinbox(settings_frame, from_=16, to=256, textvariable=self.width_var, width=10)
        width_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Label(settings_frame, text="px").grid(row=0, column=2, sticky=tk.W)
        
        # 색상 수
        ttk.Label(settings_frame, text="색상 수:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.colors_var = tk.IntVar(value=16)
        colors_spinbox = ttk.Spinbox(settings_frame, from_=4, to=256, textvariable=self.colors_var, width=10)
        colors_spinbox.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # 팔레트
        ttk.Label(settings_frame, text="팔레트:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.palette_var = tk.StringVar(value="없음")
        palette_combo = ttk.Combobox(settings_frame, textvariable=self.palette_var, 
                                      values=["없음", "pico8", "nes", "gameboy", "sweetie16"],
                                      state="readonly", width=15)
        palette_combo.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # 디더링
        self.dither_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="디더링 (Floyd-Steinberg)", 
                        variable=self.dither_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # === 프리뷰 ===
        preview_frame = ttk.LabelFrame(main_frame, text="미리보기", padding="10")
        preview_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.preview_canvas = tk.Canvas(preview_frame, width=600, height=400, bg="white")
        self.preview_canvas.pack()
        
        # === 진행 상태 ===
        self.progress_var = tk.StringVar(value="대기 중...")
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var, font=("Arial", 10))
        self.progress_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # === 버튼 ===
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="변환 시작", command=self.convert, 
                   style="Accent.TButton", width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="미리보기", command=self.preview, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="종료", command=self.root.quit, width=15).pack(side=tk.LEFT, padx=5)
        
        # 그리드 가중치
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def select_input(self):
        filename = filedialog.askopenfilename(
            title="입력 파일 선택",
            filetypes=[
                ("이미지 파일", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("모든 파일", "*.*")
            ]
        )
        if filename:
            self.input_path = Path(filename)
            self.input_label.config(text=self.input_path.name)
            
            # 출력 경로 자동 생성
            if not self.output_path:
                self.output_path = self.input_path.parent / f"{self.input_path.stem}_pixel.png"
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
                # 임시 파일로 변환
                temp_output = Path("temp_preview.png")
                
                palette = None if self.palette_var.get() == "없음" else self.palette_var.get()
                
                self.converter.convert(
                    str(self.input_path),
                    str(temp_output),
                    width=self.width_var.get(),
                    colors=self.colors_var.get(),
                    palette=palette,
                    dither=self.dither_var.get()
                )
                
                # 프리뷰 표시
                self.show_preview(temp_output)
                
                # 임시 파일 삭제
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
        
        # 캔버스 크기에 맞게 리사이즈 (비율 유지)
        canvas_width = 600
        canvas_height = 400
        
        img_ratio = img.width / img.height
        canvas_ratio = canvas_width / canvas_height
        
        if img_ratio > canvas_ratio:
            # 너비 기준
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            # 높이 기준
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)
        
        # Nearest Neighbor로 리사이즈 (픽셀 경계 유지)
        img_resized = img.resize((new_width, new_height), Image.NEAREST)
        
        # tkinter용 이미지로 변환
        self.preview_image = ImageTk.PhotoImage(img_resized)
        
        # 캔버스에 표시
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
                
                self.converter.convert(
                    str(self.input_path),
                    str(self.output_path),
                    width=self.width_var.get(),
                    colors=self.colors_var.get(),
                    palette=palette,
                    dither=self.dither_var.get()
                )
                
                self.progress_var.set(f"✅ 완료: {self.output_path.name}")
                messagebox.showinfo("완료", f"변환 완료!\n저장 위치: {self.output_path}")
                
                # 결과 프리뷰
                self.show_preview(self.output_path)
                
            except Exception as e:
                messagebox.showerror("오류", f"변환 실패:\n{e}")
                self.progress_var.set("변환 실패")
            finally:
                self.progress_bar.stop()
        
        threading.Thread(target=_convert, daemon=True).start()


def main():
    root = tk.Tk()
    app = PixelConverterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
