from flask import Blueprint, request
from home_manager import db

camera = Blueprint('camera', __name__)

class Camera(db.Model):
    __tablename__ = "cameras"

    id = db.Column(db.String(32), primary_key=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    room = db.Column(db.String(256), nullable=False)
    last_updated = db.Column(db.Integer(), nullable=False)
    images = db.Column(db.LargeBinary(), nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@camera.route('/camera/all', methods=['GET'])
def get_cameras():
    cameras = Camera.query.all()
    return {"cameras": [camera.to_dict() for camera in cameras]}, 200

@camera.route('/camera/<id>', methods=['GET', 'POST', 'DELETE'])
def camera(id):
    camera = Camera.query.filter_by(id=id).first()
    if not camera:
        return {"error": "Camera not found"}, 404

    if request.method == 'GET':
        return camera.to_dict(), 200
    elif request.method == 'POST':
        data = request.get_json()
        camera.name = data.get('name', camera.name)
        camera.room = data.get('room', camera.room)
        camera.last_updated = data.get('last_updated', camera.last_updated)

        # Grab current images, then append the new one
        images = camera.images or []
        images.append(data.get('image', None))
        camera.images = images

        db.session.commit()
        return camera.to_dict(), 200
    else:
        db.session.delete(camera)
        db.session.commit()
        return {"message": "Camera deleted"}, 200

@camera.route("/camera/<id>/upload_image", methods=['POST'])
def upload_image(id):
    camera = Camera.query.filter_by(id=id).first()
    if not camera:
        return {"error": "Camera not found"}, 404

    data = request.get_json()

    images = camera.images or []
    images.append(data.get('image', None))
    camera.images = images

    db.session.commit()
    return camera.to_dict(), 200
