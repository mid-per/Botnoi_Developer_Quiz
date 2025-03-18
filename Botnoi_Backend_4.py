import google.generativeai as genai
from flask import Flask, request, jsonify
import os
from datetime import datetime, timedelta
import re

#had to use gemini because openai and claude wants me to pay 
#use gemini-1.5-flash-8b because Generative Language API Key

app = Flask(__name__)

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def parse_date(input_text):

    # Handle empty or invalid input
    if not input_text:
        return None, None, None
        
    # Get the current date
    today = datetime.now()
    current_date = today.strftime("%Y-%m-%d")
    
    # Use the Gemini API with a more detailed prompt
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    prompt = (
        f"Today's date is {current_date}. "
        f"Convert the following date description into 'YYYY-MM-DD' format: {input_text}"
    )
    response = model.generate_content(prompt)
    
    # Log the raw response for debugging
    print("Gemini API Response:", response.text)
    
    # Extract the date part from the response using regex
    date_match = re.findall(r"\d{4}-\d{2}-\d{2}", response.text)
    if date_match:
        date_str = date_match[-1]  
        # Use the last date in the response because gemini response like this  "Tomorrow from 2025-03-18 is 2025-03-19.""
        try:
            # Try to parse the date string into a datetime object
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.year, date_obj.month, date_obj.day
        except ValueError:
            print("Failed to parse date:", date_str)
    else:
        print("No date found in response:", response.text)
    return None, None, None

@app.route('/convert-date', methods=['POST'])
def convert_date():
    data = request.json
    if not data or 'date' not in data or not data['date']:
        return jsonify({
            "year": "-",
            "month": "-",
            "day": "-"
        }), 400
    
    input_text = data.get('date')
    year, month, day = parse_date(input_text)
    
    if year and month and day:
        return jsonify({
            "year": str(year),
            "month": str(month),
            "day": str(day)
        }), 200
    else:
        return jsonify({
            "year": "-",
            "month": "-",
            "day": "-"
        }), 400
    
if __name__ == '__main__':
    app.run(debug=True)

#tested Tomorrow, Yesterday, Next Week, Last Month, End of This Month
#tested 10/10/2024, 6 January 2022, 1 มค 2540 
#tested Invalid Date (like 12345), Empty Input, No Date Provided 
#tested 31 เดือนนี้, 6 มกราคม ปีที่แล้ว, พรุ่งนี้ 
