import torch
from PIL import Image

@app.route('/process-image', methods=['POST'])
def process_image():
    image_data = request.json['image']
    # Convert the Data URI to a PIL Image
    img = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))
    # Convert the PIL Image to a PyTorch Tensor
    img_tensor = transforms.ToTensor()(img).unsqueeze(0)
    # Pass the tensor through your model
    output = model(img_tensor)
    # Get the prediction from the output
    prediction = output.argmax()
    # Save the image data to a SQLite database
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute("INSERT INTO images (data) VALUES (?)", (image_data,))
    conn.commit()
    conn.close()
    # Return the prediction to the client
    return jsonify(success=True, prediction=prediction)
