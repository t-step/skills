from app.models import TodoItem


def list_todos(session) -> list[TodoItem]:
    return session.query(TodoItem).all()


def create_todo(session, title: str) -> TodoItem:
    item = TodoItem(title=title, done=False)
    session.add(item)
    session.commit()
    return item
