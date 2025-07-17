from app import db

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))

    bookings = db.relationship('Booking', backref='guest', lazy=True)


class AccommodationType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    accommodations = db.relationship('Accommodation', backref='type', lazy=True)


class Accommodation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price_per_night = db.Column(db.Float)
    image_url = db.Column(db.String(255))

    type_id = db.Column(db.Integer, db.ForeignKey('accommodation_type.id'), nullable=False)

    bookings = db.relationship('Booking', backref='accommodation', lazy=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodation.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
