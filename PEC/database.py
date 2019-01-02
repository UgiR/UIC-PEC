from PEC.extensions import db


class CRUDMixin:

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


class UserAttribute(CRUDMixin):
    @classmethod
    def get(cls, **kwargs):
        obj = db.session.query(cls).filter_by(**kwargs).first()
        if obj is None:
            obj = cls.create(**kwargs)
        return obj
