from flask import Flask

import os
from modules import db
from modules.administrators import Administrators
from modules.airline_companies import AirlineCompanies
from modules.countries import Countries
from modules.customers import Customers
from modules.flights import Flights
from modules.tickets import Tickets
from modules.user_roles import UserRoles
from modules.users import Users

from routes import Routes

app = Flask(__name__)
app.config.from_pyfile('.config')
db.init_app(app)

# Instanse of Blueprint classes
routes_blueprint = Routes('routes', __name__)
    
# Register Blueprints
app.register_blueprint(routes_blueprint)

# Configure the database URI using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if __name__ == "__main__":
    
    # If running in Docker, initialize the database
    if os.environ.get('DOCKER_CONTAINER'):
        with app.app_context():
            admins=Administrators()
            airlines=AirlineCompanies()
            countries=Countries()
            customers=Customers()
            flights=Flights()
            tickets=Tickets()
            user_roles=UserRoles()
            users=Users()
            
            db.create_all()
        
    app.run(debug=app.config['DEBUG'], use_reloader=False, port=3000)