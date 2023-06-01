from flask import Flask, render_template, request
from Summarization import summarizer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET','POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        lang = request.form['lang']
        targ = request.form['targ']
        percent = request.form['percent']
        translated_text = summarizer(rawtext,lang,targ,percent)
    return render_template('summarizer.html',translated_text=translated_text)    

if __name__ == '__main__':
    app.run(debug=True)