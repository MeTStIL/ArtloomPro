
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
@app.route('/')
# @login_required
def index():
    return render_template("index.html")

@app.route('/artist_pages/<int:artist_page_id>')
def artist_page(artist_page_id):
    return render_template("artist-page.html")


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()