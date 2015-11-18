from flask import render_template, Response

def init_views(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/whereyouat')
    def rekt():
        resp = Response("Doot Doot")
        resp.headers['The-Flag-:3'] = "flag{html_response_headers_hold_the_secrets_to_everything}"

        return resp
