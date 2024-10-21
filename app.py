# Creado por: https://github.com/HydroAndrew22
# Agradecimiento: https://www.facebook.com/reel/1904207853424690

# Instalación pip install qrcode[pil] "el [pil] es decirle que es para python)"

from flask import Flask, render_template, request, send_file
import qrcode
import pandas as pd
import os

app = Flask(__name__)

# Ruta para la página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Si se envía una URL a través del formulario
        if 'url' in request.form and request.form['url']:
            url = request.form['url']
            qr_image = generate_qr(url)
            return send_file(qr_image, as_attachment=True)

        # Si se envía un archivo Excel
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.xlsx'):
                qr_images = process_excel(file)
                return render_template('download.html', images=qr_images)

    return render_template('index.html')

# Generar código QR a partir de una URL
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=25, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    qr_path = os.path.join('static/qr_codes', 'QR.png')
    img.save(qr_path)
    return qr_path

# Procesar archivo Excel y generar QR para cada URL
def process_excel(file):
    df = pd.read_excel(file)
    qr_images = []
    for index, row in df.iterrows():
        url = row['URL']  # Asegúrate de que la columna de URLs se llama 'URL'
        qr_path = os.path.join('static/qr_codes', f'QR_{index}.png')
        qr = qrcode.QRCode(version=1, box_size=25, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(qr_path)
        qr_images.append(f'QR_{index}.png')
    return qr_images

if __name__ == '__main__':
    if not os.path.exists('static/qr_codes'):
        os.makedirs('static/qr_codes')
    app.run(debug=True)
