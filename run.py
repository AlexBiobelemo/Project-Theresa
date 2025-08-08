from app import create_app

app = create_app()

if __name__ == '__main__':
    # Setting debug=True enables auto-reloading and shows detailed errors in the browser.
    # Turn this off for production.

    app.run(debug=False)
