from flask import Flask, render_template
from routes.main_routes import main_bp

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)