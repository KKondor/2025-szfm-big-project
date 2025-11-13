import os
from flask import Flask, render_template, session
from routes.main_routes import main_bp
from routes.api_routes import api_bp

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(main_bp)
app.register_blueprint(api_bp)

# Context processors to make functions available in templates
@app.context_processor
def inject_user_functions():
    def is_admin():
        return session.get('user_role') == 'admin'
    
    def is_user():
        return session.get('user_role') == 'user'
    
    return dict(is_admin=is_admin, is_user=is_user)

if __name__ == '__main__':
    app.run(debug=True)