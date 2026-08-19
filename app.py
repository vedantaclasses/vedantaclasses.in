from flask import Flask, render_template_string, request, redirect, url_for, make_response
import json
import os
from functools import wraps

app = Flask(__name__)

# ============================================================
# PERMANENT SINGLE-FILE STORAGE
# ============================================================

DATA_FILE = "vedanta_data.json"

DEFAULT_DATA = {
    "contact_number": "9765139831",

    "about_text": "Welcome to Vedanta Classes. We provide premium quality education to build strong foundations for future leaders.",

    "classes_text": "We provide dedicated coaching from Class 1st to Class 10th for all major educational boards.",

    "foundation_text": "Foundation Course Program: Specialized classes focusing on deep conceptual clarity, Olympiads, and competitive entrance preparation.",

    "cbse_text": "CBSE Stream: Complete NCERT curriculum coverage with continuous revision, evaluation, and weekly practice tests.",

    "ssc_text": "SSC State Board Stream: Focused training according to the latest state board patterns with special answer writing mock tests.",

    "messages": [
        {
            "sender": "Admin",
            "text": "Welcome to the Vedanta common updates group! Timetables and test alerts will be posted here daily."
        }
    ],

    "enquiries": []
}


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA.copy())

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            loaded = json.load(file)

        # Make sure old/missing keys are restored
        changed = False

        for key, value in DEFAULT_DATA.items():
            if key not in loaded:
                loaded[key] = value
                changed = True

        if changed:
            save_data(loaded)

        return loaded

    except Exception:
        save_data(DEFAULT_DATA.copy())
        return DEFAULT_DATA.copy()


def save_data(data):
    temp_file = DATA_FILE + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    os.replace(temp_file, DATA_FILE)


data_store = load_data()


# ============================================================
# MANAGEMENT PANEL PASSWORD
# ============================================================

ADMIN_PASSWORD = "vedanta#"


def admin_logged_in():
    return request.cookies.get("vedanta_admin") == "true"


def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not admin_logged_in():
            return redirect(url_for("admin_login"))
        return function(*args, **kwargs)

    return wrapper


# ============================================================
# USER SESSION
# ============================================================

def current_user():
    return request.cookies.get("user_role")


def current_username():
    return request.cookies.get("logged_username")


# ============================================================
# CSS
# ============================================================

BASE_CSS = """
:root {
    --navy-darker: #020C1B;
    --navy-dark: #0A192F;
    --navy-light: #112240;
    --navy-accent: #233554;
    --gold: #D4AF37;
    --gold-bright: #F3E5AB;
    --text-white: #E6F1FF;
    --text-gray: #8892B0;
    --green: #64FFDA;
    --red: #FF6B6B;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Arial, sans-serif;
}

body {
    background-color: var(--navy-darker);
    color: var(--text-white);
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

header {
    background-color: var(--navy-dark);
    color: var(--gold);
    padding: 25px 40px;
    border-bottom: 3px solid var(--gold);
}

.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1300px;
    margin: 0 auto;
    width: 100%;
}

.header-lhs {
    font-size: 1.1rem;
    color: var(--text-white);
    font-weight: 500;
}

.header-lhs a {
    color: var(--gold);
    text-decoration: none;
    font-weight: bold;
    font-size: 1.3rem;
    display: block;
    margin-top: 5px;
}

.header-mid {
    text-align: center;
}

.header-mid h1 {
    font-size: 3rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 800;
    text-shadow: 0 0 10px rgba(212,175,55,0.2);
}

.header-mid p {
    font-size: 1.1rem;
    color: var(--text-gray);
    font-style: italic;
    margin-top: 5px;
}

.header-rhs {
    font-size: 2.2rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--gold);
}

.nav-bar {
    background-color: var(--navy-light);
    padding: 12px 20px;
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    border-bottom: 1px solid var(--navy-accent);
}

.nav-btn,
.dropdown-btn {
    background-color: transparent;
    border: 2px solid var(--gold);
    color: var(--gold);
    padding: 10px 22px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}

.nav-btn:hover,
.dropdown-btn:hover {
    background-color: var(--gold);
    color: var(--navy-darker);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(212,175,55,0.2);
}

.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: var(--navy-light);
    min-width: 180px;
    box-shadow: 0px 8px 16px rgba(0,0,0,0.5);
    z-index: 10;
    border: 2px solid var(--gold);
    border-radius: 4px;
    margin-top: 5px;
}

.dropdown-content a {
    color: var(--gold);
    padding: 12px 16px;
    text-decoration: none;
    display: block;
    font-weight: 500;
    border-bottom: 1px solid var(--navy-accent);
}

.dropdown-content a:hover {
    background-color: var(--gold);
    color: var(--navy-darker);
}

.dropdown:hover .dropdown-content {
    display: block;
}

.main-container {
    flex: 1;
    padding: 40px 20px;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.content-card {
    background: var(--navy-dark);
    border: 1px solid var(--navy-accent);
    border-top: 5px solid var(--gold);
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    width: 100%;
    max-width: 800px;
    text-align: center;
}

.form-card {
    text-align: left;
    background: var(--navy-light);
    border: 1px solid var(--navy-accent);
    border-top: 5px solid var(--gold);
}

.hero-section {
    text-align: center;
    margin: 40px 0;
    max-width: 800px;
}

.hero-emoji {
    font-size: 6rem;
    animation: rocket-float 3.5s ease-in-out infinite;
    display: inline-block;
    margin-bottom: 20px;
    filter: drop-shadow(0 0 20px rgba(212,175,55,0.4));
}

@keyframes rocket-float {
    0% {
        transform: translateY(0px) rotate(0deg);
    }

    50% {
        transform: translateY(-25px) rotate(5deg);
    }

    100% {
        transform: translateY(0px) rotate(0deg);
    }
}

.hero-text {
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--text-white);
    line-height: 1.4;
    letter-spacing: -0.5px;
}

.hero-subtext {
    font-size: 1.2rem;
    color: var(--text-gray);
    margin-top: 15px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: var(--gold);
    font-size: 0.95rem;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 12px 15px;
    background-color: var(--navy-darker);
    border: 2px solid var(--navy-accent);
    border-radius: 4px;
    font-size: 1rem;
    color: var(--text-white);
    transition: all 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    border-color: var(--gold);
    outline: none;
    box-shadow: 0 0 10px rgba(212,175,55,0.1);
}

.submit-btn {
    background-color: var(--gold);
    color: var(--navy-darker);
    padding: 14px 30px;
    border: none;
    border-radius: 4px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
    width: 100%;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.submit-btn:hover {
    background-color: var(--text-white);
    color: var(--navy-darker);
    transform: translateY(-2px);
}

.modal {
    display: none;
    position: fixed;
    z-index: 100;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(2, 12, 27, 0.85);
    justify-content: center;
    align-items: center;
    backdrop-filter: blur(6px);
}

.modal-content {
    background-color: var(--navy-dark);
    padding: 35px;
    border-radius: 8px;
    border: 2px solid var(--gold);
    width: 100%;
    max-width: 420px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.6);
    position: relative;
    color: var(--text-white);
}

.close-modal {
    position: absolute;
    right: 20px;
    top: 15px;
    font-size: 1.8rem;
    cursor: pointer;
    color: var(--text-gray);
}

.close-modal:hover {
    color: var(--gold);
}

.chat-box {
    background: var(--navy-darker);
    border: 2px solid var(--navy-accent);
    height: 350px;
    overflow-y: auto;
    padding: 20px;
    border-radius: 6px;
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.chat-msg {
    padding: 12px 16px;
    border-radius: 8px;
    max-width: 80%;
    line-height: 1.4;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
}

.chat-msg.admin-msg {
    background: var(--navy-light);
    border-left: 5px solid var(--gold);
    align-self: flex-start;
    color: var(--gold-bright);
}

.chat-msg.user-msg {
    background: var(--navy-accent);
    align-self: flex-end;
    color: var(--text-white);
    border-right: 5px solid var(--gold);
}

.badge {
    background: #00F5D4;
    color: var(--navy-darker);
    padding: 3px 8px;
    font-size: 0.75rem;
    border-radius: 12px;
    margin-left: 8px;
    vertical-align: middle;
    font-weight: bold;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% {
        opacity: 0.6;
    }

    50% {
        opacity: 1;
    }

    100% {
        opacity: 0.6;
    }
}

.student-button {
    display: block;
    width: 100%;
    padding: 16px 20px;
    margin-bottom: 10px;
    background: var(--navy-light);
    border: 1px solid var(--navy-accent);
    border-left: 5px solid var(--gold);
    border-radius: 5px;
    color: var(--text-white);
    text-decoration: none;
    transition: 0.3s;
}

.student-button:hover {
    background: var(--navy-accent);
    transform: translateX(5px);
}

.student-button strong {
    color: var(--gold);
    font-size: 1.1rem;
}

.student-detail {
    background: var(--navy-light);
    padding: 18px;
    border-radius: 5px;
    border: 1px solid var(--navy-accent);
    margin-bottom: 12px;
}

.student-detail b {
    color: var(--gold);
}

@media(max-width: 800px) {
    header {
        padding: 20px;
    }

    .header-container {
        flex-direction: column;
        gap: 20px;
        text-align: center;
    }

    .header-mid h1 {
        font-size: 2rem;
    }

    .header-rhs {
        font-size: 1.3rem;
    }

    .main-container {
        padding: 25px 12px;
    }

    .content-card {
        padding: 25px 18px;
    }

    .hero-text {
        font-size: 1.7rem;
    }

    .hero-emoji {
        font-size: 4rem;
    }

    .nav-bar {
        gap: 8px;
    }

    .nav-btn,
    .dropdown-btn {
        padding: 8px 13px;
        font-size: 0.9rem;
    }
}
"""


# ============================================================
# BASE LAYOUT
# ============================================================

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vedanta Classes - Official Website</title>
    <style>{{ css|safe }}</style>
</head>

<body>

<header>
    <div class="header-container">

        <div class="header-lhs">
            📞 CONTACT US
            <a href="tel:{{ data.contact_number }}">
                {{ data.contact_number }}
            </a>
        </div>

        <div class="header-mid">
            <h1>Vedanta Classes</h1>
            <p>Learn today, Lead tomorrow...</p>
        </div>

        <div class="header-rhs">
            Class 1st to 10th
        </div>

    </div>
</header>


<nav class="nav-bar">

    <a href="{{ url_for('view_page', page_id='about') }}" class="nav-btn">
        About
    </a>

    <a href="{{ url_for('view_page', page_id='classes') }}" class="nav-btn">
        Classes
    </a>


    <div class="dropdown">

        <button class="dropdown-btn">
            Courses ▼
        </button>

        <div class="dropdown-content">

            <a href="{{ url_for('view_page', page_id='foundation') }}">
                Foundation
            </a>

            <a href="{{ url_for('view_page', page_id='cbse') }}">
                CBSE
            </a>

            <a href="{{ url_for('view_page', page_id='ssc') }}">
                SSC
            </a>

        </div>

    </div>


    <a href="{{ url_for('student_info') }}" class="nav-btn">
        Student Info
    </a>


    {% if session_user == 'parent' %}

        <a href="{{ url_for('parent_group') }}"
           class="nav-btn"
           style="border-color:var(--green);color:var(--green);">

            Parent Group
            <span class="badge">Live</span>

        </a>

    {% else %}

        <button onclick="openModal('parentModal')" class="nav-btn">
            Parent Login
        </button>

    {% endif %}


    {% if session_user == 'student' %}

        <a href="{{ url_for('student_report') }}"
           class="nav-btn"
           style="border-color:var(--green);color:var(--green);">

            Student Report
            <span class="badge">Live</span>

        </a>

    {% else %}

        <button onclick="openModal('studentModal')" class="nav-btn">
            Student Login
        </button>

    {% endif %}


    {% if session_user %}

        <a href="{{ url_for('logout') }}"
           class="nav-btn"
           style="border-color:var(--red);color:var(--red);margin-left:15px;">

            Logout

        </a>

    {% endif %}

</nav>


<div class="main-container">

    {{ inner_content|safe }}

</div>


<!-- PARENT LOGIN -->

<div id="parentModal" class="modal">

    <div class="modal-content">

        <span class="close-modal"
              onclick="closeModal('parentModal')">
            &times;
        </span>

        <h3 style="margin-bottom:20px;color:var(--gold);font-size:1.4rem;">
            🔐 Parent Login Panel
        </h3>

        <form action="{{ url_for('handle_login', login_type='parent') }}"
              method="POST">

            <div class="form-group">

                <label>Parent Mobile Number</label>

                <input type="text"
                       name="uid"
                       required
                       placeholder="Registered Mobile Number">

            </div>


            <div class="form-group">

                <label>Group Access Key</label>

                <input type="password"
                       name="access_key"
                       required
                       placeholder="Enter Token Secret Code">

            </div>


            <button type="submit" class="submit-btn">
                Verify & Access Group
            </button>

        </form>

    </div>

</div>


<!-- STUDENT LOGIN -->

<div id="studentModal" class="modal">

    <div class="modal-content">

        <span class="close-modal"
              onclick="closeModal('studentModal')">
            &times;
        </span>

        <h3 style="margin-bottom:20px;color:var(--gold);font-size:1.4rem;">
            🔐 Student Analytics Login
        </h3>

        <form action="{{ url_for('handle_login', login_type='student') }}"
              method="POST">

            <div class="form-group">

                <label>Student Full Name</label>

                <input type="text"
                       name="student_name"
                       required
                       placeholder="Enter Student Name">

            </div>


            <div class="form-group">

                <label>Registered Parent Mobile Number</label>

                <input type="text"
                       name="uid"
                       required
                       placeholder="Enter Parent Mobile Number">

            </div>


            <div class="form-group">

                <label>Access Key</label>

                <input type="password"
                       name="access_key"
                       required
                       placeholder="Enter Access Code">

            </div>


            <button type="submit" class="submit-btn">
                Verify & Open Reports
            </button>

        </form>

    </div>

</div>


<script>

function openModal(id) {
    document.getElementById(id).style.display = 'flex';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

window.onclick = function(e) {

    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }

};

</script>

</body>
</html>
"""


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    home_html = """
    <div class="hero-section">

        <div class="hero-emoji">
            🚀
        </div>

        <p class="hero-text">
            Welcome to Vedanta Classes.in
        </p>

        <p class="hero-subtext">
            Empowering students through high-quality standard
            learning environments to scale academic peaks.
        </p>

    </div>
    """

    return render_template_string(
        BASE_LAYOUT,
        css=BASE_CSS,
        data=data_store,
        session_user=current_user(),
        inner_content=home_html
    )


# ============================================================
# ABOUT / CLASSES / COURSES
# ============================================================

@app.route("/screen/<page_id>")
def view_page(page_id):

    readable_title = page_id.replace("_", " ").upper()

    stored_text = data_store.get(
        f"{page_id}_text",
        "Content hasn't been added yet via admin board."
    )

    page_html = f"""
    <div class="content-card">

        <h2 style="
            color:var(--gold);
            font-size:2rem;
            margin-bottom:20px;
            letter-spacing:1px;
            border-bottom:2px solid var(--navy-accent);
            padding-bottom:12px;
        ">
            {readable_title}
        </h2>

        <p style="
            font-size:1.2rem;
            line-height:1.8;
            color:var(--text-white);
            text-align:left;
        ">
            {stored_text}
        </p>

        <div style="margin-top:35px;text-align:left;">

            <a href="/"
               style="
               color:var(--gold);
               font-weight:bold;
               text-decoration:none;
               border-bottom:1px solid var(--gold);
               ">

                ← Return to Home

            </a>

        </div>

    </div>
    """

    return render_template_string(
        BASE_LAYOUT,
        css=BASE_CSS,
        data=data_store,
        session_user=current_user(),
        inner_content=page_html
    )


# ============================================================
# STUDENT INFO
# ============================================================

@app.route("/student-info", methods=["GET", "POST"])
def student_info():

    alert_box = ""

    if request.method == "POST":

        submission = {

            "id": len(data_store["enquiries"]) + 1,

            "name": request.form.get("name", "").strip(),

            "target_class":
                request.form.get("target_class", "").strip(),

            "school":
                request.form.get("school", "").strip(),

            "contact":
                request.form.get("contact", "").strip()

        }

        data_store["enquiries"].append(submission)

        save_data(data_store)

        alert_box = """
        <div style="
            background-color:var(--navy-accent);
            color:var(--green);
            padding:15px;
            border-radius:4px;
            margin-bottom:25px;
            border-left:5px solid var(--green);
            font-weight:600;
        ">

            ✔ Form submission saved permanently!

            Our admin team will review and contact you
            with your access code.

        </div>
        """


    form_html = f"""

    <div class="content-card form-card" style="max-width:600px;">

        <h2 style="
            color:var(--gold);
            text-align:center;
            font-size:1.8rem;
            margin-bottom:25px;
            border-bottom:2px solid var(--navy-accent);
            padding-bottom:10px;
        ">

            📋 STUDENT INFO REGISTRATION

        </h2>

        {alert_box}


        <form method="POST">

            <div class="form-group">

                <label>Student's Full Name</label>

                <input type="text"
                       name="name"
                       placeholder="Fill student name"
                       required>

            </div>


            <div class="form-group">

                <label>Applying for Class / Standard</label>

                <input type="text"
                       name="target_class"
                       placeholder="e.g. 9th Standard"
                       required>

            </div>


            <div class="form-group">

                <label>Current School & Board</label>

                <input type="text"
                       name="school"
                       placeholder="e.g. St. Xavier CBSE"
                       required>

            </div>


            <div class="form-group">

                <label>Parent Mobile Number (For Group Sync)</label>

                <input type="text"
                       name="contact"
                       placeholder="Enter Mobile or Contact Number"
                       required>

            </div>


            <button type="submit"
                    class="submit-btn"
                    style="margin-top:15px;">

                Save and Submit Application

            </button>

        </form>

    </div>

    """

    return render_template_string(
        BASE_LAYOUT,
        css=BASE_CSS,
        data=data_store,
        session_user=current_user(),
        inner_content=form_html
    )


# ============================================================
# LOGIN
# ============================================================

@app.route("/auth/<login_type>", methods=["POST"])
def handle_login(login_type):

    key = request.form.get("access_key", "")

    uid = request.form.get("uid", "").strip()

    if key == "co2max":

        if login_type == "parent":
            destination = url_for("parent_group")
        else:
            destination = url_for("student_report")

        response = make_response(redirect(destination))

        response.set_cookie("user_role", login_type)

        if login_type == "student":

            s_name = request.form.get(
                "student_name",
                ""
            ).strip()

            response.set_cookie(
                "logged_username",
                s_name
            )

        return response

    else:

        return """
        <script>
            alert(
                'Incorrect Verification Code! Fill Student Info registration form to obtain code.'
            );
            window.location.href='/';
        </script>
        """


# ============================================================
# LOGOUT
# ============================================================

@app.route("/clear-session")
def logout():

    response = make_response(
        redirect(url_for("home"))
    )

    response.delete_cookie("user_role")
    response.delete_cookie("logged_username")

    return response


# ============================================================
# PARENT GROUP
# ============================================================

@app.route("/parent-hub", methods=["GET", "POST"])
def parent_group():

    if current_user() != "parent":
        return redirect(url_for("home"))

    if request.method == "POST":

        msg = request.form.get(
            "parent_msg",
            ""
        ).strip()

        if msg:

            data_store["messages"].append({
                "sender": "Parent Workspace",
                "text": msg
            })

            save_data(data_store)


    chat_messages = ""

    for msg in data_store["messages"]:

        css_class = (
            "admin-msg"
            if msg["sender"] == "Admin"
            else "user-msg"
        )

        chat_messages += f"""
        <div class="chat-msg {css_class}">

            <strong>
                {msg["sender"]}:
            </strong>

            {msg["text"]}

        </div>
        """


    parent_html = f"""

    <div class="content-card"
         style="text-align:left;">

        <h2 style="
            color:var(--gold);
            border-bottom:2px solid var(--navy-accent);
            padding-bottom:8px;
            margin-bottom:5px;
        ">

            👥 Centralized Parents Communication Group

        </h2>


        <p style="
            color:var(--text-gray);
            font-size:0.95rem;
            margin-bottom:20px;
        ">

            Noticeboard broadcast channel:
            Messages sent here are global and shared instantly
            across all active parent dashboards.

        </p>


        <div class="chat-box">

            {chat_messages}

        </div>


        <form method="POST"
              style="display:flex;gap:12px;">

            <input type="text"
                   name="parent_msg"
                   placeholder="Type notification broadcast message to all users..."
                   required
                   style="
                   flex:1;
                   padding:12px;
                   background:var(--navy-darker);
                   border:2px solid var(--navy-accent);
                   color:var(--text-white);
                   border-radius:4px;
                   ">

            <button type="submit"
                    class="submit-btn"
                    style="width:auto;padding:0 35px;">

                Send

            </button>

        </form>

    </div>

    """

    return render_template_string(
        BASE_LAYOUT,
        css=BASE_CSS,
        data=data_store,
        session_user=current_user(),
        inner_content=parent_html
    )


# ============================================================
# STUDENT REPORT
# ============================================================

@app.route("/student-report-card")
def student_report():

    if current_user() != "student":
        return redirect(url_for("home"))

    s_name = (
        current_username()
        if current_username()
        else "Student"
    )

    report_html = f"""

    <div class="content-card">

        <h2 style="
            color:var(--gold);
            border-bottom:3px solid var(--navy-accent);
            padding-bottom:10px;
            margin-bottom:20px;
        ">

            📊 PERFORMANCE REPORT CARD:
            {s_name.upper()}

        </h2>


        <div style="
            padding:40px;
            color:var(--text-gray);
            background:var(--navy-light);
            border-radius:8px;
            border:2px dashed #233554;
        ">

            <p style="
                font-size:1.4rem;
                font-weight:bold;
                margin-bottom:8px;
                color:var(--text-white);
            ">

                [ Report System is Currently Empty ]

            </p>


            <p style="font-size:1rem;">

                Academic metrics feedback,
                cumulative analytics, and monthly exam reports
                for {s_name} will populate upon master admin release.

            </p>

        </div>

    </div>

    """

    return render_template_string(
        BASE_LAYOUT,
        css=BASE_CSS,
        data=data_store,
        session_user=current_user(),
        inner_content=report_html
    )


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    error = ""

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        if password == ADMIN_PASSWORD:

            response = make_response(
                redirect(url_for("admin_panel"))
            )

            response.set_cookie(
                "vedanta_admin",
                "true"
            )

            return response

        else:

            error = """
            <div style="
                background:#3a1515;
                color:#ff6b6b;
                padding:12px;
                border-radius:4px;
                margin-bottom:20px;
                border-left:5px solid #ff6b6b;
            ">

                ❌ Incorrect Management Panel Password

            </div>
            """


    login_html = f"""

    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>
            Vedanta Management Login
        </title>

        <style>
            {BASE_CSS}

            body {{
                justify-content:center;
                align-items:center;
                padding:20px;
            }}

            .admin-login {{
                width:100%;
                max-width:450px;
                background:var(--navy-dark);
                border:1px solid var(--navy-accent);
                border-top:5px solid var(--gold);
                padding:40px;
                border-radius:8px;
                box-shadow:0 20px 50px rgba(0,0,0,0.5);
            }}
        </style>

    </head>


    <body>

        <div class="admin-login">

            <h1 style="
                text-align:center;
                color:var(--gold);
                margin-bottom:10px;
            ">

                ⚙️ Management Panel

            </h1>


            <p style="
                text-align:center;
                color:var(--text-gray);
                margin-bottom:30px;
            ">

                Vedanta Classes Administration

            </p>


            {error}


            <form method="POST">

                <div class="form-group">

                    <label>
                        Management Password
                    </label>

                    <input type="password"
                           name="password"
                           required
                           autofocus
                           placeholder="Enter management password">

                </div>


                <button type="submit"
                        class="submit-btn">

                    🔐 Open Management Console

                </button>

            </form>


            <div style="
                margin-top:25px;
                text-align:center;
            ">

                <a href="/"
                   style="
                   color:var(--gold);
                   text-decoration:none;
                   ">

                    ← Back to Website

                </a>

            </div>

        </div>

    </body>

    </html>

    """

    return render_template_string(login_html)


# ============================================================
# ADMIN LOGOUT
# ============================================================

@app.route("/admin-logout")
def admin_logout():

    response = make_response(
        redirect(url_for("home"))
    )

    response.delete_cookie("vedanta_admin")

    return response


# ============================================================
# ADMIN STUDENT DETAIL
# ============================================================

@app.route("/admin/student/<int:student_id>")
@admin_required
def admin_student_detail(student_id):

    student = None

    for item in data_store["enquiries"]:

        if item.get("id") == student_id:
            student = item
            break


    if student is None:

        return redirect(
            url_for("admin_panel")
        )


    detail_html = f"""

    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>
            Student Details - Vedanta Classes
        </title>

        <style>
            {BASE_CSS}

            body {{
                padding:40px 20px;
            }}

            .detail-box {{
                width:100%;
                max-width:800px;
                margin:0 auto;
                background:var(--navy-dark);
                border:1px solid var(--navy-accent);
                border-top:5px solid var(--gold);
                padding:35px;
                border-radius:8px;
                box-shadow:0 15px 35px rgba(0,0,0,0.5);
            }}
        </style>

    </head>


    <body>

        <div class="detail-box">

            <h1 style="
                color:var(--gold);
                margin-bottom:25px;
                border-bottom:2px solid var(--navy-accent);
                padding-bottom:15px;
            ">

                👨‍🎓 Student Information

            </h1>


            <div class="student-detail">

                <b>Student Name:</b>

                <span style="margin-left:10px;">
                    {student.get("name", "")}
                </span>

            </div>


            <div class="student-detail">

                <b>Class / Standard:</b>

                <span style="margin-left:10px;">
                    {student.get("target_class", "")}
                </span>

            </div>


            <div class="student-detail">

                <b>School & Board:</b>

                <span style="margin-left:10px;">
                    {student.get("school", "")}
                </span>

            </div>


            <div class="student-detail">

                <b>Parent Mobile:</b>

                <span style="margin-left:10px;">
                    <a href="tel:{student.get("contact", "")}"
                       style="color:var(--gold);">

                        {student.get("contact", "")}

                    </a>
                </span>

            </div>


            <div class="student-detail">

                <b>Registration ID:</b>

                <span style="margin-left:10px;">
                    {student.get("id", "")}
                </span>

            </div>


            <div style="
                margin-top:30px;
                display:flex;
                gap:15px;
                flex-wrap:wrap;
            ">

                <a href="/admin"
                   class="nav-btn">

                    ← Back to Management Panel

                </a>


                <a href="/admin-logout"
                   class="nav-btn"
                   style="
                   border-color:var(--red);
                   color:var(--red);
                   ">

                    Logout

                </a>

            </div>

        </div>

    </body>

    </html>

    """

    return render_template_string(detail_html)


# ============================================================
# MANAGEMENT PANEL
# ============================================================

@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin_panel():

    if request.method == "POST":

        action_intent = request.form.get(
            "action_intent"
        )


        if action_intent == "set_contact":

            data_store["contact_number"] = request.form.get(
                "num_val",
                ""
            ).strip()

            save_data(data_store)


        elif action_intent == "set_screen":

            screen_key = request.form.get(
                "screen_key",
                ""
            )

            body_content = request.form.get(
                "body_content",
                ""
            )

            if screen_key:

                data_store[f"{screen_key}_text"] = body_content

                save_data(data_store)


        elif action_intent == "admin_broadcast":

            broadcast = request.form.get(
                "broadcast_msg",
                ""
            ).strip()

            if broadcast:

                data_store["messages"].append({
                    "sender": "Admin",
                    "text": broadcast
                })

                save_data(data_store)


        return redirect(
            url_for("admin_panel")
        )


    # ========================================================
    # STUDENT BUTTONS
    # ========================================================

    student_buttons = ""

    if data_store["enquiries"]:

        for item in data_store["enquiries"]:

            student_buttons += f"""

            <a href="{url_for(
                'admin_student_detail',
                student_id=item.get('id')
            )}"
               class="student-button">

                <strong>
                    👨‍🎓 {item.get("name", "Student")}
                </strong>

                <br>

                <span style="
                    color:var(--text-gray);
                    font-size:0.9rem;
                ">

                    Class:
                    {item.get("target_class", "Not specified")}

                    &nbsp; | &nbsp;

                    School:
                    {item.get("school", "Not specified")}

                </span>

                <br>

                <span style="
                    color:var(--gold-bright);
                    font-size:0.85rem;
                ">

                    Click to view complete information →

                </span>

            </a>

            """

    else:

        student_buttons = """

        <p style="
            text-align:center;
            color:var(--text-gray);
            padding:30px 0;
        ">

            No Student Info submissions received yet.

        </p>

        """


    # ========================================================
    # ADMIN HTML
    # ========================================================

    admin_html = f"""

    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>
            Management Panel - Vedanta Classes
        </title>

        <style>

            {BASE_CSS}

            body {{
                background:var(--navy-darker);
                padding:40px;
                color:var(--text-white);
            }}

            .bar {{
                background:var(--navy-dark);
                padding:20px 35px;
                border-radius:8px;
                display:flex;
                justify-content:space-between;
                align-items:center;
                border-bottom:4px solid var(--gold);
                margin-bottom:35px;
                box-shadow:0 4px 20px rgba(0,0,0,0.4);
            }}

            .layout-grid {{
                display:grid;
                grid-template-columns:1.1fr 0.9fr;
                gap:35px;
                max-width:1300px;
                margin:0 auto;
            }}

            .box {{
                background:var(--navy-dark);
                padding:30px;
                border-radius:8px;
                border:1px solid var(--navy-accent);
                margin-bottom:30px;
                box-shadow:0 10px 25px rgba(0,0,0,0.3);
            }}

            h2 {{
                color:var(--gold);
                border-bottom:2px solid var(--navy-accent);
                padding-bottom:10px;
                margin-top:0;
                font-size:1.4rem;
            }}

            .token {{
                background:var(--navy-accent);
                border:1px dashed var(--gold);
                padding:12px;
                border-radius:4px;
                text-align:center;
                font-weight:bold;
                font-size:1.1rem;
                color:var(--gold);
                margin-bottom:20px;
            }}

            @media(max-width:900px) {{

                body {{
                    padding:20px 10px;
                }}

                .bar {{
                    flex-direction:column;
                    gap:15px;
                    text-align:center;
                }}

                .layout-grid {{
                    grid-template-columns:1fr;
                }}

            }}

        </style>

    </head>


    <body>


        <div class="bar">

            <h1 style="
                margin:0;
                font-size:1.8rem;
                color:var(--text-white);
            ">

                ⚙️ Management Control Panel

            </h1>


            <div style="
                display:flex;
                gap:20px;
                align-items:center;
            ">

                <a href="/"
                   target="_blank"
                   style="
                   color:var(--gold);
                   font-weight:bold;
                   text-decoration:none;
                   border-bottom:1px solid var(--gold);
                   ">

                    Launch Client Site ↗

                </a>


                <a href="/admin-logout"
                   style="
                   color:var(--red);
                   font-weight:bold;
                   text-decoration:none;
                   ">

                    Logout

                </a>

            </div>

        </div>


        <div class="layout-grid">


            <!-- LEFT SIDE -->

            <div>


                <!-- CONTACT -->

                <div class="box">

                    <h2>
                        📞 Core Contact Configurations
                    </h2>


                    <form method="POST">

                        <input type="hidden"
                               name="action_intent"
                               value="set_contact">


                        <div class="form-group">

                            <label>
                                LHS Website Phone Number
                            </label>

                            <input type="text"
                                   name="num_val"
                                   value="{data_store['contact_number']}"
                                   required>

                        </div>


                        <button type="submit"
                                class="submit-btn"
                                style="width:auto;">

                            Update Gateway Contact

                        </button>

                    </form>

                </div>


                <!-- CONTENT -->

                <div class="box">

                    <h2>
                        📝 Content Dynamic Publisher
                    </h2>


                    <form method="POST">

                        <input type="hidden"
                               name="action_intent"
                               value="set_screen">


                        <div class="form-group">

                            <label>
                                Select Screen Target
                            </label>

                            <select name="screen_key">

                                <option value="about">
                                    About Screen
                                </option>

                                <option value="classes">
                                    Classes Screen
                                </option>

                                <option value="foundation">
                                    Courses -> Foundation Screen
                                </option>

                                <option value="cbse">
                                    Courses -> CBSE Screen
                                </option>

                                <option value="ssc">
                                    Courses -> SSC Screen
                                </option>

                            </select>

                        </div>


                        <div class="form-group">

                            <label>
                                Rich Text / Page Content
                            </label>

                            <textarea name="body_content"
                                      rows="4"
                                      placeholder="Enter custom text data details..."
                                      required></textarea>

                        </div>


                        <div style="margin-top:10px;">

                            <button type="submit"
                                    class="submit-btn"
                                    style="width:auto;">

                                Deploy Content Live

                            </button>

                        </div>

                    </form>

                </div>


                <!-- BROADCAST -->

                <div class="box">

                    <h2>
                        📢 Post Group Message
                    </h2>


                    <form method="POST">

                        <input type="hidden"
                               name="action_intent"
                               value="admin_broadcast">


                        <div class="form-group">

                            <label>
                                Broadcast Message Text
                            </label>

                            <textarea name="broadcast_msg"
                                      rows="3"
                                      placeholder="Type notification statement..."
                                      required></textarea>

                        </div>


                        <button type="submit"
                                class="submit-btn"
                                style="width:auto;">

                            Broadcast Message

                        </button>

                    </form>

                </div>


            </div>


            <!-- RIGHT SIDE -->

            <div>


                <!-- STUDENTS -->

                <div class="box">

                    <h2>
                        📥 Student Info Submissions
                    </h2>


                    <p style="
                        color:var(--text-gray);
                        margin-bottom:20px;
                        line-height:1.5;
                    ">

                        Every submitted Student Info form
                        is permanently saved.

                        The student's name appears below as
                        a separate button.

                        Click the student's button to see
                        complete information.

                    </p>


                    {student_buttons}

                </div>


                <!-- ACCESS CODE -->

                <div class="box">

                    <h2>
                        🔐 Student / Parent Access
                    </h2>


                    <div class="token">

                        🔑 LOGIN ACCESS CODE:
                        co2max

                    </div>


                    <p style="
                        color:var(--text-gray);
                        line-height:1.6;
                    ">

                        Management Panel Password:

                        <strong style="color:var(--gold);">
                            vedanta#
                        </strong>

                    </p>

                </div>


                <!-- PERMANENT STORAGE -->

                <div class="box">

                    <h2>
                        💾 Permanent Saving System
                    </h2>


                    <p style="
                        color:var(--text-gray);
                        line-height:1.7;
                    ">

                        All Management Panel changes and
                        Student Info submissions are stored
                        permanently in:

                    </p>


                    <div class="token"
                         style="margin-top:15px;">

                        vedanta_data.json

                    </div>


                    <p style="
                        color:var(--text-gray);
                        line-height:1.7;
                    ">

                        Restarting the Flask server will not
                        remove the saved information.

                    </p>

                </div>


            </div>


        </div>


    </body>

    </html>

    """

    return render_template_string(admin_html)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5008,
        debug=True
    )
