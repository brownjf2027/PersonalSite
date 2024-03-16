import datetime
from os import environ
from flask import Flask, request, render_template, redirect, url_for, flash, make_response, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Date, LargeBinary
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, FileField, TextAreaField, EmailField, DateField, HiddenField
from wtforms.validators import DataRequired, ValidationError

SALT_ROUNDS = 16


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
# Initialize Flask-Bootstrap
bootstrap = Bootstrap(app)

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    title: Mapped[str] = mapped_column(String(100))
    blurb: Mapped[str] = mapped_column(String(250))
    body: Mapped[str] = mapped_column(String(1000))


class Image(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    data = mapped_column(LargeBinary)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Snippet(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    data = mapped_column(String)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


with app.app_context():
    db.create_all()
    posts = Post.query.all()
    for post in posts:
        print(post.title)


#     # db.drop_all()
#     # users = User.query.all()


class PostForm(FlaskForm):
    post_id = HiddenField('Post ID:')
    date = DateField('Date')
    title = StringField('Title:', validators=[DataRequired()])
    blurb = TextAreaField('Blurb:', validators=[DataRequired()])
    body = TextAreaField('Body:', validators=[DataRequired()], render_kw={"style": "height: 250px;"})
    submit = SubmitField("Submit Post")


@app.route("/post", methods=['GET', 'POST'])
def post():
    post_id = request.args.get('edit_post_id')
    form = PostForm()

    if form.validate_on_submit():
        if post_id:
            # If post ID is provided, it's an update operation
            post = Post.query.get_or_404(post_id)
            post.id = post.id
            post.date = form.date.data
            post.title = form.title.data
            post.blurb = form.blurb.data
            post.body = form.body.data

            print(f"post_id = {post.id}"
                  f"post.date = {post.date}"
                  f"post.title = {post.title}"
                  f"post.blurb = {post.blurb}"
                  f"post.body = {post.body}")

            db.session.commit()
            flash('Saved!')
            return redirect(url_for('show_post', post_id=post.id))

        else:
            new_post = Post(
                date=form.date.data,
                title=form.title.data,
                blurb=form.blurb.data,
                body=form.body.data
            )
            db.session.add(new_post)
            db.session.commit()

            # snip = request.data['snip']

            # Check if the 'image_file' was included in the request
            if 'image_file' in request.files:
                file = request.files['image_file']
                # Check if a file was selected and if it has an allowed extension
                if file and allowed_file(file.filename):
                    file_data = file.read()
                    img_file = Image(name=file.filename, data=file_data, post_id=new_post.id)  # Use new_post.id
                    db.session.add(img_file)
                    db.session.commit()

            flash('Saved!')
            return redirect(url_for('post', post_id=new_post.id))  # Redirect with new_post.id

    if post_id:
        # If post ID is provided, fetch the existing post data for editing
        post = Post.query.get_or_404(post_id)
        form.post_id.data = post.id
        print(post_id)
        form.date.data = post.date
        form.title.data = post.title
        form.blurb.data = post.blurb
        form.body.data = post.body

    return render_template("add_post.html", form=form)


def allowed_file(filename):
    allowed_extensions = {'jpg', 'gif', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = Post.query.filter_by(id=post_id).first()
    # Fetch other necessary data, like image
    image = db.session.query(Image).filter_by(id=requested_post.id).first()
    if image:
        image_data = image.data
    else:
        image_data = None

    return render_template("post.html", post=requested_post, image=image_data)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    requested_post = Post.query.filter_by(id=post_id).first()
    db.session.delete(requested_post)
    db.session.commit()
    flash("Deleted!")
    all_posts = Post.query.order_by(Post.id.desc()).all()
    return redirect(url_for('post'))


@app.route('/')
def home():
    all_posts = Post.query.order_by(Post.id.desc()).all()
    # all_images = Post.query.order_by(Image.id.desc()).all()

    return render_template("index.html", all_posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)
