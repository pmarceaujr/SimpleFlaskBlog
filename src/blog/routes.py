from src.blog import blog_app
from flask import *
from src.blog.models import *
from src.blog.helpers import *


@blog_app.route('/')
def index():  # put application's code here
    blog_data = Blog.query.all()
    user_data = User.query.all()
    authors = {user.id: f"{user.first_name} {user.last_name}" for user in user_data}
    return render_template('index.html', blog_data=blog_data, authors=authors)


@blog_app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@blog_app.route('/blogs/<blog_id>')
def get_blog(blog_id):
    blog=Blog.query.filter_by(id=blog_id).first()
    return render_template('blogs.html', blog=blog)


@blog_app.route('/my_blogs')
def get_my_blogs():
    my_blogs = Blog.query.filter_by(author_id=session['user_id']).all()
    return render_template('my_blogs.html', my_blogs=my_blogs)


@blog_app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register.html')
        else:
            User.create_user(
                fname=userDetails['first_name'],
                lname=userDetails['last_name'],
                user_name=userDetails['username'],
                email=userDetails['email'],
                password=userDetails['password']
            )
            flash('Registration Successful.  Please login.', 'success')
            return redirect(url_for('blog_app.log_user_in'))
    flash('New user?  Please register.', 'info')
    return render_template('register.html')


@blog_app.route('/login', methods=['GET', 'POST'])
def log_user_in():  # sourcery skip: use-named-expression
    if request.method == 'POST':
        userDetails = request.form
        user = User.query.filter_by(user_name=userDetails['user_name']).first()
        if user:
            if not user.check_password(userDetails['password']):
                flash('Invalid Password, Please try again', 'danger')
                return redirect(url_for('blog_app.log_user_in'))
            else:
                session['login'] = True
                session['firstname'] = user.first_name
                session['last_name'] = user.last_name
                session['user_id'] = user.id
                flash(f"Welcome, {session['firstname']}, you have successfully logged in. ", 'success')
                return redirect(url_for('blog_app.get_my_blogs'))
        else:
            flash('Invalid User Name, Please try again', 'danger')
            return redirect(url_for('blog_app.log_user_in'))
    return render_template('login.html')


@blog_app.route('/write', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        form_data = request.form
        new_blog = Blog(
                blog_body=form_data['blog_body'],
                title=form_data['title'],
                author_id=session['user_id'],
        )
        db.session.add(new_blog)
        db.session.commit()
        flash('Your new blog has been posted', 'success')
        return redirect(url_for('blog_app.get_my_blogs'))
    return render_template('write.html')


@blog_app.route('/edit/<blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    blog_data = Blog.query.filter_by(id=blog_id).first()
    if request.method == 'POST':
        form_data = request.form
        blog_data.blog_body=form_data['blog_body']
        blog_data.title=form_data['title'],
        db.session.commit()
        flash('Your blog has been updted', 'success')
        return redirect(url_for('blog_app.get_blog', blog_id=blog_data.id))
    else:
        return render_template('edit.html', blog_data=blog_data)


@blog_app.route('/delete/<blog_id>', methods=['GET', 'POST'])  # only need to delete, no get required, so not GET method needed
def delete_blog(blog_id):
    blog_data = Blog.query.filter_by(id=blog_id).first()
    if request.method == 'POST':
        db.session.delete(blog_data)
        db.session.commit()
        flash(f'Blog ID: {blog_data.id} Blog title: "{blog_data.title}" has been deleted', 'warning')
        return redirect(url_for('blog_app.get_my_blogs'))
    # return render_template('delete_book.html', book=book, book_id=book.id)
    flash(f'Blog ID: {blog_data.id} Blog title: "{blog_data.title}" will be deleted', 'danger')
    return render_template('delete.html', blog_data=blog_data)


@blog_app.route('/logout')
def log_user_off():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')
