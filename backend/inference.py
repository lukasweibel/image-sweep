import tensorflow as tf
import numpy as np
from io import BytesIO
from PIL import Image

def predict_class(file, model_path='models/model.keras', target_size=(192, 192), class_names=['other', 'screenshot']):
    model = tf.keras.models.load_model(model_path)
    img = Image.open(BytesIO(file.read())).convert('RGB')
    img = img.resize(target_size)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict_on_batch(img_array)
    predicted_class_index = (prediction > 0.5).astype(int)
    predicted_class = class_names[predicted_class_index[0][0]]
    print(f"Predicted class: {predicted_class}")
    return predicted_class
