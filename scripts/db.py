from flywheel.models import db, BaseModel


def get_all_models():
    import gc
    return [
        kls for kls in gc.get_objects()
        if issubclass(type(kls), type) and issubclass(kls, BaseModel)
        and kls != BaseModel and 'BaseModel' not in kls.__name__
    ]


def create_all_tables():
    db.create_tables(get_all_models())


def drop_all_tables():
    db.drop_tables(get_all_models())


def init():
    create_all_tables()


if __name__ == '__main__':
    init()
