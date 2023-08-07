from flask import Flask, render_template, request
from mydeck import create_presentation

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/select_slides', methods=['POST'])
def select_slides():
    selected_slide_ids = []
    for slide_key in ['slide1', 'slide2', 'slide3', 'slide4']:
        slide_id = request.form.get(slide_key)
        if slide_id:
            selected_slide_ids.append(slide_id)
            
    new_presentation_url = create_presentation(selected_slide_ids)

    return render_template('result.html', url=new_presentation_url)

if __name__ == '__main__':
    app.run(debug=True)
