from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import database
from functools import wraps
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret_key"  # change before submission

# simple login required decorator
def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped


@app.route("/")
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        user = database.validate_user(email, password)
        if user:
            # store minimal user info in session
            session['user'] = {'user_id': user['user_id'], 'name': user['name'], 'email': user['email']}
            flash("Logged in successfully", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        if not (name and email and password):
            flash("All fields are required", "warning")
            return render_template("register.html")
        try:
            database.create_user(name, email, password)
            flash("Registration successful — please login", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Registration failed: {e}", "danger")
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop('user', None)
    flash("Logged out", "info")
    return redirect(url_for('login'))


@app.route("/dashboard")
@login_required
def dashboard():
    """
    IMPORTANT: fetch meetings in the route (server-side),
    then pass them to the template as 'meetings'.
    This avoids calling database.* functions inside Jinja.
    """
    # fetch upcoming meetings for the logged in host
    meetings = database.get_upcoming_meetings(session['user']['user_id'])
    return render_template("dashboard.html", user=session['user'], meetings=meetings)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create_meeting():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        date = request.form.get("date", "").strip()          # expect YYYY-MM-DD
        start_time = request.form.get("start_time", "").strip()  # expect HH:MM:SS
        duration = request.form.get("duration", "").strip()
        if not (title and date and start_time and duration):
            flash("All fields required", "warning")
            return render_template("create_meeting.html")

        try:
            duration_int = int(duration)
        except ValueError:
            flash("Duration must be an integer (minutes)", "warning")
            return render_template("create_meeting.html")

        try:
            code = database.create_meeting(session['user']['user_id'], title, date, start_time, duration_int)
            flash(f"Meeting created. Code: {code}", "success")
            return redirect(url_for('view_meetings'))
        except Exception as e:
            flash(f"Could not create meeting: {e}", "danger")

    return render_template("create_meeting.html")


@app.route("/meetings")
@login_required
def view_meetings():
    rows = database.get_upcoming_meetings(session['user']['user_id'])
    return render_template("view_meetings.html", meetings=rows)


@app.route("/export_csv")
@login_required
def export_csv():
    rows = database.get_upcoming_meetings(session['user']['user_id'])
    if not rows:
        flash("No meetings to export", "warning")
        return redirect(url_for('dashboard'))

    df = pd.DataFrame(rows)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(io.BytesIO(buffer.getvalue().encode('utf-8')),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='meetings_export.csv')


@app.route("/join/<code>")
@login_required
def join_meeting(code):
    # Simple simulated join page
    return render_template("join.html", code=code, user=session['user'])


if __name__ == "__main__":
    # run locally on port 5000
    app.run(debug=True, host='127.0.0.1', port=5000)
