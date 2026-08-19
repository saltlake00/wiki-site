#!/usr/bin/env python3
"""
픽셀아트 변환기 웹 GUI (Flask)
- 브라우저 기반 UI
- 드래그앤드롭 업로드
- 실시간 미리보기
- 결과 다운로드
"""

from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import tempfile
import os
from advanced_converter import AdvancedPixelConverter
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 제한
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

converter = AdvancedPixelConverter()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_to_base64(img):
    """PIL Image를 base64 문자열로 변환"""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # 파일 체크
        if 'file' not in request.files:
            return jsonify({'error': '파일이 업로드되지 않았습니다'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '파일이 선택되지 않았습니다'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '지원하지 않는 파일 형식입니다'}), 400
        
        # 파라미터 추출
        width = int(request.form.get('width', 64))
        colors = int(request.form.get('colors', 16))
        palette = request.form.get('palette', 'none')
        if palette == 'none':
            palette = None
        
        downscale_method = request.form.get('downscale', 'nearest')
        dither_method = request.form.get('dither', 'floyd-steinberg')
        add_outline = request.form.get('outline', 'false') == 'true'
        outline_thickness = int(request.form.get('outline_thickness', 1))
        smooth = int(request.form.get('smooth', 0))
        enhance_contrast = float(request.form.get('contrast', 1.0))
        enhance_saturation = float(request.form.get('saturation', 1.0))
        crt_effect = request.form.get('crt', 'false') == 'true'
        
        # 임시 파일 저장
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 출력 확장자 결정 (GIF는 GIF 유지)
        output_ext = '.gif' if filename.lower().endswith('.gif') else '.png'
        output_filename = f'pixel_{Path(filename).stem}{output_ext}'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        file.save(input_path)
        
        # 변환 실행
        result_img = converter.convert_advanced(
            input_path, output_path,
            width=width,
            colors=colors,
            palette=palette,
            downscale_method=downscale_method,
            dither_method=dither_method,
            add_outline=add_outline,
            outline_thickness=outline_thickness,
            smooth=smooth,
            enhance_contrast=enhance_contrast,
            enhance_saturation=enhance_saturation,
            crt_effect=crt_effect
        )
        
        # 원본 이미지도 로드
        original_img = Image.open(input_path)
        
        # GIF인 경우 파일 경로로 전달 (애니메이션 유지)
        if output_ext == '.gif':
            # GIF는 base64 변환하지 않고 URL로 전달
            original_base64 = image_to_base64(original_img)
            result_url = f'/download/{output_filename}'
            
            try:
                os.remove(input_path)
            except:
                pass
            
            return jsonify({
                'success': True,
                'original': original_base64,
                'result': result_url,  # GIF는 URL로
                'is_animated': True,
                'download_url': result_url
            })
        else:
            # 정적 이미지는 base64로
            original_base64 = image_to_base64(original_img)
            result_base64 = image_to_base64(result_img)
            
            try:
                os.remove(input_path)
            except:
                pass
            
            return jsonify({
                'success': True,
                'original': original_base64,
                'result': result_base64,
                'is_animated': False,
                'download_url': f'/download/{output_filename}'
            })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    print("🎨 픽셀아트 변환기 웹 GUI 시작...")
    print("🌐 브라우저에서 http://localhost:5000 접속")
    app.run(debug=True, host='0.0.0.0', port=5000)
