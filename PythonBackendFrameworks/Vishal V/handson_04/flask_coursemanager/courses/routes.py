from flask import Blueprint, jsonify, request

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

courses = []


def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    return make_response_json(courses)


@courses_bp.route('/', methods=['POST'])
def create_course():
    payload = request.get_json(silent=True) or {}
    required_fields = ['name', 'code', 'credits']
    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        return make_response_json({'error': f'Missing required fields: {", ".join(missing)}'}, 400)

    course = {
        'id': len(courses) + 1,
        'name': payload['name'],
        'code': payload['code'],
        'credits': payload['credits'],
    }
    courses.append(course)
    return make_response_json(course, 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = next((item for item in courses if item['id'] == course_id), None)
    if course is None:
        return make_response_json({'error': 'Course not found'}, 404)
    return make_response_json(course)


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = next((item for item in courses if item['id'] == course_id), None)
    if course is None:
        return make_response_json({'error': 'Course not found'}, 404)

    payload = request.get_json(silent=True) or {}
    if 'name' in payload:
        course['name'] = payload['name']
    if 'code' in payload:
        course['code'] = payload['code']
    if 'credits' in payload:
        course['credits'] = payload['credits']
    return make_response_json(course)


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    for index, course in enumerate(courses):
        if course['id'] == course_id:
            del courses[index]
            return make_response_json({'message': 'Course deleted'})
    return make_response_json({'error': 'Course not found'}, 404)
