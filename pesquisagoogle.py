from PIL import Image

im = Image.open("screenie.png")

im1 = im.crop((100, 100, 50, 45))
im1.show()