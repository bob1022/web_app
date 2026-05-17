
from flask import Flask, render_template, redirect, request
app = Flask(__name__)

SPACECRAFTS = {
    "Apollo 10": 11.08,
    "Voyager 1": 17.0,
    "Voyager 2": 15.4,
    "New Horizons": 16.26,
    "Parker Solar Probe": 192.0,
    "JWST": 0.6,
    "10% Speed of Light": 29979
}


def convert_to_km(distance, unit):
    if unit == "au":
        return distance * 149597870.7
    elif unit == "ly":
        return distance * 9.4607e12
    elif unit == "pc":
        return distance * 3.0857e13
    elif unit == "kpc":
        return distance * 3.0857e16
    elif unit == "mpc":
        return distance * 3.0857e19
    return distance


def format_distance(distance_km):
    au = distance_km / 149597870.7
    ly = distance_km / 9.4607e12
    pc = ly / 3.26156
    kpc = pc / 1000
    mpc = kpc / 1000

    if au < 1000:
        return f"{au:,.2f} AU"
    elif ly < 100:
        return f"{ly:,.2f} LY"
    elif pc < 1000:
        return f"{pc:,.2f} PC"
    elif kpc < 1000:
        return f"{kpc:,.2f} KPC"
    else:
        return f"{mpc:,.2f} MPC"

space_objects = {
    "Moon": {"distance": 384400, "unit": "km"},
    "Mars": {"distance": 225000000, "unit": "km"},
    "Jupiter": {"distance": 778000000, "unit": "km"},
    "Pluto": {"distance": 5900000000, "unit": "km"},
    "Alpha Centauri": {"distance": 4.37, "unit": "ly"},
    "Betelgeuse": {"distance": 642.5, "unit": "ly"},
    "Capella": {"distance": 42.9, "unit": "ly"},
    "Andromeda Galaxy": {"distance": 0.778, "unit": "mpc"}
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/travel_time", methods=["GET", "POST"])
def travel_time():
    time = None
    user_distance = None
    error = None
    destination = None
    distance = None
    distance_display = None
    days = None
    years = None
    spacecraft = None
    speed = None
    mph = None
    

    if request.method == "POST":
        try:
            destination = request.form["destination"]
            user_distance = request.form["distance"]
            distance = float(user_distance.replace(",", ""))
            unit = request.form["unit"]
            spacecraft = request.form["spacecraft"]
            speed_value = SPACECRAFTS[spacecraft]
            speed = f"{speed_value:,.0f}"
            mph = f"{speed_value * 2236.936:,.0f}"
            # mph = f"{speed * 2236.936:,.0f}"

            # Convert to kilometers
            distance_km = convert_to_km(distance, unit)

            # Time calculations
            time_seconds = distance_km / speed_value
            days_value = time_seconds / 86400
            years_value = days_value / 365

            days = f"{days_value:,.2f}"
            years = f"{years_value:,.2f}"
            distance = f"{distance_km:,.2f}"
            distance_display = format_distance(distance_km)
            spacecraft=spacecraft,
            speed=speed

        except ValueError:
            error = "Please enter valid numeric values."

    return render_template(
        "travel_time.html",
        destination=destination,
        spacecraft=spacecraft,
        speed=speed,
        mph=mph,
        distance=distance_display,
        days=days,
        years=years,
        error=error
    )


@app.route("/travel_time_db", methods=["GET", "POST"])
def travel_time_db():
    time = None
    days = None
    years = None
    error = None
    destination = None
    distance = None
    distance_display = None
    spacecraft = None
    speed = None
    mph = None

    if request.method == "POST":
        try:
            destination = request.form["destination"]

            spacecraft = request.form["spacecraft"]
            speed_value = SPACECRAFTS[spacecraft]
            speed = f"{speed_value:,.0f}"
            mph = f"{speed_value * 2236.936:,.0f}"

            selected_object = space_objects[destination]
            distance = selected_object["distance"]
            unit = selected_object["unit"]

            # Convert to kilometers
            distance_km = convert_to_km(distance, unit)

            # Time calculations
            time_seconds = distance_km / speed_value
            days_value = time_seconds / 86400
            years_value = days_value / 365

            days = f"{days_value:,.2f}"
            years = f"{years_value:,.2f}"
            distance_display = format_distance(distance_km)

        except Exception:
            error = "Please select a valid destination."

    return render_template(
        "travel_time_db.html",
        space_objects=space_objects,
        destination=destination,
        spacecraft=spacecraft,
        speed=speed,
        mph=mph,
        distance=distance_display,
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
        "mls": 1.60934,
        "au": 149597870.7,
        "ly": 9.4607e12,
        "pc": 3.0857e13,
        "kpc": 3.0857e16,
        "mpc": 3.0857e19
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

                unit_names = {
                "km": "Kilometers",
                "mls": "Miles",
                "au": "AU",
                "ly": "Light-Year",
                "pc": "Parsec",
                "kpc": "Kiloparsec",
                "mpc": "Megaparsec"
            }

            if converted_value < 1:
                 converted_text = f"{converted_value:,.6f}"
            else:
                converted_text = f"{converted_value:,.2f}"

            result = f"{value:g} {unit_names[from_unit]} = {converted_text} {unit_names[to_unit]}"

        except ValueError:
            error = "Please enter a valid numeric value."

    return render_template(
        "astro_converter.html",
        result=result,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
