from flask import Blueprint, render_template
from auth.auth_utils import login_required, admin_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def home():
    return render_template('item-list.html')

@main_bp.route('/basket')
@login_required
def basket():
    return render_template('basket.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/register')
def register():
    return render_template('register.html')

@main_bp.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')

@main_bp.route('/item-list')
@login_required
def item_list():
    return render_template('item-list.html')

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main_bp.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')