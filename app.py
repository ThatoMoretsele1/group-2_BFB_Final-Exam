from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ============================================================
# HELPER FUNCTION TO GET ALL LOCATIONS
# ============================================================
def get_locations():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT location_name FROM routes_locations")
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]

# ============================================================
# MAIN PAGE
# ============================================================
@app.route('/')
def main():
    locations = get_locations()
    return render_template('main.html', locations=locations)

# ============================================================
# ROLE SELECTION PAGE
# ============================================================
@app.route('/signup')
def role_selection():
    return render_template('roleSelection.html')

# ============================================================
# COMMUTER SIGNUP PAGE
# ============================================================
@app.route('/commuter-signup')
def commuter_signup():
    return render_template('signup.html')

# ============================================================
# DRIVER SIGNUP (GET)
# ============================================================
@app.route('/driver-signup')
def driver_signup_get():
    return render_template('driverSignup.html')

# ============================================================
# DRIVER SIGNUP (POST)
# ============================================================
@app.route('/driver_signup', methods=['GET', 'POST'])
def driver_signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        license_plate = request.form['license_plate']
        vehicle_color = request.form['vehicle_color']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match!"

        try:
            with sqlite3.connect('database.db', timeout=10) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM Driver_reg WHERE number_plate = ?",
                    (license_plate,)
                )

                if cursor.fetchone():
                    return "This license plate is already registered!"

                cursor.execute("""
                    INSERT INTO Driver_reg
                    (full_name, Last_name, number_plate, Vehicle_color, phone, password, Comfirm_password)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    first_name, last_name, license_plate,
                    vehicle_color, phone, password, confirm_password
                ))

                conn.commit()

            # Render trip creation page after signup
            return render_template('create.html', locations=get_locations())

        except sqlite3.OperationalError as e:
            return f"Database is busy, try again. Error: {e}"

    return render_template('driverSignup.html')

# ============================================================
# DRIVER TRIP CREATION PAGE (5 DROP-OFFS)
# ============================================================
@app.route('/driver-registration', methods=['GET', 'POST'])
def driver_registration():
    locations = get_locations()

    if request.method == 'POST':
        dropoffs = [request.form.get(f'dropoff{i}') for i in range(1, 6)]
        times = [request.form.get(f'time{i}') for i in range(1, 6)]

        # For simplicity, assume driver_id = 1 (replace with actual logged-in driver ID)
        driver_id = 1

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        for i in range(5):
            if dropoffs[i] and times[i]:
                cursor.execute("""
                    INSERT INTO dropoff_location (
                        driver_id,
                        location_name, 
                        dropoff_time
                    ) VALUES (?, ?, ?)
                """, (driver_id, dropoffs[i], times[i]))
        conn.commit()
        conn.close()

        return render_template("main.html")  # Render main page after creating trip

    return render_template('create.html', locations=locations)

# ============================================================
# CHECK AVAILABILITY
# ============================================================
@app.route("/check_availability", methods=["POST"])
def check_availability():
    pickup = request.form['pickup']
    dropoff = request.form['dropoff']
    date = request.form['date']
    time = request.form['time']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch all driver dropoffs matching pickup or dropoff
    cursor.execute("""
        SELECT dl.driver_id, dr.full_name, dr.number_plate, dr.Vehicle_color, dl.location_name, dl.dropoff_time
        FROM dropoff_location dl
        JOIN Driver_reg dr ON dl.driver_id = dr.driver_id
        WHERE dl.location_name=? OR dl.location_name=?
    """, (pickup, dropoff))
    
    rows = cursor.fetchall()
    matches = []

    # Process rows to find possible routes
    driver_routes = {}
    for row in rows:
        driver_id, full_name, plate, color, loc, dropoff_time = row
        if driver_id not in driver_routes:
            driver_routes[driver_id] = {'driver_name': full_name, 'vehicle': f"{color} - {plate}", 'locations': {}}
        driver_routes[driver_id]['locations'][loc] = dropoff_time

    # Check if driver has both pickup and dropoff
    for driver_id, info in driver_routes.items():
        if pickup in info['locations'] and dropoff in info['locations']:
            driver_pickup_time = info['locations'][pickup]
            driver_dropoff_time = info['locations'][dropoff]
            requested_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            driver_dt = datetime.strptime(f"{date} {driver_dropoff_time}", "%Y-%m-%d %H:%M")
            status = "Exact Match" if requested_dt <= driver_dt else "Next Available"
            matches.append({
                'driver_name': info['driver_name'],
                'vehicle': info['vehicle'],
                'pickup': pickup,
                'dropoff': dropoff,
                'date': date,
                'time': driver_dropoff_time,
                'status': status
            })

    conn.close()
    return render_template("track.html", matches=matches)

# ============================================================
# OTHER ROUTES (KEEPING YOUR ORIGINAL FLOW)
# ============================================================
@app.route("/track_transport", methods=["POST"])
def track_transport():
    return render_template("track.html")

@app.route("/book", methods=["POST"])
def book():
    # Example: insert booking
    driver_name = request.form['driver_name']
    pickup = request.form['pickup']
    dropoff = request.form['dropoff']
    date = request.form['date']
    time = request.form['time']
    user_id = 1  # Placeholder for logged-in user

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (user_id, pickup_location, dropoff_location, pickup_time)
        VALUES (?, ?, ?, ?)
    """, (user_id, pickup, dropoff, f"{date} {time}"))
    conn.commit()
    conn.close()

    return render_template("track.html", matches=[])

@app.route("/customer_view", methods=["POST"])
def customer_view():
    return render_template("passenger.html")

@app.route('/login')
def login():
    return render_template('Login.html')

# ============================================================
# RUN APP
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)
