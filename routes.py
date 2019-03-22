from config import app
from controller_functions import index, process, login, active, logout, create_tweet, add_like, delete_tweet, edit_tweet, update_tweet, show_user_list, follow_user

app.add_url_rule('/', view_func=index)
app.add_url_rule('/register', view_func=process, methods=['POST'])
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/dashboard', view_func=active)
app.add_url_rule('/logout', view_func=logout)
app.add_url_rule('/tweets/create', view_func=create_tweet, methods=['POST'])
app.add_url_rule('/tweets/<id>/add_like', view_func=add_like, methods=['POST'])
app.add_url_rule('/tweets/<id>/delete', view_func=delete_tweet, methods=['POST'])
app.add_url_rule('/tweets/<id>/edit', view_func=edit_tweet)
app.add_url_rule('/tweets/<id>/update', view_func=update_tweet, methods=['POST'])
app.add_url_rule('/users', view_func=show_user_list)
app.add_url_rule('/users/<id>/follow', view_func=follow_user, methods=['POST'])