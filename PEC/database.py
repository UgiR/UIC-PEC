from PEC.extensions import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer(), primary_key=True)


class UserAttributeModel(BaseModel):
    __abstract__ = True

    @classmethod
    def get(cls, **kwargs):
        '''Function prevents duplicate entries to many-to-many relationships between users and attributes
        :param kwargs:
        :return: An instance of the attribute model. If it did not exist on function call, one is created
        '''
        obj = db.session.query(cls).filter_by(**kwargs).first()
        if obj is None:
            obj = cls(**kwargs)
            db.session.add(obj)
            db.session.commit()
        return obj

    def __repr__(self):
        return '<User attribute {}>'.format(self.name)


class CRUDMixin:
    """Basic CRUD operations for models"""
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            self.save()
        return self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()
