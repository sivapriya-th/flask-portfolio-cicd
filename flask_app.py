
import os
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["DEBUG"] = True

#SQLALCHEMY_DATABASE_URI = "sqlite:////home/priya2026/mysite/comments.db"
db_password = os.environ.get("MYSQL_ROOT_PASSWORD")

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://root:{db_password}@mysql:3306/portfolio"
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

admin_password = os.environ.get("ADMIN_PASSWORD")

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username="admin").first()

    if admin is None:
        admin = User(
            username="admin",
            password_hash=generate_password_hash(admin_password)
        )
        db.session.add(admin)
        db.session.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())

    comment = Comment(content=request.form["contents"])
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    username = request.form["username"]

    user = User.query.filter_by(username=username).first()

    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/portfolio/")
def portfolio():
    return render_template("portfolio.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

