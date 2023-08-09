import base64
import io

import requests
from PIL import Image

output_image = Image.open("0.1105555646-18055869757.jpg")
output_image = Image.open("0.262766449-17721215256.jpg")
output_image = Image.open("0.104539030739-15000887715.jpg")
w, h = output_image.size
jpeg_image_buffer = io.StringIO()
output_image.save(jpeg_image_buffer, format="JPEG")
output_image_data = jpeg_image_buffer.getvalue()
output_image_base64 = base64.b64encode(output_image_data)
data = {
    "image": output_image_base64,
    "box": "[[0, 0, {}, 0, 0, {}, {}, {}]]".format(w, h, w, h),
}
code1 = requests.post("http://10.9.30.47:8080/ocr/v1/express_bill", data=data).text
print(code1)
