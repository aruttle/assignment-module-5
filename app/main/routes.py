from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime
from functools import wraps
from app.main import main
from app import db
from app.models import Guest, Accommodation, Booking, AccommodationType

# Admin login required decorator
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash("Please log in to access the admin area.", "warning")
            return redirect(url_for('main.admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@main.route('/')
def home():
    accommodations = Accommodation.query.limit(3).all()
    return render_template('home.html', accommodations=accommodations)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/accommodations')
def accommodations():
    accommodations = Accommodation.query.all()
    return render_template('accommodations.html', accommodations=accommodations)


@main.route('/gallery')
def gallery():
    return render_template('gallery.html')


@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '0000': 
            session['admin_logged_in'] = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.admin_bookings'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('admin_login.html')


@main.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.admin_login'))


@main.route('/admin/bookings')
@admin_login_required
def admin_bookings():
    bookings = Booking.query.all()
    return render_template('admin_bookings.html', bookings=bookings)


@main.route('/admin/delete-booking/<int:booking_id>', methods=['POST'])
@admin_login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted successfully.', 'success')
    return redirect(url_for('main.admin_bookings'))


@main.route('/book', methods=['GET', 'POST'])
def book():
    accommodation_types = AccommodationType.query.all()
    accommodation_objects = Accommodation.query.all()

    accommodations = [
        {
            "id": acc.id,
            "name": acc.name,
            "type_id": acc.type_id
        }
        for acc in accommodation_objects
    ]

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        accommodation_id = request.form.get('accommodation')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        if not all([name, email, accommodation_id, start_date_str, end_date_str]):
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('main.book'))

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('main.book'))

        if start_date >= end_date:
            flash('End date must be after start date.', 'danger')
            return redirect(url_for('main.book'))

        # Check for overlapping bookings
        existing_bookings = Booking.query.filter_by(accommodation_id=accommodation_id).all()
        for booking in existing_bookings:
            if not (end_date <= booking.start_date or start_date >= booking.end_date):
                flash('Selected accommodation is not available for those dates.', 'danger')
                return redirect(url_for('main.book'))

        # Save guest and booking
        guest = Guest.query.filter_by(email=email).first()
        if not guest:
            guest = Guest(name=name, email=email, phone=phone)
            db.session.add(guest)
            db.session.commit()

        booking = Booking(
            guest_id=guest.id,
            accommodation_id=accommodation_id,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(booking)
        db.session.commit()

        flash('Booking successful! Thank you.', 'success')
        return redirect(url_for('main.home'))

    # GET request - prepare booked date ranges grouped by accommodation
    from collections import defaultdict
    all_bookings = Booking.query.all()
    booked_ranges_by_accommodation = defaultdict(list)

    for booking in all_bookings:
        booked_ranges_by_accommodation[booking.accommodation_id].append({
            'start': booking.start_date.strftime('%Y-%m-%d'),
            'end': booking.end_date.strftime('%Y-%m-%d')
        })

    return render_template(
        'book.html',
        accommodation_types=accommodation_types,
        accommodations=accommodations,
        booked_ranges=booked_ranges_by_accommodation
    )


@main.route('/accommodation/<int:accommodation_id>')
def accommodation_detail(accommodation_id):
    accommodation = Accommodation.query.get_or_404(accommodation_id)
    return render_template('accommodation_detail.html', accommodation=accommodation)

# 404 handler
@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# 500 handler
@main.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500