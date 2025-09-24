from flask import current_app

from app.repositories import contact_repository


def create_contact(name: str, email: str, message: str) -> None:
    current_app.logger.info("Saving contact message for %s", email)
    contact_repository.create_contact(name, email, message)
