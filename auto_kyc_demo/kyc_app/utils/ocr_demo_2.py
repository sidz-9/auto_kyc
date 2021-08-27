import json
import pytesseract
import cv2
from PIL import Image
import ftfy
# from numpy import unicode_

import pan_read
'''module which we made to read the text of the document'''
import aadhaar_read
import io


# Defining main function
def main():
    print("hey there")

    # img = cv2.imread("image.jpg")
    # aadhar_image_demo_2.jpg
    img = cv2.imread("sample-pan-card-front.jpg")
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    var = cv2.Laplacian(img, cv2.CV_64F).var()
    if var < 50:
        print("Image is Too Blurry....")
        k = input('Press Enter to Exit.')
        exit(1)

    filename = "sample-pan-card-front.jpg"
    # filename = "image.jpg"
    text = pytesseract.image_to_string(Image.open(filename), lang='eng')

    text_output = open('output.txt', 'w', encoding='utf-8')
    text_output.write(text)
    text_output.close()

    file = open('output.txt', 'r', encoding='utf-8')
    text = file.read()

    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)

    if "income" in text.lower() or "tax" in text.lower() or "department" in text.lower():
        data = pan_read.pan_read_data(text)
    elif "male" in text.lower():
        data = aadhaar_read.adhaar_read_data(text)

    try:
        to_unicode = unicode
    except NameError:
        to_unicode = str
    with io.open('info.json', 'w', encoding='utf-8') as outfile:
        data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(data))

    with open('info.json', encoding='utf-8') as data:
        data_loaded = json.load(data)

    if data_loaded['ID Type'] == 'PAN':
        print("\n---------- PAN Details ----------")
        print("\nPAN Number: ", data_loaded['PAN'])
        print("\nName: ", data_loaded['Name'])
        print("\nFather's Name: ", data_loaded['Father Name'])
        print("\nDate Of Birth: ", data_loaded['Date of Birth'])
        print("\n---------------------------------")
    elif data_loaded['ID Type'] == 'Adhaar':
        print("\n---------- ADHAAR Details ----------")
        print("\nADHAAR Number: ", data_loaded['Adhaar Number'])
        print("\nName: ", data_loaded['Name'])
        print("\nDate Of Birth: ", data_loaded['Date of Birth'])
        print("\nSex: ", data_loaded['Sex'])
        print("\n------------------------------------")
    k = input("\n\nPress Enter To EXIT")
    exit(0)

# Using the special variable
# __name__
if __name__ == "__main__":
    main()