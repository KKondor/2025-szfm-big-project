from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('base.html')

@main_bp.route('/basket')
def basket():
    return render_template('basket.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/item-list')
def item_list():
    return render_template('item-list.html')