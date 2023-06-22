from flask import Flask
from AppFolder.appblueprint import app_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "arunisto"
app.register_blueprint(app_bp)


if __name__ == "__main__":
    app.run(debug=True)

