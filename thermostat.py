from flask import Blueprint, request
from home_manager import db

thermostat = Blueprint('thermostat', __name__)

class Thermostat(db.Model):
    __tablename__ = "thermostat_data"

    id = db.Column(db.String(32), primary_key=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    room = db.Column(db.String(256), nullable=False)
    last_updated = db.Column(db.Integer(), nullable=False)
    temperature = db.Column(db.Float(), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@thermostat.route('/thermostat/all', methods=['GET'])
def get_thermostats():
    thermostats = Thermostat.query.all()
    return {"thermostats": [thermostat.to_dict() for thermostat in thermostats]}, 200

@thermostat.route('/thermostat/<id>', methods=['GET', 'POST', 'DELETE'])
def thermostat(id):
    thermostat = Thermostat.query.filter_by(id=id).first()
    if not thermostat:
        return {"error": "Thermostat not found"}, 404

    if request.method == 'GET':
        return thermostat.to_dict(), 200
    elif request.method == 'POST':
        data = request.get_json()
        thermostat.name = data.get('name', thermostat.name)
        thermostat.room = data.get('room', thermostat.room)
        thermostat.last_updated = data.get('last_updated', thermostat.last_updated)
        thermostat.temperature = data.get('temperature', thermostat.temperature)
        db.session.commit()
        return thermostat.to_dict(), 200
    else:
        db.session.delete(thermostat)
        db.session.commit()
        return {"message": "Thermostat deleted"}, 200