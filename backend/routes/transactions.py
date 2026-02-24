from flask import Blueprint, request, jsonify
from models import db, Book, Member, Transaction
from datetime import date, timedelta
import uuid

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

FINE_PER_DAY = 5.0  # Fine amount per day overdue
MAX_BORROW_DAYS = 14  # Maximum borrowing period in days


@transactions_bp.route('', methods=['GET'])
def get_transactions():
    """Get all transactions with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', '')
    member_id = request.args.get('member_id', type=int)

    query = Transaction.query

    if status:
        query = query.filter(Transaction.status == status)

    if member_id:
        query = query.filter(Transaction.member_id == member_id)

    query = query.order_by(Transaction.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'transactions': [t.to_dict() for t in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@transactions_bp.route('/borrow', methods=['POST'])
def borrow_book():
    """Borrow a book"""
    data = request.get_json()
    book_id = data.get('book_id')
    member_id = data.get('member_id')

    # Validate book
    book = Book.query.get_or_404(book_id)
    if book.available_copies <= 0:
        return jsonify({'error': 'No copies available for borrowing'}), 400

    # Validate member
    member = Member.query.get_or_404(member_id)
    if member.status != 'active':
        return jsonify({'error': 'Member is not active'}), 400

    # Check if member has reached max books limit
    active_borrows = Transaction.query.filter_by(
        member_id=member_id,
        status='active'
    ).count()

    if active_borrows >= member.max_books_allowed:
        return jsonify({'error': f'Member has reached maximum books limit ({member.max_books_allowed})'}), 400

    # Create transaction
    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=MAX_BORROW_DAYS)

    transaction = Transaction(
        transaction_id=f"TXN{uuid.uuid4().hex[:8].upper()}",
        book_id=book_id,
        member_id=member_id,
        transaction_type='borrow',
        borrow_date=borrow_date,
        due_date=due_date,
        status='active'
    )

    # Update book available copies
    book.available_copies -= 1

    db.session.add(transaction)
    db.session.commit()

    return jsonify(transaction.to_dict()), 201


@transactions_bp.route('/return', methods=['POST'])
def return_book():
    """Return a borrowed book"""
    data = request.get_json()
    transaction_id = data.get('transaction_id')

    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    if transaction.status != 'active':
        return jsonify({'error': 'This book has already been returned'}), 400

    return_date = date.today()
    transaction.return_date = return_date
    transaction.status = 'returned'

    # Calculate fine if overdue
    if return_date > transaction.due_date:
        days_overdue = (return_date - transaction.due_date).days
        fine_amount = days_overdue * FINE_PER_DAY
        transaction.fine_amount = fine_amount

    # Update book available copies
    book = Book.query.get(transaction.book_id)
    if book:
        book.available_copies += 1

    db.session.commit()

    return jsonify(transaction.to_dict())


@transactions_bp.route('/overdue', methods=['GET'])
def get_overdue_books():
    """Get all overdue transactions"""
    today = date.today()

    overdue_transactions = Transaction.query.filter(
        Transaction.status == 'active',
        Transaction.due_date < today
    ).all()

    # Update status to overdue
    for t in overdue_transactions:
        t.status = 'overdue'
    db.session.commit()

    return jsonify({
        'overdue_books': [t.to_dict() for t in overdue_transactions],
        'count': len(overdue_transactions)
    })


@transactions_bp.route('/pay-fine/<int:transaction_id>', methods=['POST'])
def pay_fine(transaction_id):
    """Pay fine for a transaction"""
    transaction = Transaction.query.get_or_404(transaction_id)

    if transaction.fine_amount <= 0:
        return jsonify({'error': 'No fine to pay'}), 400

    if transaction.fine_paid:
        return jsonify({'error': 'Fine already paid'}), 400

    transaction.fine_paid = True
    db.session.commit()

    return jsonify(transaction.to_dict())


@transactions_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get transaction statistics"""
    total_books = Book.query.count()
    total_members = Member.query.count()
    active_borrows = Transaction.query.filter_by(status='active').count()
    overdue_books = Transaction.query.filter_by(status='overdue').count()

    # Calculate total fines
    total_fines = db.session.query(
        db.func.sum(Transaction.fine_amount)
    ).filter(Transaction.fine_paid == False).scalar() or 0

    return jsonify({
        'total_books': total_books,
        'total_members': total_members,
        'active_borrows': active_borrows,
        'overdue_books': overdue_books,
        'total_unpaid_fines': float(total_fines)
    })