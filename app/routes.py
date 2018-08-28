from app import app

@app.route('/')
@app.route('/index')
def index():
    return """
<h1>My working web app</h1>
<p>If all is right in this world, this should be accessible via a live <b>Heroku hosted url</b>.</p>
"""
