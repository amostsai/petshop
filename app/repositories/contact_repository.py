from app.repositories._utils import execute


def create_contact(name: str, email: str, message: str) -> None:
    query = "INSERT INTO contact (name, email, message) VALUES (%s, %s, %s);"
    execute(
        query,
        (name, email, message),
        error_message="Failed to save contact message",
        commit=True,
    )
