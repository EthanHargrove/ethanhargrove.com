from flask import Flask, render_template, request, session, redirect, url_for
import requests
from flask_mobility import Mobility
from forms import DesktopRandomSystemForm, MobileRandomSystemForm, ContactForm
from numpy import transpose, empty, array, zeros
from rebound import OrbitPlot
from sigfig import round
from numpy.random import randint
import io
import base64
from matplotlib import pyplot as plt
from system_generation import get_star_probs, get_star_mass, generate_system
from hidden_info import secret_key, email_password, turnstile_site_key, turnstile_secret_key
from flask_mail import Mail, Message
from misc_funcs import handle_dark_mode, handle_grid_input, chess_to_numpy, squares_to_uci
import sudoku_solver
from json import dumps, loads
import chess


app = Flask(__name__, static_folder='static')
Mobility(app)
app.config["SECRET_KEY"] = secret_key
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['TESTING'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ethanhargrove99@gmail.com'
app.config['MAIL_PASSWORD'] = email_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    message_sent = False
    if "dark_mode" not in session:
        session["dark_mode"] = False
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            subject = form.subject.data
            body = form.message.data
            turnstile = request.form.get("cf-turnstile-response")
            if turnstile:
                url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
                payload = {'secret': turnstile_secret_key, 'response': turnstile, "remoteip": request.remote_addr}
                r = requests.post(url, data=payload)
                j = r.json()
                if j["success"]==True:
                    message = Message(subject, sender=app.config["MAIL_USERNAME"], recipients = [app.config["MAIL_USERNAME"]])
                    message.body = f"name: {name}\nemail: {email}\nmessage: {body}"
                    mail.send(message)
                    message_sent = True
                    form = ContactForm(formdata=None)
        else:
            session["dark_mode"] = not session["dark_mode"]
    return render_template("index.html", title="Home", dark_mode=session["dark_mode"], form=form, message_sent=message_sent, turnstile_site_key=turnstile_site_key)


@app.route("/CV", methods=["GET", "POST"])
def cv():
    handle_dark_mode()
    return render_template("CV.html", title="CV", dark_mode=session["dark_mode"])


@app.route("/projects", methods=["GET", "POST"])
def projects():
    handle_dark_mode()
    return render_template("projects.html", title="Projects", dark_mode=session["dark_mode"])


# @app.route("/transit_timing", methods=["GET", "POST"])
# def ttvs():
#     handle_dark_mode()
#     return render_template("ttvs.html", title="Transit Timing", dark_mode=session["dark_mode"])


@app.route("/ttv_explanation", methods=["GET", "POST"])
def ttv_explanation():
    handle_dark_mode()
    return render_template("ttv_explanation.html", title="Transit Timing Explained", dark_mode=session["dark_mode"])


@app.route("/random_system", methods=["GET", "POST"])
def random_system():
    POST = False
    if request.MOBILE:
        form = MobileRandomSystemForm()
    else:
        form = DesktopRandomSystemForm()
    parameters = ["Mass", "Period (days)", "Eccentricity", "Inclination (radians)",
                      "Longitude of Ascending Node (radians)", "Argument of Periapsis (radians)", "True Anomaly (radians)"]
    param_symbols = ["\(M_\odot\)", "\(P\) (days)", "\(e\)", "\(i\) (rad)", "\(\Omega\) (rad)", "\(\omega\) (rad)", r"\(\nu\) (rad)"]
    sorted_sys_param = []
    transposed_param_string = []
    fancy_pngImageB64String = ""
    slices_pngImageB64String = ""
    num_planets = 0
    if request.method == "POST":
        if form.num_planets.data:
            POST = True
            if request.MOBILE:
                num_planets = form.num_planets.data
            else:
                num_planets = form.num_planets.data
            if num_planets == 8:
                num_planets = randint(2,8)
            star_mass = form.star_mass.data
            if star_mass is None:
                brackets, star_probs = get_star_probs(1000)
                star_mass = get_star_mass(brackets=brackets, star_probs=star_probs)
            else:
                star_mass = float(star_mass)
            terr_only = form.terr_only.data
            turnstile = request.form.get("cf-turnstile-response")
            if turnstile:
                url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
                payload = {'secret': turnstile_secret_key, 'response': turnstile, "remoteip": request.remote_addr}
                r = requests.post(url, data=payload)
                j = r.json()
                if j["success"]==True:
                    sorted_sys_param, sim = generate_system(num_planets, star_mass, terr_only)
                    transposed_param = transpose(sorted_sys_param)
                    transposed_param_string = empty(transposed_param.shape, dtype="object")
                    for i, param in enumerate(transposed_param):
                        for j, value in enumerate(param):
                            if 0.0 < value < 0.01:
                                string = str(round(value, sigfigs=5, notation="sci"))
                                E_ind = string.index('E')
                                string = r"\(" + string[0:E_ind] + r"\times 10^{" +  string[E_ind+1:] +  "}\)"
                            else:
                                string = str(round(value, sigfigs=5))

                            transposed_param_string[i,j] = string

                    px = 1/plt.rcParams["figure.dpi"]

                    fancy_fig, fancy_ax = OrbitPlot(sim, unitlabel="(AU)", figsize=(400*px, 400*px), fancy=True, color=True)
                    fancy_pngImage = io.BytesIO()
                    plt.savefig(fancy_pngImage, bbox_inches="tight", backend="agg", facecolor="#E5EFEA")
                    fancy_pngImageB64String = "data:image/png;base64,"
                    fancy_pngImageB64String += base64.b64encode(fancy_pngImage.getvalue()).decode('utf8')

                    slices_fig, slices_sub1, slices_sub2, slices_sub3 = OrbitPlot(sim, slices=1.0, unitlabel="(AU)", figsize=(400*px, 400*px), color=True)
                    slices_pngImage = io.BytesIO()
                    plt.savefig(slices_pngImage, bbox_inches="tight", backend="agg", facecolor="#E5EFEA")
                    slices_pngImageB64String = "data:image/png;base64,"
                    slices_pngImageB64String += base64.b64encode(slices_pngImage.getvalue()).decode('utf8')
        else:
            handle_dark_mode()
    return render_template("random_system.html", title="Random System Generator", form=form, param_symbols=param_symbols,
    sorted_sys_param=sorted_sys_param, transposed_param=transposed_param_string, parameters=parameters, fancy_image=fancy_pngImageB64String,
    slices_image=slices_pngImageB64String, POST=POST, dark_mode=session["dark_mode"], turnstile_site_key=turnstile_site_key)


@app.route("/random_system_explanation", methods=["GET", "POST"])
def random_system_explanation():
    handle_dark_mode()
    return render_template("random_system_explanation.html", title="Random System Generator Explained", dark_mode=session["dark_mode"])

@app.route("/sudoku_solver", methods=["GET", "POST"])
def sudoku_solver_page():
    if "dark_mode" not in session:
        session["dark_mode"] = False
    if request.method == "POST":
        turnstile = request.form.get("cf-turnstile-response")
        if turnstile:
            url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
            payload = {'secret': turnstile_secret_key, 'response': turnstile, "remoteip": request.remote_addr}
            r = requests.post(url, data=payload)
            j = r.json()
            if j["success"]==True:
                try:
                    sudoku_puzzle = handle_grid_input(9,9)
                    puzzle_list = [[int(i) for i in row] for row in sudoku_puzzle]
                    puzzle_str = dumps(puzzle_list)
                    solved_puzzle = sudoku_solver.sudoku_solver(sudoku_puzzle)
                    solved_puzzle_list = [[int(i) for i in row] for row in solved_puzzle]
                    solved_puzzle_str = dumps(solved_puzzle_list)
                    return redirect( url_for( "sudoku_solved_page", unsolved_puzzle=puzzle_str, solved_puzzle=solved_puzzle_str ) )
                except:
                    handle_dark_mode()
        else:
            handle_dark_mode()

    return render_template("sudoku_solver.html", title="Sudoku Solver", dark_mode=session["dark_mode"], turnstile_site_key=turnstile_site_key)


@app.route("/sudoku_solved", methods=["GET", "POST"])
def sudoku_solved_page():
    handle_dark_mode()
    try:
        solved_puzzle = loads(request.args["solved_puzzle"])
        unsolved_puzzle = loads(request.args["unsolved_puzzle"])
        return render_template("sudoku_solved.html", title="Sudoku Solver", dark_mode=session["dark_mode"], solved_puzzle=solved_puzzle, unsolved_puzzle=unsolved_puzzle)
    except:
        return redirect( url_for( "sudoku_solver_page" ) )


@app.route("/chess", methods=["GET", "POST"])
def chess_start():
    session["chess_colour"] = None
    if "dark_mode" not in session:
        session["dark_mode"] = False
    if request.method == "POST":
        turnstile = request.form.get("cf-turnstile-response")
        if turnstile:
            url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
            payload = {'secret': turnstile_secret_key, 'response': turnstile, "remoteip": request.remote_addr}
            r = requests.post(url, data=payload)
            j = r.json()
            if j["success"]==True:
                form_type = request.form.get("form_type")
                if form_type == "chess_colour":
                    session["chess_colour"] = request.form.get("colour")
                    session["board_fen"] = chess.STARTING_FEN
                    return redirect( url_for( "chess_move" ) )
                elif form_type == "dark_mode":
                    handle_dark_mode()
        else:
            form_type = request.form.get("form_type")
            if form_type == "dark_mode":
                handle_dark_mode()

    np_board = zeros((8,8), dtype=int)

    return render_template("chess_start.html", title="Chess", dark_mode=session["dark_mode"], chess_colour=session["chess_colour"], board=np_board, turnstile_site_key=turnstile_site_key)


@app.route("/chess_move", methods=["GET", "POST"])
def chess_move():
    if "dark_mode" not in session:
        session["dark_mode"] = False
    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "dark_mode":
            handle_dark_mode()
        elif form_type == "chess_colour":
          session["chess_colour"] = request.form.get("colour")
          session["board_fen"] = chess.STARTING_FEN
          return redirect( url_for( "chess_move" ) )
        elif form_type == "chess_move":
            selected_squares = request.form.get("selected_squares").split(',')
            try:
                uci_str = squares_to_uci(selected_squares, session["chess_colour"])
                board = chess.Board(session["board_fen"])
                _ = board.push_uci(uci_str)
                session["board_fen"] = board.fen()
            except ValueError:
                pass
    board = chess.Board(session["board_fen"])
    np_board = chess_to_numpy(board, session["chess_colour"])
    return render_template("chess.html", title="Chess", dark_mode=session["dark_mode"], chess_colour=session["chess_colour"], board=np_board)


# @app.route("/chess_move", methods=["GET", "POST"])
# def chess_move():
#     if "dark_mode" not in session:
#         session["dark_mode"] = False
#     try:
#         new_game = loads(request.args["new_game"])
#         if new_game:
#             new_game = False
#             board = chess.Board()
#             np_board = chess_to_numpy(board, session["chess_colour"])
#             return render_template("chess.html", title="Chess", dark_mode=session["dark_mode"], chess_colour=session["chess_colour"], board=np_board)
#     except:
#         if request.method == "POST":
#             form_type = request.form.get("form_type")
#             print(f"form_type = {form_type}")
#             if form_type == "chess_colour":
#                 session["chess_colour"] = request.form.get("colour")
#                 return redirect( url_for( "chess_move", new_game="True" ) )
#             elif form_type == "chess_move":
#                 selected_squares = request.form.get("selected_squares").split(',')
#             elif form_type == "dark_mode":
#                 handle_dark_mode()
#     if request.method == "POST":
#         form_type = request.form.get("form_type")
#         print(f"form_type = {form_type}")
#         if form_type == "chess_colour":
#             session["chess_colour"] = request.form.get("colour")
#             return redirect( url_for( "chess_move", new_game="True" ) )
#         elif form_type == "chess_move":
#             selected_squares = request.form.get("selected_squares").split(',')
#         elif form_type == "dark_mode":
#             handle_dark_mode()
#     if 'np_board' in globals() or 'np_board' in locals():
#         return render_template("chess.html", title="Chess", dark_mode=session["dark_mode"], chess_colour=session["chess_colour"], board=np_board)
#     else:
#         np_board = array([[-3, -5, -4, -2, -1, -4, -5, -3],
#                       [-6, -6, -6, -6, -6, -6, -6, -6],
#                       [ 0,  0,  0,  0,  0,  0,  0,  0],
#                       [ 0,  0,  0,  0,  0,  0,  0,  0],
#                       [ 0,  0,  0,  0,  0,  0,  0,  0],
#                       [ 0,  0,  0,  0,  0,  0,  0,  0],
#                       [ 6,  6,  6,  6,  6,  6,  6,  6],
#                       [ 3,  5,  4,  2,  1,  4,  5,  3]], dtype=int)
#         if session["chess_colour"] == "black":
#             return render_template("chess.html", title="Chess", dark_mode=session["dark_mode"], chess_colour=session["chess_colour"], board=np_board)
#         else:
#             np_board *= -1
#             return render_template("chess.html", title="Chess", dark_mode=session["dark_mode"], chess_colour=session["chess_colour"], board=np_board)

#     return render_template("chess.html", title="Chess", dark_mode=session["dark_mode"], chess_colour=session["chess_colour"], board=np_board)

# @app.route("/chess", methods=["GET", "POST"])
# def chess():
#     print("chess")
#     if "dark_mode" not in session:
#         session["dark_mode"] = False
#     if "chess_colour" not in session:
#         session["chess_colour"] = "white"

#     if request.method == "POST":
#         print("posted")
#         try:
#             selected_squares = request.form.get("selected_squares").split(',')
#             print(f"squares = {selected_squares}")
#         except:
#             print("dark")
#             handle_dark_mode()



#     if 'board' in globals() or 'board' in locals():
#         return render_template("chess.html", title="Chess", dark_mode=session["dark_mode"], chess_colour=session["chess_colour"], board=np_board)
#     else:
#         np_board = array([[-3, -5, -4, -2, -1, -4, -5, -3],
#                       [-6, -6, -6, -6, -6, -6, -6, -6],
#                       [ 0,  0,  0,  0,  0,  0,  0,  0],
#                       [ 0,  0,  0,  0,  0,  0,  0,  0],
#                       [ 0,  0,  0,  0,  0,  0,  0,  0],
#                       [ 0,  0,  0,  0,  0,  0,  0,  0],
#                       [ 6,  6,  6,  6,  6,  6,  6,  6],
#                       [ 3,  5,  4,  2,  1,  4,  5,  3]], dtype=int)
#         if session["chess_colour"] == "black":
#             return render_template("chess.html", title="Chess", dark_mode=session["dark_mode"], chess_colour=session["chess_colour"], board=np_board)
#         else:
#             board *= -1
#             return render_template("chess.html", title="Chess", dark_mode=session["dark_mode"], chess_colour=session["chess_colour"], board=np_board)


@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    return app.send_static_file("sitemap.xml")

if __name__ == "__main__":
    app.run(debug=True)

