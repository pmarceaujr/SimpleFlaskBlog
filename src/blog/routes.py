from src.blog import blog_app
from flask import *
from src.blog.models import *


@blog_app.route('/')
def index():  # put application's code here
    data = User.query.all()
    print(data)
    return render_template('index.html')


@blog_app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@blog_app.route('/blog/<blog_id>')
def get_blog(blog_id):
    return render_template('blogs.html', blog_id=blog_id)


@blog_app.route('/my_blogs')
def get_my_blogs():
    return render_template('my_blogs.html')


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
def log_user_in():
    return render_template('login.html')


@blog_app.route('/write', methods=['GET', 'POST'])
def write_blog():
    return render_template('write.html')


@blog_app.route('/edit/<blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    return render_template('edit.html')


@blog_app.route('/delete/<blog_id>', methods=['POST'])  # only need to delete, no get required, so not GET method needed
def delete_blog(blog_id):
    return render_template('delete.html')


@blog_app.route('/logout')
def log_user_off():
    return render_template('logout.html')
