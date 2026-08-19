#!/usr/bin/env python3
"""
고급 픽셀아트 변환기 GUI (Advanced Version)
- 원본/미리보기 비교 뷰
- 드래그앤드롭 지원
- 모던 UI 디자인
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from pathlib import Path
import threading
import tempfile
import os
from advanced_converter import AdvancedPixelConverter
from PIL import Image, ImageTk


class AdvancedPixelConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("고급 픽셀아트 변환기")
        self.root.geometry("1200x900")
        self.root.configure(bg="#f5f5f5")
        
        self.converter = AdvancedPixelConverter()
        self.input_path = None
        self.output_path = None
        self.original_image = None
        self.preview_image = None
        
        # 임시 파일 경로 (권한 문제 해결)
        self.temp_dir = tempfile.mkdtemp()
        
        self.setup_ui()
    
    def setup_ui(self):
        # 메인 컨테이너
        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # === 왼쪽 패널: 설정 ===
        left_panel = tk.Frame(main_container, bg="#ffffff", relief=tk.RIDGE, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # 타이틀
        title_frame = tk.Frame(left_panel, bg="#4a90e2", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title = tk.Label(
            title_frame,
            text="🎨 픽셀아트 변환기",
            font=("Arial", 18, "bold"),
            bg="#4a90e2",
            fg="white"
        )
        title.pack(pady=15)
        
        # 스크롤 가능한 설정 영역
        canvas = tk.Canvas(left_panel, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # === 드롭존 ===
        dropzone_frame = tk.LabelFrame(
            scrollable_frame,
            text="📁 파일 선택",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#333"
        )
        dropzone_frame.pack(fill=tk.X, padx=15, pady=15)
        
        self.dropzone = tk.Label(
            dropzone_frame,
            text="이미지를 드래그하거나\n클릭하여 선택",
            font=("Arial", 10),
            bg="#e3f2fd",
            fg="#666",
            relief=tk.FLAT,
            borderwidth=2,
            height=3,
            cursor="hand2"
        )
        self.dropzone.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # 드롭존 이벤트
        self.dropzone.drop_target_register(DND_FILES)
        self.dropzone.dnd_bind('<<Drop>>', self.on_drop)
        self.dropzone.bind('<Button-1>', lambda e: self.select_input())
        self.dropzone.bind('<Enter>', lambda e: self.dropzone.config(bg="#bbdefb"))
        self.dropzone.bind('<Leave>', lambda e: self.dropzone.config(bg="#e3f2fd"))
        
        # 파일 정보
        file_info_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        file_info_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        tk.Label(file_info_frame, text="📄", font=("Arial", 10), bg="#ffffff").pack(side=tk.LEFT)
        self.file_label = tk.Label(
            file_info_frame,
            text="파일이 선택되지 않음",
            font=("Arial", 9),
            fg="#999",
            bg="#ffffff"
        )
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        # === 기본 설정 ===
        basic_frame = tk.LabelFrame(
            scrollable_frame,
            text="⚙️ 기본 설정",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#333"
        )
        basic_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        settings_inner = tk.Frame(basic_frame, bg="#ffffff")
        settings_inner.pack(fill=tk.X, padx=10, pady=10)
        
        # 픽셀 너비
        row1 = tk.Frame(settings_inner, bg="#ffffff")
        row1.pack(fill=tk.X, pady=5)
        tk.Label(row1, text="픽셀 너비:", bg="#ffffff", font=("Arial", 9)).pack(side=tk.LEFT)
        self.width_var = tk.IntVar(value=64)
        tk.Spinbox(
            row1,
            from_=16,
            to=256,
            textvariable=self.width_var,
            width=8,
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=5)
        tk.Label(row1, text="px", bg="#ffffff", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # 색상 수
        row2 = tk.Frame(settings_inner, bg="#ffffff")
        row2.pack(fill=tk.X, pady=5)
        tk.Label(row2, text="색상 수:", bg="#ffffff", font=("Arial", 9)).pack(side=tk.LEFT)
        self.colors_var = tk.IntVar(value=16)
        tk.Spinbox(
            row2,
            from_=4,
            to=256,
            textvariable=self.colors_var,
            width=8,
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        # 팔레트
        row3 = tk.Frame(settings_inner, bg="#ffffff")
        row3.pack(fill=tk.X, pady=5)
        tk.Label(row3, text="팔레트:", bg="#ffffff", font=("Arial", 9)).pack(side=tk.LEFT)
        self.palette_var = tk.StringVar(value="없음")
        ttk.Combobox(
            row3,
            textvariable=self.palette_var,
            values=["없음", "pico8", "nes", "gameboy", "sweetie16", "cga"],
            state="readonly",
            width=12,
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        # === 고급 설정 ===
        advanced_frame = tk.LabelFrame(
            scrollable_frame,
            text="🔧 고급 설정",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#333"
        )
        advanced_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        adv_inner = tk.Frame(advanced_frame, bg="#ffffff")
        adv_inner.pack(fill=tk.X, padx=10, pady=10)
        
        # 다운스케일
        row4 = tk.Frame(adv_inner, bg="#ffffff")
        row4.pack(fill=tk.X, pady=5)
        tk.Label(row4, text="다운스케일:", bg="#ffffff", font=("Arial", 9)).pack(side=tk.LEFT)
        self.downscale_var = tk.StringVar(value="nearest")
        ttk.Combobox(
            row4,
            textvariable=self.downscale_var,
            values=["nearest", "pixelate", "lanczos_then_nearest"],
            state="readonly",
            width=15,
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        # 디더링
        row5 = tk.Frame(adv_inner, bg="#ffffff")
        row5.pack(fill=tk.X, pady=5)
        tk.Label(row5, text="디더링:", bg="#ffffff", font=("Arial", 9)).pack(side=tk.LEFT)
        self.dither_var = tk.StringVar(value="floyd-steinberg")
        ttk.Combobox(
            row5,
            textvariable=self.dither_var,
            values=["floyd-steinberg", "ordered", "none"],
            state="readonly",
            width=15,
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        # 외곽선
        self.outline_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            adv_inner,
            text="외곽선 추가",
            variable=self.outline_var,
            bg="#ffffff",
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=5)
        
        # 슬라이더들
        tk.Label(adv_inner, text="대비:", bg="#ffffff", font=("Arial", 9)).pack(anchor=tk.W, pady=(10, 0))
        self.contrast_var = tk.DoubleVar(value=1.0)
        tk.Scale(
            adv_inner,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            variable=self.contrast_var,
            orient=tk.HORIZONTAL,
            bg="#ffffff",
            font=("Arial", 8)
        ).pack(fill=tk.X, pady=2)
        
        tk.Label(adv_inner, text="채도:", bg="#ffffff", font=("Arial", 9)).pack(anchor=tk.W, pady=(5, 0))
        self.saturation_var = tk.DoubleVar(value=1.0)
        tk.Scale(
            adv_inner,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            variable=self.saturation_var,
            orient=tk.HORIZONTAL,
            bg="#ffffff",
            font=("Arial", 8)
        ).pack(fill=tk.X, pady=2)
        
        # CRT 효과
        self.crt_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            adv_inner,
            text="CRT 스캔라인 효과",
            variable=self.crt_var,
            bg="#ffffff",
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=5)
        
        self.outline_thickness_var = tk.IntVar(value=1)
        self.smooth_var = tk.IntVar(value=0)
        
        # === 버튼 ===
        button_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Button(
            button_frame,
            text="🔍 미리보기",
            command=self.preview,
            bg="#4a90e2",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(fill=tk.X, pady=5)
        
        tk.Button(
            button_frame,
            text="✨ 변환 시작",
            command=self.convert,
            bg="#5cb85c",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(fill=tk.X, pady=5)
        
        tk.Button(
            button_frame,
            text="🔄 초기화",
            command=self.reset_settings,
            bg="#f0ad4e",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(fill=tk.X, pady=5)
        
        # === 오른쪽 패널: 비교 뷰 ===
        right_panel = tk.Frame(main_container, bg="#ffffff", relief=tk.RIDGE, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 타이틀
        compare_title = tk.Frame(right_panel, bg="#4a90e2", height=60)
        compare_title.pack(fill=tk.X)
        compare_title.pack_propagate(False)
        
        tk.Label(
            compare_title,
            text="📊 원본 / 미리보기 비교",
            font=("Arial", 16, "bold"),
            bg="#4a90e2",
            fg="white"
        ).pack(pady=15)
        
        # 비교 컨테이너
        compare_container = tk.Frame(right_panel, bg="#ffffff")
        compare_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 원본 (왼쪽)
        original_frame = tk.Frame(compare_container, bg="#f9f9f9", relief=tk.RIDGE, bd=1)
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            original_frame,
            text="📷 원본",
            font=("Arial", 12, "bold"),
            bg="#f9f9f9",
            fg="#333"
        ).pack(pady=10)
        
        self.original_canvas = tk.Canvas(
            original_frame,
            bg="#ffffff",
            highlightthickness=0
        )
        self.original_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 미리보기 (오른쪽)
        preview_frame = tk.Frame(compare_container, bg="#f9f9f9", relief=tk.RIDGE, bd=1)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            preview_frame,
            text="✨ 미리보기",
            font=("Arial", 12, "bold"),
            bg="#f9f9f9",
            fg="#333"
        ).pack(pady=10)
        
        self.preview_canvas = tk.Canvas(
            preview_frame,
            bg="#ffffff",
            highlightthickness=0
        )
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 상태 바
        status_frame = tk.Frame(self.root, bg="#333", height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="준비")
        tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg="#333",
            fg="white"
        ).pack(side=tk.LEFT, padx=15)
        
        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate', length=200)
        self.progress_bar.pack(side=tk.RIGHT, padx=15)
    
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0].strip('{}')
            self.load_file(file_path)
    
    def load_file(self, file_path):
        try:
            self.input_path = Path(file_path)
            valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
            
            if self.input_path.suffix.lower() not in valid_extensions:
                messagebox.showerror("오류", "지원하지 않는 파일 형식입니다.")
                return
            
            # UI 업데이트
            self.file_label.config(text=self.input_path.name, fg="#333")
            self.dropzone.config(
                text=f"✓ {self.input_path.name}\n클릭하여 다른 파일 선택",
                bg="#c8e6c9",
                fg="#2e7d32"
            )
            
            # 출력 경로 자동 생성
            self.output_path = self.input_path.parent / f"{self.input_path.stem}_pixel.png"
            
            # 원본 이미지 표시
            self.show_original()
            
            self.status_var.set(f"✓ 파일 로드 완료: {self.input_path.name}")
            
        except Exception as e:
            messagebox.showerror("오류", f"파일 로드 실패:\n{e}")
    
    def show_original(self):
        """원본 이미지 표시"""
        try:
            img = Image.open(self.input_path)
            self.display_image(img, self.original_canvas, "original")
        except Exception as e:
            print(f"원본 표시 오류: {e}")
    
    def display_image(self, img, canvas, tag):
        """캔버스에 이미지 표시"""
        canvas_width = canvas.winfo_width() or 400
        canvas_height = canvas.winfo_height() or 600
        
        # 비율 유지 리사이즈
        img_ratio = img.width / img.height
        canvas_ratio = canvas_width / canvas_height
        
        if img_ratio > canvas_ratio:
            new_width = canvas_width - 20
            new_height = int(new_width / img_ratio)
        else:
            new_height = canvas_height - 20
            new_width = int(new_height * img_ratio)
        
        img_resized = img.resize((new_width, new_height), Image.NEAREST)
        
        if tag == "original":
            self.original_image = ImageTk.PhotoImage(img_resized)
            canvas.delete("all")
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2
            canvas.create_image(x, y, image=self.original_image, anchor=tk.NW)
        else:
            self.preview_image = ImageTk.PhotoImage(img_resized)
            canvas.delete("all")
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2
            canvas.create_image(x, y, image=self.preview_image, anchor=tk.NW)
    
    def reset_settings(self):
        self.width_var.set(64)
        self.colors_var.set(16)
        self.palette_var.set("없음")
        self.downscale_var.set("nearest")
        self.dither_var.set("floyd-steinberg")
        self.outline_var.set(False)
        self.contrast_var.set(1.0)
        self.saturation_var.set(1.0)
        self.crt_var.set(False)
        self.status_var.set("설정 초기화 완료")
    
    def select_input(self):
        filename = filedialog.askopenfilename(
            title="입력 파일 선택",
            filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.gif *.bmp *.webp")]
        )
        if filename:
            self.load_file(filename)
    
    def preview(self):
        if not self.input_path:
            messagebox.showwarning("경고", "먼저 파일을 선택하세요!")
            return
        
        self.status_var.set("미리보기 생성 중...")
        self.progress_bar.start()
        
        def _preview():
            try:
                # 임시 파일 경로 (권한 문제 해결)
                temp_output = os.path.join(self.temp_dir, "preview.png")
                palette = None if self.palette_var.get() == "없음" else self.palette_var.get()
                
                self.converter.convert_advanced(
                    str(self.input_path), temp_output,
                    width=self.width_var.get(),
                    colors=self.colors_var.get(),
                    palette=palette,
                    downscale_method=self.downscale_var.get(),
                    dither_method=self.dither_var.get(),
                    add_outline=self.outline_var.get(),
                    outline_thickness=self.outline_thickness_var.get(),
                    smooth=self.smooth_var.get(),
                    enhance_contrast=self.contrast_var.get(),
                    enhance_saturation=self.saturation_var.get(),
                    crt_effect=self.crt_var.get()
                )
                
                img = Image.open(temp_output)
                self.display_image(img, self.preview_canvas, "preview")
                
                self.status_var.set("✓ 미리보기 완료!")
            except Exception as e:
                messagebox.showerror("오류", f"미리보기 실패:\n{e}")
                self.status_var.set("미리보기 실패")
            finally:
                self.progress_bar.stop()
        
        threading.Thread(target=_preview, daemon=True).start()
    
    def convert(self):
        if not self.input_path:
            messagebox.showwarning("경고", "먼저 파일을 선택하세요!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="저장 위치 선택",
            defaultextension=".png",
            initialfile=f"{self.input_path.stem}_pixel.png",
            filetypes=[("PNG 이미지", "*.png")]
        )
        
        if not filename:
            return
        
        self.output_path = Path(filename)
        self.status_var.set("변환 중...")
        self.progress_bar.start()
        
        def _convert():
            try:
                palette = None if self.palette_var.get() == "없음" else self.palette_var.get()
                
                self.converter.convert_advanced(
                    str(self.input_path), str(self.output_path),
                    width=self.width_var.get(),
                    colors=self.colors_var.get(),
                    palette=palette,
                    downscale_method=self.downscale_var.get(),
                    dither_method=self.dither_var.get(),
                    add_outline=self.outline_var.get(),
                    outline_thickness=self.outline_thickness_var.get(),
                    smooth=self.smooth_var.get(),
                    enhance_contrast=self.contrast_var.get(),
                    enhance_saturation=self.saturation_var.get(),
                    crt_effect=self.crt_var.get()
                )
                
                self.status_var.set(f"✅ 저장 완료: {self.output_path.name}")
                messagebox.showinfo("완료", f"변환 완료!\n{self.output_path}")
                
                # 결과를 미리보기에 표시
                img = Image.open(self.output_path)
                self.display_image(img, self.preview_canvas, "preview")
                
            except Exception as e:
                messagebox.showerror("오류", f"변환 실패:\n{e}")
                self.status_var.set("변환 실패")
            finally:
                self.progress_bar.stop()
        
        threading.Thread(target=_convert, daemon=True).start()
    
    def __del__(self):
        """임시 디렉토리 정리"""
        try:
            import shutil
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except:
            pass


def main():
    root = TkinterDnD.Tk()
    app = AdvancedPixelConverterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
