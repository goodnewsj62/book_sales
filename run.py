from app import create_app,db

app= create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db':db} #all you want available in flask shell


if __name__ == "__main__":
    if app.config.get('DEBUG'):
        app.run(debug=True)
        # app.run(debug=True, ssl_context="adhoc")# if installed only
    else:
        app.run(debug=False)