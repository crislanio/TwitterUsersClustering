from flask import Flask, request, render_template
from api.API import get_api_instance
from clustering.kmedoids import update_clusters_in_db
from db.Insert_users import insert_users_from_time_to_db, set_auto_increment_keys_for_already_inserted_users, \
    insert_more_users_to_db, insert_more_users_without_unnecessary_api_calls
from db.get_utilities import get_clusters_from_db

app = Flask(__name__)


@app.route('/')
def home_page():
    return app.send_static_file('home.html')


@app.route('/main', methods=['POST'])
def main_page():
    api = get_api_instance(request.form.get('consumer_key'), request.form.get('consumer_secret'),
                           request.form.get('access_token'), request.form.get('access_token_secret'))
    return app.send_static_file('main.html')


@app.route('/insert_users', methods=['POST'])
def insert_users():
    api = get_api_instance()
    first = int(request.form.get('first_page'))
    last = int(request.form.get('last_page'))
    insert_users_from_time_to_db(api, first, last)
    return app.send_static_file('main.html')


@app.route('/insert_more_users', methods=['POST'])
def insert_more_users():
    api = get_api_instance()
    # first = int(request.form.get('first_page'))
    # last = int(request.form.get('last_page'))
    insert_more_users_to_db(api)
    return app.send_static_file('main.html')


@app.route('/insert_more_users_faster', methods=['POST'])
def insert_more_users_faster():
    api = get_api_instance()
    # first = int(request.form.get('first_page'))
    # last = int(request.form.get('last_page'))
    insert_more_users_without_unnecessary_api_calls(api, min_friends=10, min_followers=10)
    return app.send_static_file('main.html')



@app.route('/modify_users', methods=['POST'])
def set_keys():
    api = get_api_instance()
    set_auto_increment_keys_for_already_inserted_users(api)
    return app.send_static_file('home.html')


@app.route('/update_clusters', methods=['POST'])
def update_clusters():
    k = int(request.form.get('k_value')) - 1
    update_clusters_in_db(k)
    return app.send_static_file('main.html')


@app.route('/show_clusters', methods=['GET', 'POST'])
def show_clusters():
    clusters = get_clusters_from_db()
    # for c in clusters:
    #     print c, len(clusters[c])
    return render_template('clusters.html', title='Clusters', clusters=clusters)
    # return app.send_static_file('main.html')


if __name__ == '__main__':
    app.run(debug=True)
