
import numpy
import cv2
from PIL import Image
from pdf2image import convert_from_path

class Inverter:
    def __init__(self, filename):
        self.filename = filename
    
    def invert_pdf(self) -> None:
        images = convert_from_path(self.filename)
        inverted_images = []
        for image in images:
            # convert to np array:
            image = numpy.array(image)
            
            # Resize:
            image = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
            
            # Normalize:
            image = cv2.normalize(image, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX) 
            
            # Gray:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Denoise:
            image = cv2.bilateralFilter(src=image, d=5, sigmaColor=55, sigmaSpace=60)
            
            # Binarize and invert:
            ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Convert to pdf:
            image = Image.fromarray(image)
            inverted_images.append(image)
        
        # Save first image and append rest:
        inverted_images[0].save(f"inverted_{self.filename}", save_all=True, append_images=inverted_images[1:])
              
def main(): 
    Inverter('Lab13.pdf').invert_pdf()
main()
