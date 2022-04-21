"""Program is used to extract the text from image"""

import string
import cv2
import pytesseract


def image_to_text(image_path, path_to_tesseract):
    """converted image to text"""
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
    texts = pytesseract.image_to_string(img)
    print(texts)
    return img


def draw_boxes_on_character(img,path_to_tesseract):
    """find only characters of the image"""
    img_width = img.shape[1]
    img_height = img.shape[0]
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
    conf = r'-c tessedit_char_whitelist='+string.ascii_letters
    boxes = pytesseract.image_to_boxes(img, config =conf)
    for box in boxes.splitlines():
        box = box.split(" ")
        character = box[0]
        x = int(box[1])
        y = int(box[2])
        x2 = int(box[3])
        y2 = int(box[4])
        cv2.rectangle(img, (x, img_height - y), (x2, img_height - y2), (0, 255, 0), 1)
        cv2.putText(img, character, (x, img_height -y2), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255) , 1)
    return img


def draw_boxes_on_text(img,path_to_tesseract):
    """find only text of the image"""
    raw_data = pytesseract.image_to_data(img)
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
    for count, data in enumerate(raw_data.splitlines()):
        if count > 0:
            data = data.split()
            if len(data) == 12:
                x, y, w, h, content = int(data[6]), int(data[7]), int(data[8]), int(data[9]), data[11]
                cv2.rectangle(img, (x, y), (w+x, h+y), (0, 255, 0), 1)
                cv2.putText(img, content, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255) , 1)   
    return img


def displaying_image(img):
    """image display"""
    cv2.imshow("Output", img)
    cv2.waitKey(0)

def selection(number,img, path_to_tesseract):
    """selecting the options"""
    match number:
        case 1:
            first = draw_boxes_on_character(img, path_to_tesseract)
            displaying_image(first)
        case 2:
            second =  draw_boxes_on_text(img, path_to_tesseract)
            displaying_image(second)
        case default:
            print("selected number is out of range")


if __name__ == "__main__":
    """function to run all functions"""
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image_path = r"C:\Users\Vissamsetty Bharath\Documents\project_python\second.png"
    image_first_face = image_to_text(image_path, path_to_tesseract)
    displaying_image(image_first_face)
    print("Now you have two options")
    printing = """1. drawing boxes on character in image (1),
2. drawing boxes on text in image (2),
****************************************"""
    print(printing)
    number = int(input("Enter a number: "))
    selection(number ,image_first_face, path_to_tesseract)
