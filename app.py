from core.factory.app_factory import ApplicationFactory

app = ApplicationFactory.create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
    )
