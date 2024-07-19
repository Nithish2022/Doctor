from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import pdfkit
import os

app = Flask(__name__)

# Tesseract-OCR path for Windows (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

@app.route('/')
def index():
    return render_template('index.html', recognized_text='', doctor_input='', medicines=[], prescription_html='', pdf_url='')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'handwritten_image' in request.files:
        file = request.files['handwritten_image']
        filename = secure_filename(file.filename)
        image = Image.open(file)
        recognized_text = pytesseract.image_to_string(image)
        return render_template('index.html', recognized_text=recognized_text, doctor_input='', medicines=[], prescription_html='', pdf_url='')
    return 'No file uploaded'

@app.route('/submit_prescription', methods=['POST'])
def submit_prescription():
    doctor_input = request.form['doctor_input']
    medicines = [
        {
            'name': request.form.getlist('medicine_name')[i],
            'dosage': request.form.getlist('dosage')[i],
            'duration': request.form.getlist('duration')[i]
        } for i in range(len(request.form.getlist('medicine_name')))
    ]

    # Render the prescription template HTML
    rendered = render_template('prescription_template.html', doctor_input=doctor_input, medicines=medicines)

    # Save the HTML to a file
    html_filename = 'prescription.html'
    with open(html_filename, 'w') as f:
        f.write(rendered)

    # Convert HTML to PDF
    pdf_filename = 'prescription.pdf'
    options = {
        'enable-local-file-access': ''
    }
    pdfkit.from_file(html_filename, pdf_filename, configuration=config, options=options)

    # Return the rendered HTML and PDF URL
    return render_template('index.html', recognized_text='', doctor_input=doctor_input, medicines=medicines, prescription_html=rendered, pdf_url=pdf_filename)

@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    pdf_filename = request.args.get('file')
    return send_file(pdf_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

