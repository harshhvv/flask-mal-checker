from flask import Flask, render_template, redirect, url_for, send_from_directory
from training import train_data
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

# imports for checking file using saved classifier and extracted resources
from checkdll import (
    get_resources,
    get_version_info,
    get_entropy,
    extract_infos,
    checkpe,
)


class uploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload file")


app = Flask(__name__)
app.config["SECRET_KEY"] = "root"
app.config["UPLOAD_FOLDER"] = "uploads/files"
app.config["DOWNLOAD_FOLDER"] = "downloads"


@app.route("/", methods=["GET", "POST"])
def listFiles():
    files = os.listdir(app.config["DOWNLOAD_FOLDER"])
    return render_template("file_list.html", files=files)


@app.route("/download/<filename>")
def download_file(filename):
    # Call check_dll_file to check if the file is malicious
    fhandle = "downloads/" + filename
    is_malicious = checkpe(fhandle)

    # If the file is malicious, don't allow the download
    if is_malicious == 0:
        return "File is malicious and cannot be downloaded."

    # If the file is not malicious, allow the download
    return send_from_directory(
        app.config["DOWNLOAD_FOLDER"], filename, as_attachment=True
    )


@app.route("/upload", methods=["GET", "POST"])
def home():
    form = uploadFileForm()

    if form.validate_on_submit():
        file = form.file.data
        name = file.filename
        file.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                secure_filename(file.filename),
            )
        )
        fhandle = "uploads/files/" + file.filename
        ans = checkpe(fhandle)
        if ans == 0:
            res_string = "malicious"
            print(res_string)
        else:
            res_string = "not malicious"
            print(res_string)
            # print("not mal")

        return redirect(url_for("aftercheck", ans=res_string))
    # print("uploads/files/" + name)
    return render_template("index.html", form=form)


@app.route("/results/<ans>", methods=["GET", "POST"])
def aftercheck(ans):
    return ans


if __name__ == "__main__":
    app.run(debug=True, host="192.168.122.226", ssl_context="adhoc")
