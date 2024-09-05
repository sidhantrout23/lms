from flask import Blueprint, request,render_template,redirect, url_for, session
from models import db
from models.models import User
from models.models import Course
from models.models import CourseMaterial
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            session['user_id'] = user.id
            print(f"User logged in: {user.id}")  # Debugging statement
            return redirect(url_for('main.dashboard'))
        else:
            return render_template('login.html', message="Invalid email or password")

    return render_template('login.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/courses')
def courses():
    user_id = session.get('user_id')
    if not user_id:
        print("No user_id in session")  # Debugging statement
        return redirect(url_for('main.login'))
    user = User.query.get(user_id)
    if not user:
        print("User not found")  # Debugging statement
        return redirect(url_for('main.login'))
    return render_template('courses.html', user=user)

@main.route('/course/<course_id>')
def course_detail(course_id):
    user_id = session.get('user_id')
    if not user_id:
        print("No user_id in session")  # Debugging statement
        return redirect(url_for('main.login'))
    user = User.query.get(user_id)
    if not user:
        print("User not found")  # Debugging statement
        return redirect(url_for('main.login'))
    course = Course.query.get_or_404(course_id)
    materials = CourseMaterial.query.filter_by(course_id=course_id).all()
    return render_template('course_detail.html', course=course, materials=materials,user=user)






@main.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.login')) 