from datetime import datetime

from sqlalchemy.orm import validates

from Backend.app.database import db

children = db.Table('children',
    db.Column('child_id', db.Integer, db.ForeignKey('child.id'), primary_key=True),
    db.Column('parent_id', db.Integer, db.ForeignKey('parent.id'), primary_key=True)
)


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20), nullable=True)
    children = db.relationship('Child', secondary=children, lazy='subquery',
                               backref=db.backref('parents', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    __mapper_args__ = {
        "order_by": created_at
    }
    __tablename__ = 'parent'

    def __repr__(self):
        return (
            '<{class_name}('
            'parent_id={self.id}, '
            'name="{self.name}")>'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )


class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    __mapper_args__ = {
        "order_by": created_at
    }
    __tablename__ = 'child'

    def __repr__(self):
        return (
            '<{class_name}('
            'child_id={self.id}, >'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
