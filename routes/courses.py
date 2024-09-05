from flask import Blueprint, request, jsonify, session,render_template,redirect,url_for
from werkzeug.utils import secure_filename
import os
from models import db
from models.models import Course, CourseMaterial, User

courses = Blueprint('courses', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'doc','docx', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@courses.route('/courses', methods=['POST'])
def create_course():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user or not user.is_teacher:
        return jsonify({"message": "Unauthorized"}), 403

    # Get form data instead of JSON
    title = request.form.get('title')
    description = request.form.get('description')

    # Ensure both title and description are provided
    if not title or not description:
        return jsonify({"message": "Missing title or description"}), 400

    # Create a new course using form data
    new_course = Course(title=title, description=description, teacher_id=user_id)
    db.session.add(new_course)
    db.session.commit()
    return render_template('courses.html',user=user)


@courses.route('/courses', methods=['GET'])
def get_courses():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if user and user.is_teacher:
        courses = Course.query.filter_by(teacher_id=user_id).all()
    else:
        courses = Course.query.all()

    output = [{"id": course.id, "title": course.title, "description": course.description, "teacher_id": course.teacher_id} for course in courses]
    return jsonify(output)

@courses.route('/add-course', methods=['GET'])
def add_course_form():
    return render_template('add_course.html')

@courses.route('/course/<int:course_id>', methods=['GET'])
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_detail.html', course=course)


@courses.route('/course/<int:course_id>/materials', methods=['POST'])
def add_course_material(course_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user or not user.is_teacher:
        return jsonify({"message": "Unauthorized"}), 403

    course = Course.query.get_or_404(course_id)
    if course.teacher_id != user_id:
        return jsonify({"message": "Forbidden"}), 403

    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('static/uploads', filename)
        file.save(file_path)
        new_material = CourseMaterial(
            filename=filename,
            url=file_path,
            course_id=course_id
        )
        db.session.add(new_material)
        db.session.commit()
        return redirect(url_for('main.course_detail', course_id=course_id))

    return jsonify({"message": "File type not allowed"}), 400
