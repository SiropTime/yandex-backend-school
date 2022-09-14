from app import app, db, on_init


if __name__ == '__main__':
    db.create_all()
    on_init()
    app.run(host="0.0.0.0", port=8080)
