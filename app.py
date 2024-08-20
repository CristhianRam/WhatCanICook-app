from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')
words = {"Hello", "World", "I'm Here"}

@app.route("/")
def render_index_page():
    """Function to render the html file."""
    return render_template('index.html', words=words)

if __name__ == '__main__':
    app.run(debug=True)