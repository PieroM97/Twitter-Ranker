from flask import Blueprint,render_template,request
import app.main.service.sentiment_service as sentiment



Controller_blueprint = Blueprint("QAController_blueprint", __name__)

@Controller_blueprint.route("/")
def index():
    return render_template('index.html')

@Controller_blueprint.post("/")
def getResult():
    username = request.form['username-text']
    result = sentiment.get_user_score(username, 20, "hugging")
    return render_template("result.html", result=result)


@Controller_blueprint.app_errorhandler(500)
def error():
    return render_template("error.html"),500

@Controller_blueprint.app_errorhandler(404)
def not_found(error):
    return render_template("error.html"),404

