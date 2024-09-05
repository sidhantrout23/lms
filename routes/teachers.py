from flask import Blueprint, request, jsonify
from models import db
from models.models import Course

teachers = Blueprint('teachers', __name__)

@teachers.route('/teacher/<teacher_id>/courses', methods=['GET'])
def get_teacher_courses(teacher_id):
    courses = Course.query.filter_by(teacher_id=teacher_id).all()
    output = [{"id": course.id, "title": course.title, "description": course.description} for course in courses]
    return jsonify(output)
