from flask import Blueprint

def create_routes(app):
    from .users import users
    from .courses import courses
    from .enrollment import enrollment
    from .materials import materials
    from .teachers import teachers

    app.register_blueprint(users, url_prefix='/api')
    app.register_blueprint(courses, url_prefix='/api')
    app.register_blueprint(enrollment, url_prefix='/api')
    app.register_blueprint(materials, url_prefix='/api')
    app.register_blueprint(teachers, url_prefix='/api')
