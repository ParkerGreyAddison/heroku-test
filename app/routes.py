from app import app
from flask import request
from flask import jsonify

@app.route('/')
@app.route('/index')
def index():
    return """
<h1>My working web app</h1>
<p>If all is right in this world, this should be accessible via a live <b>Heroku hosted url</b>.</p>
<p>The GitHub repository <i>can</i> be private.</p> 
"""

@app.route('/request', methods=['GET'])
def returnjson():
	zipcode = request.args.get('zip')
	days = request.args.get('days')
	budget = request.args.get('budget')

	return jsonify({'zipcode':zipcode, 'days':days, 'budget':budget})