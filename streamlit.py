import streamlit as st
import fitz
import pytesseract
from PIL import Image
import speech_recognition as sr
import pyttsx3

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pdf_file_path = r'--PDF Path--'
img_path = r'--Image Path--'

def perform_ocr(image):
    text=pytesseract.image_to_string(image)
    return text

pdf_document=fitz.open(pdf_file_path)

text_speech = pyttsx3.init()

num_pages = pdf_document.page_count

st.header('Learning Helper')

img = Image.open(img_path)
st.image(img, use_column_width=True)

r=sr.Recognizer()
mic=sr.Microphone()
while True:
    with mic as source:
        text_speech.say('Lets learn Class 12 English Today. Say the page number to read or Say 0 to read all the pages')
        text_speech.runAndWait()
        audio=r.listen(source)

        try:
            text=r.recognize_google(audio)
            print('You Said : ',text)
            text_speech.say('You Said : ',text)
            text_speech.runAndWait()

            page_num=int(text)-1


            break

        except sr.UnknownValueError:
            print("Didn't hear anything, please repeat")
            text_speech.say("Didn't hear anything, please repeat")
            text_speech.runAndWait()

        except ValueError:
            print("Please say a page number")
            text_speech.say("Please say a page number")
            text_speech.runAndWait()




def main(page_num):
   if 0 <= page_num < num_pages:
    # Get the specified page
    page=pdf_document[page_num]
    
    # Convert the PDF page to an image using PIL
    image=page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
    image_pil=Image.frombytes("RGB", [image.width, image.height], image.samples)
    
    # Perform OCR on the selected page's image
    page_text=perform_ocr(image_pil)
    
    # Print the extracted text from the selected page
    print(f"Page {page_num + 1}:\n{page_text}\n{'=' * 40}\n")

    text_speech.say(page_text)
    text_speech.runAndWait()

   elif page_num==-1:
       for page_num in range(pdf_document.page_count):
        page=pdf_document[page_num]
        # Convert the PDF page to an image using PIL
        image=page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
        image_pil=Image.frombytes("RGB", [image.width, image.height], image.samples)
    
        # Perform OCR on the current page's image
        page_text=perform_ocr(image_pil)
    
        # Print the extracted text from the current page
        print(f"Page {page_num + 1}:\n{page_text}\n{'=' * 40}\n")

        text_speech.say(page_text)
        text_speech.runAndWait()
       
   else:
    print("Invalid page number.")

    text_speech.say('Invalid page number')
    text_speech.runAndWait()


result = ''


st.success(result)


if __name__ == "__main__":
    main(page_num)
