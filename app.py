from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load all the environment variables from .env file

app = Flask(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               FOOD ITEMS AND CALORIES:

                1. Item 1 - XXX calories

                TOTAL CALORIES:
                Your total caloric intake from this meal is XXX calories.

                NUTRITIONAL ANALYSIS:
                Based on my assessment, this meal contains the following ratios of macronutrients:

                - Carbohydrates: XX%
                - Protein: XX%
                - Fat: XX%
                - Sugar: XX%

                RECOMMENDATION:
                [Your food is healthy/Your food is not healthy] because [detailed explanation of why it is or is not healthy].
                I would recommend [specific suggestions to improve meal healthiness] to help optimize your nutritional intake.
"""

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file, img_file_buffer):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        image_parts = [
            {
                "mime_type": uploaded_file.mimetype,
                "data": bytes_data
            }
        ]
        return image_parts
    elif img_file_buffer is not None:
        bytes_data = img_file_buffer.read()
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    upload_option = request.form.get("upload_option")
    uploaded_file = request.files["file"] if upload_option == "Upload Photo" else None
    img_file_buffer = request.files["file"] if upload_option == "Take a Picture" else None

    if uploaded_file is None and img_file_buffer is None:
        return "<p>Please upload an image or capture your meal first.</p>"
    else:
        image_data = input_image_setup(uploaded_file, img_file_buffer)
        response = get_gemini_response(input_prompt, image_data, "")
        return response

if __name__ == "__main__":
    app.run(debug=True)
