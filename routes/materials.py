from flask import Blueprint, request, jsonify
from models import db
from models.models import CourseMaterial

materials = Blueprint('materials', __name__)

@materials.route('/materials', methods=['POST'])
def add_material():
    data = request.get_json()
    new_material = CourseMaterial(
        filename=data['filename'],
        url=data['url'],
        course_id=data['course_id']
    )
    db.session.add(new_material)
    db.session.commit()
    return jsonify({"message": "Material added successfully!"})

@materials.route('/materials/<course_id>', methods=['GET'])
def get_materials(course_id):
    materials = CourseMaterial.query.filter_by(course_id=course_id).all()
    output = [{"id": material.id, "filename": material.filename, "url": material.url} for material in materials]
    return jsonify(output)
