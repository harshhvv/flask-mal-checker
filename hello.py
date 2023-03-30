from flask import Flask, render_template
from training import train_data
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms import SubmitField

# import verifycheck
# import checkdll


class uploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload file")


app = Flask(__name__)
app.config["SECRET_KEY"] = "root"


@app.route("/", methods=["GET", "POST"])
def tryy():
    form = uploadFileForm()

    return render_template("index.html", form=form)  # "okok working"
    # return train_data()


if __name__ == "__main__":
    app.run(debug=True)
