from flask import current_app

from . import repository


def create_contact(name: str, email: str, message: str) -> None:
    current_app.logger.info("Saving contact message for %s", email)
    repository.create_contact(name, email, message)
