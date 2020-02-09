from flask_blog import create_app

app = create_app()


if __name__ == '__main__':

    app.run()


#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '@qwerty1234!'
#app.config['MYSQL_DB'] = 'CHINAGUIDE'
#mysql=MySQL(app)