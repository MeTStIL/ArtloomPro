
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
@app.route('/')
# @login_required
def index():
    return render_template("index.html")

@app.route('/<string:login>')
def artist_page(login):
    return render_template("artist-page.html")

@app.route('/editor/<string:login>')
def artist_page_editor(login):
    return render_template("artist-page-editor.html")

@app.route('/accounts/<string:login>')
def account_page(login):
    return render_template("account-page.html")

@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()