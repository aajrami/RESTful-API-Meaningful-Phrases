## @uthor Ahmed Alajrami
##

from flask import Flask, request, render_template
from flask_restful import reqparse, Api,abort, Resource
from model import Model


app = Flask(__name__)
api = Api(app)
m = Model()

parser = reqparse.RequestParser()
parser.add_argument('text')

class PostText(Resource):

    def post(self):
        args = parser.parse_args()
        # check that the posted text is 500 characters or less
        if len(args['text']) > 500:
            abort(400, message="Text is larger than 500 characters!")
        else:
            #build the model
            Model.buildModel(self)
            #process the text and extract the meaningful phrases
            phrases = Model.postedText(self, args['text'])
            return phrases, 201

##
## setup the API resource routing
##
api.add_resource(PostText, '/posttext')
@app.route('/')
def main_form():
    return '<div style="text-align:center;"><form action="submit" id="textform" method="post"><textarea name="text" rows="8" cols="50">Enter Text here...</textarea><br><input type="submit" value="Submit"></form></div>'

@app.route('/submit', methods=['POST'])
def submit_textarea():
    if len(request.form["text"]) > 500:
        return "Error! Text is larger than 500 characters!"
    else:
        # build the model
        m.buildModel()
        # process the text and extract the meaningful phrases
        phrases = m.postedText(request.form["text"])
        if len(phrases) == 0:
            return "No meaningful phrases found!"
        else:
            return render_template('phrases.html', phrases=phrases)

if __name__ == '__main__':
    app.run(debug=True)