from flask import request, session

def handle_dark_mode():
    if "dark_mode" not in session:
        session["dark_mode"] = False
    if request.method == "POST":
        session["dark_mode"] = not session["dark_mode"]
