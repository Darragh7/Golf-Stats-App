from flask import Flask, render_template, request, redirect, url_for, g, session
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, EnterRound, ViewHistory, Leaderboard,ViewStats, DeleteRounds , UpdateRounds
from functools import wraps
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt  
import numpy as np


app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "secret-key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.before_request
def logged_in_user():
    g.user = session.get("user_id", None)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        message = "Account created successfully!"
        db = get_db()
        possible_clashing_user = db.execute("""
                                            SELECT *
                                            FROM users
                                            WHERE user_id = ?;
                                            """,
                                            (user_id,)).fetchone()
        if possible_clashing_user is not None:
            form.user_id.errors.append(
                "User id already taken , choose another!")
        else:
            db.execute("""
                        INSERT INTO users (user_id, password)
                        VALUES (?,?);
                        """,
                        (user_id, generate_password_hash(password))
                       )
            db.commit()
            return redirect(url_for('login') + '?message=' + message)
    return render_template("register.html",
                               form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    message = request.args.get("message")
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        possible_clashing_user = db.execute("""
                                            SELECT *
                                            FROM users
                                            WHERE user_id = ?;
                                            """,
                                            (user_id,)).fetchone()
        if possible_clashing_user is None:
            form.user_id.errors.append("User does not exist!")
        elif not check_password_hash(possible_clashing_user["password"], password):
            form.password.errors.append("Incorrect Password!")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html",
                           form=form,
                           message=message)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/enter_round", methods=["GET", "POST"])
@login_required
def enterRound():
    form = EnterRound()
    user_id = g.user
    score = form.score.data
    courseRate_dict = {
        'Blarney': 71,
        'Lee Valley': 70,
        'Cork': 72,
        'Kinsale': 70,
        'Douglas': 71,
        'Mahon': 70,
        'Muskerry': 71,
        'Monkestown': 71,
        'Raffeen Creek': 68,
        'Fota Island Resort': 71
    }
    slope_dict = {
        'Blarney': 100,
        'Lee Valley': 99,
        'Cork': 109,
        'Kinsale': 95,
        'Douglas': 97,
        'Mahon': 95,
        'Muskerry': 102,
        'Monkestown': 94,
        'Raffeen Creek': 90,
        'Fota Island Resort': 93
    }
    if form.validate_on_submit():
        db = get_db()
        name = form.name.data
        course_rating = courseRate_dict.get(name, "")
        slope_rating = slope_dict.get(name, "")
        date = form.date.data
        if course_rating and slope_rating:
            handicap = round(
                ((score - course_rating) * (113.0 / slope_rating)), 1)
            db.execute("""
                        INSERT INTO rounds (user_id, date, name, score, handicap)
                        VALUES (?, ?, ?, ?, ?);
                        """, (user_id, date, name, score, handicap)
                        )
            db.commit()

        else:
            handicap = ""
    else:
        handicap = ""
    if form.validate_on_submit():
        puts_per_round = form.puttStat1.data
        one_putt_percent = form.puttStat2.data
        three_putt_avoid = form.puttStat3.data
        avg_putt_dist = form.puttStat4.data
        date = form.date.data
        db = get_db()
        db.execute("""
                INSERT INTO putting_stats (user_id, date, puts_per_round, one_putt_percent, three_putt_avoid, avg_putt_dist)
                VALUES (?, ?, ?, ?, ?, ?);
                """, (user_id, date, puts_per_round, one_putt_percent, three_putt_avoid, avg_putt_dist)
                )
        db.commit()
    return render_template('enterRound.html',
                           handicap=handicap,
                           form=form)


@app.route("/stats", methods=["GET", "POST"])
@login_required
def stats():
    form = ViewStats()
    plot_filename = None  
    puts_per_round_avg = 0
    one_putt_percent_avg = 0
    three_putt_avoid_avg = 0
    avg_putt_dist_avg = 0 
    if form.validate_on_submit():
        start_date = form.start_date_one.data
        end_date = form.start_date_one.data
        db = get_db()
        stats = db.execute("""
                        SELECT puts_per_round, one_putt_percent, three_putt_avoid, avg_putt_dist
                        FROM putting_stats
                        WHERE date BETWEEN ? AND ?;
                        """, (start_date, end_date)
                        ).fetchall()
        db.commit()
        if stats :
            processed_putts_per_round = [row["puts_per_round"] for row in stats]
            processed_one_putt_percent = [row["one_putt_percent"] for row in stats]
            processed_three_putt_avoid = [row["three_putt_avoid"] for row in stats]
            processed_avg_putt_dist = [row["avg_putt_dist"] for row in stats]
            puts_per_round_avg = np.mean(processed_putts_per_round)
            one_putt_percent_avg = np.mean(processed_one_putt_percent)
            three_putt_avoid_avg = np.mean(processed_three_putt_avoid)
            avg_putt_dist_avg = np.mean(processed_avg_putt_dist)
            
        else:
            puts_per_round_avg = 50
            one_putt_percent_avg = 50
            three_putt_avoid_avg = 97
            avg_putt_dist_avg = 50
  
    # Reference to Youtube tutorial on webpage
    categories = ['Putts Per Round', 'One Putt Percentage', 'Three Putt Avoidance', 'Average Distance of Putts Made']
    MavStats = [28, 46, 97, 77] 
    userStats = [puts_per_round_avg, one_putt_percent_avg, three_putt_avoid_avg, avg_putt_dist_avg]

    label_placement = np.linspace(start=0, stop=2 * np.pi, num=len(MavStats) + 1)
    MavStats.append(MavStats[0])  
    userStats.append(userStats[0])  

    plt.figure(figsize=(5.5, 4.125))
    plt.subplot(polar=True)
    plt.plot(label_placement, MavStats)
    plt.plot(label_placement, userStats)
    lines, labels = plt.thetagrids(np.degrees(label_placement[:-1]), labels=categories)
    plt.legend(labels=['Maverick', 'You'], loc=(0.95, 0.8))

    plot_filename = "static/plot.png"
    plt.savefig(plot_filename)
    plt.close()

    return render_template("stats.html", plot_filename=plot_filename,form=form)



@app.route("/round_history",methods=["GET","POST"])
@login_required
def roundHistory():
    form = ViewHistory()
    if form.validate_on_submit():
        db= get_db()
        user_id=g.user
        start_date=form.start_date.data
        end_date=form.end_date.data
        print("start_date:", start_date)
        print("end_date:", end_date)
        round_history = db.execute("""
                                    SELECT name, date, score, handicap
                                    FROM rounds
                                    WHERE date BETWEEN ? AND ? AND user_id = ?;
                                    """, (start_date, end_date,user_id )
                                    ).fetchall()
        print("round_history:", round_history)
        if not round_history:
            return render_template('roundHistory.html', 
                                   form=form, 
                                   error="No rounds entered during this period yet !")

        return render_template('roundHistory.html',
                                round_history=round_history,
                                form=form)
    else:
        return render_template('roundHistory.html', form=form)

@app.route("/leaderboard",methods=["GET","POST"])
@login_required
def leaderboard():
    form = Leaderboard()
    leaderboard=""
    if form.validate_on_submit():
        db= get_db()
        leaderboard = db.execute("""
                                SELECT  date, score, handicap, name
                                FROM rounds
                                WHERE name = ?
                                ORDER BY score ASC;
                                """,
                                (form.name.data,)).fetchall()
    return render_template('leaderboard.html',
                            form=form,
                            leaderboard=leaderboard)

@app.route("/delete", methods=["GET", "POST"])
@login_required
def deleteRounds():
    form = DeleteRounds()
    date = form.dateDelete.data
    db = get_db()
    print(db)
    db.execute( """
                DELETE FROM rounds
                WHERE date = ?;
                """, (date,))
    db.commit() 
    round_history = db.execute("""
                                    SELECT name, date, score, handicap
                                    FROM rounds
                                    WHERE user_id = ?;
                                    """, (g.user,)).fetchall()
    round_history = db.execute("""
                                SELECT name, date, score, handicap
                                FROM rounds
                                WHERE user_id = ?;
                                """, (g.user,)
                                ).fetchall()
    
    return render_template("delete.html",
                           round_history=round_history, 
                           form=form)

@app.route("/update", methods=["GET", "POST"])
@login_required
def updateRounds():
    form = UpdateRounds()
    date = form.dateSelect.data
    newScore = form.newScore.data
    newPuttStat1 = form.newPuttStat1.data
    newPuttStat2 = form.newPuttStat2.data
    newPuttStat3 = form.newPuttStat3.data
    newPuttStat4 = form.newPuttStat4.data
    db = get_db()
    db.execute( """
                UPDATE rounds
                SET score = ?
                WHERE date = ?;
                """, (newScore,date))
    db.commit() 
    db.execute( """
                UPDATE putting_stats
                SET puts_per_round = ? , one_putt_percent = ? , three_putt_avoid = ? , avg_putt_dist = ?
                WHERE date = ?;
                """, (newPuttStat1, newPuttStat2, newPuttStat3, newPuttStat4, date))
    db.commit()
    round_history = db.execute("""
                                    SELECT name, date, score, handicap
                                    FROM rounds
                                    WHERE user_id = ?;
                                    """, (g.user,)).fetchall()
    round_history = db.execute("""
                                SELECT name, date, score, handicap
                                FROM rounds
                                WHERE user_id = ?;
                                """, (g.user,)
                                ).fetchall()
    
    return render_template("update.html",
                           round_history=round_history, 
                           form=form)

