from flask import Blueprint, request, render_template, jsonify
from helpers import token_required
from models import db, User, book_schema, books_schema, Book

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
def getdata():
    return {'Hello': 'World'}

@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    author = request.json['author']
    book_title = request.json['book_title']
    book_format = request.json['book_format']
    book_length = request.json['book_length']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(isbn, author, book_title, book_format, book_length, user_token=user_token)
    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)

    return jsonify(response)


@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)

    return jsonify(response)

@api.route('/books/<isbn>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, isbn):
    book = Book.query.get(isbn)
    response = book_schema.dump(book)
    return jsonify(response)


@api.route('/contacts/<isbn>', methods = ['POST', 'PUT'])
@token_required
def update_contact(current_user_token, isbn):
    book = Book.query.get(isbn)
    book.name = request.json['author']
    book.email = request.json['book_title']
    book.address = request.json['book_format']
    book.phone_number = request.json['book_length']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)

    return jsonify(response)

#Delete Endpoint
@api.route('/books/<isbn>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, isbn):
    book = Book.query.get(isbn)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)