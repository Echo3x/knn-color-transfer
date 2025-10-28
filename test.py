from KNN_img.knn_color_transfer import knn_color_transfer
from PIL import Image

style = Image.open("/Users/oriole/Desktop/iPaper/pythonProject/ML/img_1.png")
content = Image.open('/Users/oriole/Desktop/iPaper/pythonProject/ML/img_2.png')

knn_color_transfer(content, style)