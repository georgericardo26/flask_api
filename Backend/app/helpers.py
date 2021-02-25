from werkzeug.security import check_password_hash


def get_or_create(db, model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance

    instance = model(**kwargs)

    db.session.add(instance)
    db.session.commit()

    return instance


def check_username_and_password(db, model, data):
    errors = []
    username = data.get("username")
    password = data.get("password")

    user = db.session.query(model).filter_by(username=username).one_or_none()
    if not user:
        errors.append("User Not found.")
        return None, errors

    if not check_password_hash(user.password, password):
        errors.append("Password wrong.")
        return user, errors

    return user, errors
