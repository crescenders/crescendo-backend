from factory import CrescendoApplicationFactory

dev_app = CrescendoApplicationFactory.create_app("dev")
prod_app = CrescendoApplicationFactory.create_app("prod")

if __name__ == "__main__":
    dev_app.run(
        debug=True,
        host="0.0.0.0",
    )
