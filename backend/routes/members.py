from flask import Blueprint, request, jsonify
from models import db, Member
from datetime import date, timedelta

members_bp = Blueprint('members', __name__, url_prefix='/api/members')


@members_bp.route('', methods=['GET'])
def get_members():
    """Get all members with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')

    query = Member.query

    if search:
        query = query.filter(
            (Member.first_name.ilike(f'%{search}%')) |
            (Member.last_name.ilike(f'%{search}%')) |
            (Member.email.ilike(f'%{search}%')) |
            (Member.member_id.ilike(f'%{search}%'))
        )

    if status:
        query = query.filter(Member.status == status)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'members': [member.to_dict() for member in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@members_bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Get a specific member by ID"""
    member = Member.query.get_or_404(member_id)
    return jsonify(member.to_dict())


@members_bp.route('', methods=['POST'])
def create_member():
    """Create a new member"""
    data = request.get_json()

    # Generate member ID
    last_member = Member.query.order_by(Member.id.desc()).first()
    next_id = (last_member.id + 1) if last_member else 1
    member_id = f"LIB{next_id:05d}"

    # Check if email already exists
    if Member.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Member with this email already exists'}), 400

    join_date = date.today()
    expiry_date = join_date + timedelta(days=365)  # 1 year membership

    member = Member(
        member_id=member_id,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        membership_type=data.get('membership_type', 'standard'),
        join_date=join_date,
        expiry_date=expiry_date,
        max_books_allowed=data.get('max_books_allowed', 3)
    )

    db.session.add(member)
    db.session.commit()

    return jsonify(member.to_dict()), 201


@members_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Update a member"""
    member = Member.query.get_or_404(member_id)
    data = request.get_json()

    for key, value in data.items():
        if hasattr(member, key) and key not in ['id', 'member_id', 'created_at']:
            setattr(member, key, value)

    db.session.commit()
    return jsonify(member.to_dict())


@members_bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete a member"""
    member = Member.query.get_or_404(member_id)

    # Check if member has active borrows
    active_borrows = [t for t in member.transactions if t.status == 'active']
    if active_borrows:
        return jsonify({'error': 'Cannot delete member with active borrows'}), 400

    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted successfully'})


@members_bp.route('/<int:member_id>/borrowed', methods=['GET'])
def get_member_borrowed_books(member_id):
    """Get books currently borrowed by a member"""
    member = Member.query.get_or_404(member_id)
    from models import Transaction

    active_borrows = Transaction.query.filter_by(
        member_id=member_id,
        status='active'
    ).all()

    return jsonify({
        'member': member.to_dict(),
        'borrowed_books': [t.to_dict() for t in active_borrows]
    })