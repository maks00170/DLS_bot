import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import PIL
from io import BytesIO
import logging
logging.basicConfig(level=logging.INFO)

class ImageProcessing:
    
    def __init__(self, new_size):
        self.new_size = new_size
        self.image_size = None


    def load_img(self, path_to_img):
        max_dim = 512
        
        img = Image.open(path_to_img)
              
        img = np.array(img)

        img = tf.image.convert_image_dtype(img, dtype=tf.float32)

            
        shape = tf.cast(tf.shape(img)[:-1], tf.float32)
        long_dim = max(shape)
        scale = max_dim / long_dim

        new_shape = tf.cast(shape * scale, tf.int32)

        img = tf.image.resize(img, new_shape)
        img = img[tf.newaxis, :]

        
        return img
    
    def tensor_to_image(self, tensor):
        tensor = tensor*255
        tensor = np.array(tensor, dtype=np.uint8)
        
        if np.ndim(tensor)>3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]

        image = PIL.Image.fromarray(tensor)
        bio = BytesIO()
        bio.name = 'output.jpeg'
        image.save(bio, 'JPEG')
        bio.seek(0)
        return bio



def run(style_image, content_image):
    
    style_processing = ImageProcessing(new_size=512)
    content_processing = ImageProcessing(new_size=512)
    


    style_image = style_processing.load_img(style_image)
    content_image = content_processing.load_img(content_image)
   
   
   
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    #print(2)
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    
    output = content_processing.tensor_to_image(stylized_image)
    return output
