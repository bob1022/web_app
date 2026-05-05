
from flask import Flask, render_template, redirect, request
app = Flask(__name__)

space_objects = {
    "Moon": {"distance": 384400, "unit": "km"},
    "Mars": {"distance": 225000000, "unit": "km"},
    "Jupiter": {"distance": 778000000, "unit": "km"},
    "Pluto": {"distance": 5900000000, "unit": "km"},
    "Alpha Centauri": {"distance": 4.37, "unit": "ly"},
    "Betelgeuse": {"distance": 642.5, "unit": "ly"},
    "Capella": {"distance": 42.9, "unit": "ly"},
    "Andromeda Galaxy": {"distance": 2537000, "unit": "ly"}
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/travel_time", methods=["GET", "POST"])
def travel_time():
    time = None
    error = None
    destination = None
    days = None
    years = None

    if request.method == "POST":
        try:
            destination = request.form["destination"]
            distance = float(request.form["distance"].replace(",", ""))
            unit = request.form["unit"]
            speed = float(request.form["speed"])

            # Convert to kilometers
            if unit == "au":
                distance_km = distance * 149597870.7
            elif unit == "ly":
                distance_km = distance * 9.4607e12
            else:
                distance_km = distance

            # Time calculations
            time_seconds = distance_km / speed
            days_value = time_seconds / 86400
            years_value = days_value / 365

            days = f"{days_value:,.2f}"
            years = f"{years_value:,.2f}"

        except ValueError:
            error = "Please enter valid numeric values."

    return render_template(
        "travel_time.html",
        time=time,
        error=error,
        destination=destination,
        days=days,
        years=years
    )


@app.route("/travel_time_db", methods=["GET", "POST"])
def travel_time_db():
    time = None
    days = None
    years = None
    error = None
    destination = None

    if request.method == "POST":
        try:
            destination = request.form["destination"]
            speed = float(request.form["speed"])

            selected_object = space_objects[destination]
            distance = selected_object["distance"]
            unit = selected_object["unit"]

            # Convert to kilometers
            if unit == "au":
                distance_km = distance * 149597870.7
            elif unit == "ly":
                distance_km = distance * 9.4607e12
            else:
                distance_km = distance

            # Time calculations
            time_seconds = distance_km / speed
            days_value = time_seconds / 86400
            years_value = days_value / 365

            days = f"{days_value:,.2f}"
            years = f"{years_value:,.2f}"

        except Exception:
            error = "Please select a valid destination."

    return render_template(
        "travel_time_db.html",
        space_objects=space_objects,
        destination=destination,
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

@app.route("/astro_converter", methods=["GET", "POST"])
def astro_converter():
    result = None
    error = None

    conversion_to_km = {
        "km": 1,
        "au": 149597870.7,
        "ly": 9.4607e12
    }

    if request.method == "POST":
        try:
            value = float(request.form["value"].replace(",", ""))
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]

            if value < 0:
                error = "Value cannot be negative."
            else:
                km_value = value * conversion_to_km[from_unit]
                converted_value = km_value / conversion_to_km[to_unit]

                if converted_value < 1:
                    result = f"{converted_value:,.6f}"
                else:
                    result = f"{converted_value:,.2f}"

        except ValueError:
            error = "Please enter a valid numeric value."

    return render_template(
        "astro_converter.html",
        result=result,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
