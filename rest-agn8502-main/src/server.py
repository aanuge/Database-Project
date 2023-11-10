from flask import Flask
from flask_restful import Resource, Api
from api.chat import *

app = Flask(__name__)
api = Api(app)

api.add_resource(home_screen, '/')
api.add_resource(list_all_users, '/list_all_users')
api.add_resource(list_communities_and_channels, '/list_communities_and_channels')
api.add_resource(list_arrakis_messages, '/list_arrakis_messages/<string:id>')
api.add_resource(list_comedy_messages, '/list_comedy_messages/<string:id>')
api.add_resource(list_dms, '/list_dms/<string:num>')
api.add_resource(add_user, '/add')
api.add_resource(delete_user, '/delete')
api.add_resource(update_user, '/update')
api.add_resource(login, '/login')
api.add_resource(logout, '/logout')
api.add_resource(send_dm, '/send_dm')

if __name__ == '__main__':
    rebuild_tables()
    app.run(debug=True)