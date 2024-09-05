from flask import Blueprint, request, jsonify
from models import db
from models.models import Enrollment, Course

enrollment = Blueprint('enrollment', __name__)

@enrollment.route('/enroll', methods=['POST'])
def enroll():
    data = request.get_json()
    new_enrollment = Enrollment(user_id=data['user_id'], course_id=data['course_id'])
    db.session.add(new_enrollment)
    db.session.commit()
    return jsonify({"message": "Enrolled successfully!"})

@enrollment.route('/enrollments/<user_id>', methods=['GET'])
def get_enrollments(user_id):
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    courses = [Enrollment.query.get(enrollment.course_id) for enrollment in enrollments]
    output = [
        {
            "course_id": course.id
        } for course in courses
    ]
    return jsonify(output)
