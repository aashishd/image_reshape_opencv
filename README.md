# image_reshape_opencv
Reshape images using CV2 library

# Requirements
Open CV 3

# How to convert images ?
  1. Create an object of ImageShapeConverter class.
  2. Use parameter height, width, maintain_aspect_ratio to set default parameters
  3. Default values for params are : 
    height = 360px (desired height of the converted image)
    width = 480px (desired width of the converted image)
    maintain_aspect_ratio = True (the aspect ratio is maintained in the output ratio as the input image)
   4. After creating the object, call convert method by passing the image object ( as read by the PIL library). The returned value is           converted image
