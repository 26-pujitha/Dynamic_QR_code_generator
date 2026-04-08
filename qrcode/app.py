from flask import Flask, request, render_template_string
import qrcode
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>QR Generator</title>
</head>
<body style="text-align:center; font-family:Arial; background:#f4f4f4; padding-top:50px;">

<div style="background:white; padding:20px; display:inline-block; border-radius:10px;">
    <h2>Dynamic QR Code Generator</h2>

    <form method="POST">
        <input type="text" name="url" placeholder="Enter URL" required style="padding:10px; width:250px;">
        <br><br>
        <button type="submit" style="padding:10px; background:blue; color:white; border:none;">Generate</button>
    </form>

    {% if qr_code %}
        <h3>Your QR Code:</h3>
        <img src="data:image/png;base64,{{ qr_code }}">
        <br><br>
        <a href="data:image/png;base64,{{ qr_code }}" download="qr.png">Download QR</a>
    {% endif %}
</div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code = None

    if request.method == 'POST':
        url = request.form.get('url')

        if url:
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img = img.convert("RGB")

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            qr_code = base64.b64encode(buffer.getvalue()).decode()

    return render_template_string(HTML, qr_code=qr_code)


if __name__ == "__main__":
    app.run(debug=True)