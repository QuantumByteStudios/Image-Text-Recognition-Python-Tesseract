
# THIS IS RAW CODE NOT TO RUN!!
# LINUX CODE!!
# sudo apt install tesseract

import os

os.system("clear")

ImageFilePath = input(
    "Image File Ka Path De Without Extension (PNG he chaiye merko): ")

OutputFile = ImageFilePath+".png"

os.system(f"tesseract {OutputFile} {ImageFilePath}")

os.system("clear")
print("File Contents are: \n")
os.system(f"cat {ImageFilePath}.txt")
