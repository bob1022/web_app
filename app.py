from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/travel_time", methods=["GET", "POST"])
def travel_time():
    destination = None
    time = None
    hours = None
    days = None
    years = None
    error = None

    if request.method == "POST":
        try:
            destination = request.form["destination"]
            speed = float(request.form["speed"])
            distance = float(request.form["distance"].replace(",", ""))
            unit = request.form["unit"]

            # Convert all distance to kilometers
            if unit == "au":
                distance *= 149597870.7
            elif unit == "ly":
                distance *= 9.4607e12
            if speed <= 0:
                error = "Speed must be greater than zero."
            elif distance < 0:
                error = "Distance cannot be negative."
            else:
                time_seconds = distance / speed

                time = round(time_seconds, 2)
                hours = round(time_seconds / 3600, 2)
                days = f"{time_seconds / 86400:,.2f}"
                years = f"{time_seconds / 31557600:,.2f}"

        except ValueError:
            error = "Please enter a valid distance."

    return render_template(
        "travel_time.html",
        destination=destination,
        time=time,
        days=days,
        years=years,
        error=error
    )

@app.route("/au_to_ly", methods=["GET", "POST"])
def au_to_ly():
    ly = None
    error = None

    if request.method == "POST":
        try:
            au = float(request.form["au"].replace(",", ""))

            if au < 0:
                error = "AU cannot be negative."
            else:
                ly_value = au * 1.58125e-5
                ly = f"{ly_value:,.6f}"

        except ValueError:
            error = "Please enter a valid numeric AU value."

    return render_template("au_to_ly.html", ly=ly, error=error)

@app.route("/ly_to_au", methods=["GET", "POST"])
def ly_to_au():
    au = None
    error = None

    if request.method == "POST":
        try:
            ly = float(request.form["ly"].replace(",", ""))

            if ly < 0:
                error = "Light-Years cannot be negative."
            else:
                au_value = ly * 63241
                au = f"{au_value:,.2f}"

        except ValueError:
            error = "Please enter a valid numeric LY value."

    return render_template("ly_to_au.html", au=au, error=error)


@app.route("/stellarium")
def stellarium():
    return redirect("https://stellarium-web.org/")


if __name__ == "__main__":
    app.run(debug=True)
