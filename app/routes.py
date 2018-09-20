from app import app
from flask import request
from flask import jsonify
from app.test import func
from script import script
import threading
import time
import csv
from flask import redirect, url_for




@app.route("/a")
def a_index():
    return """
    <h1>Submit this form</h1>
    <form id="form">
    <input name="field">
    <input type="button" onclick="request()">
    </form>

    <script>

    let field;
    
    function request() {
        const xhr = new XMLHttpRequest();
        const url = "/areq?";
        console.log(url);
        field = document.getElementById("form").elements["field"].value;
        console.log(field);
        const endpoint = `${
            url}value=${
            field}`;
        xhr.responseType = "json";
        xhr.open("GET", endpoint);
        xhr.send();
        xhr.onreadystatechange = () => {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                handleResponse(xhr.response);
            }
        };
    }

    let polling;

    function handleResponse(res) {

        switch(res["status"]) {
            case "complete":
                document.body.innerHTML = `<h1>Wooo!</h1><p>Your value is <b>${res["value"]}</b>.</p>`;
                clearInterval(polling);
                break;

            case "poll":
                document.body.innerHTML = `<h1>Hold on...</h1><p>We're getting your results right now.</p>`;
                polling = window.setInterval(function() {
                    console.log("polling");
                    const xhr = new XMLHttpRequest();
                    let pollurl = "/apoll?";
                    let pollendpoint = `${
                        pollurl}value=${
                            field}`;
                    xhr.responseType = "json";
                    xhr.open("GET", pollendpoint);
                    xhr.send();
                    xhr.onreadystatechange = () => {
                        if (xhr.readyState === XMLHttpRequest.DONE) {
                            console.log(xhr.response);
                            handleResponse(xhr.response);
                        }
                    };
                }, 2000);
                break;

            case "await":
                document.body.innerHTML = `<h1>Thanks for waiting</h1><p>This will take 40 seconds.</p>`;
                break;
        }
    }

    </script>
    """

@app.route("/areq", methods=["GET"])
def areq():
    # If the value isn't in our values.csv file
        # then start a thread that will add it to the file (after sleeping)
        # and respond with instructions to start polling.
        #
        # During polling we will just check if our value is in the file yet.
        # If it is *not* then we get an "await" resonse and try again.
        # If it *is* then we send the original value again to /areq.
    value = request.args.get("value")

    if check_value_in_file(value):
        return jsonify({"status":"complete", "value":value})
    else:
        # starting separate thread to add value to file
        thread = threading.Thread(target=add_value_to_file, args=(value,))
        thread.start()

        # returning instructions to poll
        return jsonify({"status":"poll"})

def check_value_in_file(value):
    print("Checking for", value)
    with open("values.csv", 'r') as valuesfile:
        reader = csv.reader(valuesfile)
        rows = list(reader)
        values = [value for row in rows for value in row]
    return value in values

def add_value_to_file(value):
    print("Will write to file in 40 seconds")
    time.sleep(40)
    with open ("values.csv", 'w', newline='') as valuesfile:
        writer = csv.writer(valuesfile)
        writer.writerow((value,))

@app.route("/apoll", methods=["GET"])
def apoll():
    value = request.args.get("value")
    
    if check_value_in_file(value):
        return redirect("/areq?value=%s" % value)
    else:
        return jsonify({"status":"await"})

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

@app.route('/test', methods=['GET'])
def runtest():
    zipcode = request.args.get('zipcode')
    timeframe = request.args.get('timeframe')
    budget = request.args.get('budget')

    return func(zipcode, timeframe, budget)

@app.route('/script', methods=['GET'])
def runscript():
    zipcode = request.args.get('zipcode')
    timeframe = request.args.get('timeframe')
    budget = request.args.get('budget')

    return jsonify(script(zipcode, timeframe, budget))

@app.route("/slowreq", methods=["GET"])
def slowrequest():
    """
    Testing out a request that takes a long time.  This should start the process
    on a separate thread whilst returning instructions to poll for the finished
    results every couple seconds.
    """

    # VALUE = False

    def lamb():
        time.sleep(8)
        return

    # global THREAD
    THREAD = threading.Thread(target=lamb)
    THREAD.start()

    #! Alright, good to know:
        # The thread doesn't transfer over to the requests to /poll... and I
        # don't think any variable changes would.


    # Trying to define the route inside of this function to preserve variables
    @app.route("/poll")
    def poll():
        if THREAD.is_alive():
            return jsonify({"status":"await"})
        else:
            return jsonify({"status":"complete", "value":"done"})

    #! Defining within route causes error when page refreshed, doesn't allow
        # for multiple definitions of same route.

    return """
    <h1>Currently this result is saying I should poll</h1>
    <p>So, I'll have some JavaScript that makes a request to /poll every two seconds.</p>

    <script>

        let polling = window.setInterval(function() {

            console.log("polling");
            
            const xhr = new XMLHttpRequest();
            const url = "/poll";
            xhr.responseType = "json";
            xhr.open("GET", url);
            xhr.send();
            xhr.onreadystatechange = () => {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    console.log(xhr.response);
                    handleResponse(xhr.response);
                }
            };
        }, 2000);

        function handleResponse(res) {
            if(!res) {
                console.log(res.status);
            }
            
            if (res["status"] === "await") {
                console.log("still awaiting");
            } else if (res["status"] === "complete") {
                console.log("result complete");
                clearInterval(polling);
                document.body.innerHTML = `
                <h1>Wow! It's finished!</h1>
                <p>Your value is <b>${res["value"]}</b>!</p>
                `;
            }
        };

    </script>"""

# VALUE = False

# @app.route("/poll", methods=["POST"])
# def poll():
#     if request.args.get("action") == "begin":
#         global VALUE
