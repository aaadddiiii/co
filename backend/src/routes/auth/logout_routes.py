from flask import session, request, redirect

def routes(app):

    @app.route("/logout", methods=["GET", "POST"])
    def logout():

        if request.method == "POST":
            session.clear()
            return redirect("/")   # or /login

        # GET request
        return redirect("/")