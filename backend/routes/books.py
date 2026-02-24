from flask import Blueprint, request, jsonify
from models import db, Book
from datetime import datetime

books_bp = Blueprint('books', __name__, url_prefix='/api/books')


@books_bp.route('', methods=['GET'])
def get_books():
    """Get all books with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')

    query = Book.query

    if search:
        query = query.filter(
            (Book.title.ilike(f'%{search}%')) |
            (Book.author.ilike(f'%{search}%')) |
            (Book.isbn.ilike(f'%{search}%'))
        )

    if category:
        query = query.filter(Book.category == category)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'books': [book.to_dict() for book in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID"""
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())


@books_bp.route('', methods=['POST'])
def create_book():
    """Create a new book"""
    data = request.get_json()

    # Check if ISBN already exists
    if Book.query.filter_by(isbn=data.get('isbn')).first():
        return jsonify({'error': 'Book with this ISBN already exists'}), 400

    book = Book(
        isbn=data.get('isbn'),
        title=data.get('title'),
        author=data.get('author'),
        publisher=data.get('publisher'),
        publication_year=data.get('publication_year'),
        category=data.get('category'),
        total_copies=data.get('total_copies', 1),
        available_copies=data.get('available_copies', data.get('total_copies', 1)),
        location=data.get('location')
    )

    db.session.add(book)
    db.session.commit()

    return jsonify(book.to_dict()), 201


@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update a book"""
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    for key, value in data.items():
        if hasattr(book, key) and key not in ['id', 'created_at']:
            setattr(book, key, value)

    db.session.commit()
    return jsonify(book.to_dict())


@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book"""
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})


@books_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all book categories"""
    categories = db.session.query(Book.category).distinct().all()
    return jsonify({'categories': [cat[0] for cat in categories if cat[0]]})


@books_bp.route('/available', methods=['GET'])
def get_available_books():
    """Get all books with available copies"""
    books = Book.query.filter(Book.available_copies > 0).all()
    return jsonify({'books': [book.to_dict() for book in books]})