from app import app
from flask import request
from flask import jsonify
from app.test import func

@app.route('/')
@app.route('/index')
def index():
    return """
<h1>My working web app</h1>
<p>If all is right in this world, this should be accessible via a live <b>Heroku hosted url</b>.</p>
<p>The GitHub repository <i>can</i> be private.</p>

<form id="form">
<input name="zipcode">
<input name="timeframe">
<input name="budget">
<input type="button" onclick=requestFromHeroku()>
</form>

<div id="results"></div>

<script>

            function goToRequest() {

                console.log("Should be requesting any minute now...");

                const xhr = new XMLHttpRequest();

                console.log(xhr);

                const url = 'http://localhost:5000/request?';
    
                console.log(url);

                const form = document.getElementById("form");
                const zipcode = form.elements["zipcode"];
                const timeframe = form.elements["timeframe"];
                const budget = form.elements["budget"];
                const endpoint = `${url}zipcode=${zipcode.value}&timeframe=${timeframe.value}&budget=${budget.value}`;
                
                console.log(endpoint);
                
                xhr.open("GET", endpoint);

                console.log("Opened");

                xhr.send();

                console.log("But I'm still gonna send it!");

                xhr.onreadystatechange = (e) => {
                    console.log(xhr.responseText);
                    console.log(zipcode.value);
                    console.log(timeframe.value);
                    console.log(budget.value);
                }
            };

            function requestFromHeroku() {
            const xhr = new XMLHttpRequest();
            const url = "/request?";
            
            const form = document.getElementById("form");
            const zipcode = form.elements["zipcode"];
            const timeframe = form.elements["timeframe"];
            const budget = form.elements["budget"];
            const endpoint = `${url}zipcode=${zipcode.value}&timeframe=${timeframe.value}&budget=${budget.value}`;
            
            xhr.responseType = "json";

            xhr.open("GET", endpoint);
            xhr.send();

            xhr.onreadystatechange = () => {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    console.log(xhr.response);
                    renderResults(xhr.response);
                }
            };
        };
        function renderResults(res) {
            if(!res) {
                console.log(res.status);
            }
            const zipcode = res["zipcode"];
            const timeframe = res["timeframe"];
            const budget = res["budget"];
            document.getElementById("results").innerHTML = `
                <h3>Here's what we've come up with</h3>
                <p>For the store near <i>${zipcode}</i>, you can stock up for <i>${timeframe} days</i> with a budget of <i>$${budget}!</i></p>
            `
        };

</script>
"""

@app.route('/request', methods=['GET'])
def returnjson():
    zipcode = request.args.get('zipcode')
    timeframe = request.args.get('timeframe')
    budget = request.args.get('budget')

    return jsonify({'zipcode':zipcode, 'timeframe':timeframe, 'budget':budget})

@app.route('/script', methods=['GET'])
def runscript():
    zipcode = request.args.get('zipcode')
    timeframe = request.args.get('timeframe')
    budget = request.args.get('budget')

    return func(zipcode, timeframe, budget)