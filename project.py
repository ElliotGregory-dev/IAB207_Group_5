from files import create_app, db

##if __name__=='__main__':
n_app=create_app()

ctx = n_app.app_context()
ctx.push()
db.create_all()

n_app.run(debug=True)
