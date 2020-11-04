import os
import json
# Firstly, we're importing our Flask class and built in variable os.
from flask import Flask, render_template, request, flash
if os.path.exists("env.py"):
    import env

"""
We're then creating an instance of this and storing it in a variable called app. The first argument
of the Flask class is the name of the applications module - our package. Since we're just using a single module, 
we can use __name__ Flask needs this so that it knows where to look for templates and static files.
"""
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# We're then using the app.route decorator. In Python, a decorator starts with the @ sign,is a way of wrapping functions which is also called pie notation. 
# we try to browse to the root directory as indicated by the "/", then flask triggers the index function underneath and returns the "Hello, World" text. 

@app.route("/")
def index():
    return render_template("index.html")

# I'm going to add in an additional argument in the return statement called 'page_title'.this can be called anything you want, it's not specific to the framework.
# It's just a variable name. The value for my variable will simply be a string with the text 'About'

@app.route("/about")
def about():
    data = []
    # Python is opening the JSON file as "read-only", and assigning the contents of the file to a new variable we've created called json_data.
    with open("data/company.json","r") as json_data: 
        # We need to set our empty 'data' list to equal the parsed JSON data that we've sent through.
        data = json.load(json_data)
        # company=data is assigning a new variable called 'company' that will be sent through to the HTML template called company, which is equal to the 
        # list of data it's loading from the JSON file.
    return render_template("about.html", page_title = "About", company=data)


# The angle brackets will pass in data from the URL path, into our view below, and I've called this parameter: 'member_name'.
@app.route("/about/<member_name>")
# create the view for this, which is going to be: about_member.That can now take member_name from above, as an argument.
# whenever we look at our 'about' URL with something after it, that will be passed into this view.
def about_member(member_name):
    member = {}
    with open("data/company.json", "r") as json_data:
        #We will then create another variable inside, where we pass the data that we've pulled through and converted into JSON.
        data = json.load(json_data)
        # We will iterate through that data array that we've just created I give the variable name of 'obj', which is just an abbreviation for 'object'
        for obj in data:
            # to check if that object's url key from the file, is equal to the member_name we've passed through from the URL path.
            # If they do match, then we want our empty 'member' object to be equal to the object in this loop instance.
            if obj["url"] == member_name:
                member = obj
    # This first 'member' is the variable name being passed through into our html file. The second 'member' is the member object we created above.
    return render_template("member.html", member=member)


@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we have received your message!".format(
            request.form.get("name")))
    return render_template("contact.html", page_title = "Contact")

@app.route("/careers")
def careers():
    return render_template("careers.html", page_title = "Careers")

# __name__ is the name of the default module in ptyhon
if __name__ =="__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=int(os.environ.get("PORT", "5000")),
            debug=True)


# never have debug=true in a production application or when we submit our projects for assessment.
