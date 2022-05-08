from flask import Blueprint, render_template, request
from __init__ import create_app, db
from models import User
import threading
from twilio.rest import Client
import os
import sms_service

main = Blueprint('main', __name__)
app = create_app()
db.create_all(app=create_app(), bind='__all__')
client = Client(os.environ['SID'], os.environ['TOKEN'])


@main.route("/index", methods=["GET", "POST"])
@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    status = None
    if request.method == 'POST':
        if "opt_in" in request.form:
            try:
                number = request.form.get("phone").replace(" ", "")
                print(number)
                if "+" in number:
                    city = request.form.get("city").replace(" ", "").lower()
                    user = User(number=number, city=city)
                    db.session.add(user)
                    db.session.commit()
            except Exception as e:
                print(e)
                status = "Unable to opt in. Contact @RealSoerensen on twitter."
            else:
                status = "You have been opted in!"

        elif "opt_out" in request.form:
            try:
                number = request.form.get("phone_out").replace(" ", "")
                db.session.query(User).filter_by(number=number).delete()
                db.session.commit()
            except Exception as e:
                print(e)
                status = "Unable to opt out. Contact @RealSoerensen on twitter."
            else:
                status = "You have been removed from the service"
    return render_template("home.html", status=status)

if __name__ == "__main__":
    threading.Thread(target=sms_service.scheduler,).start()
    app.run(host='0.0.0.0', port=8080, debug=False)
