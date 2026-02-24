from flask import Blueprint
from routes.books import books_bp
from routes.members import members_bp
from routes.transactions import transactions_bp

__all__ = ['books_bp', 'members_bp', 'transactions_bp']