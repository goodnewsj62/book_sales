from app import create_app,db,pwd_context
from app.models import Payment,Admin
from livereload import Server

app= create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db':db,'Admin':Admin,"Payment":Payment,'pw':pwd_context} #all you want available in flask shell


if __name__ == "__main__":
    if app.config.get('DEBUG'):
        server = Server(app =app.wsgi_app)
        server.serve(port=5000)
        # app.run(debug=True, ssl_context="adhoc")# if installed only
    else:
        app.run(debug=False)