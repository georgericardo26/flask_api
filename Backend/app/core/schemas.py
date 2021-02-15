from marshmallow import Schema, fields, post_load, validates, ValidationError

from Backend.app.database import db
from Backend.app.core.models import Parent, Child


class ParentSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)

    def create_parent(self, data):
        parent = Parent(**data)
        db.session.add(parent)
        db.session.commit()
        return parent

    def update_parent(self, parent, data):
        parent.name = data.get('name', parent.name)
        db.session.commit()
        return parent


class ChildSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    # parents = fields.Method("get_parents")
    parents_ids = fields.List(fields.Integer, required=True, load_only=True)
    parents = fields.Nested(ParentSchema, many=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    def create_child(self, data):
        parents_input = data.pop("parents_ids")
        parents = Parent.query.filter(Parent.id.in_(parents_input)).all()

        child = Child(**data)

        for parent in parents:
            child.parents.append(parent)

        db.session.add(child)
        db.session.commit()
        return child

    def update_child(self, child, data):
        parents_input = data.pop("parents_ids")
        parents = Parent.query.filter(Parent.id.in_(parents_input)).all()

        child.parents = []

        for parent in parents:
            child.parents.append(parent)

        child.name = data.get('name', child.name)
        db.session.commit()
        return child

    # uri = fields.Method("get_item_uri")
    #
    # def get_item_uri(self, obj):
    #     return '/api/child/{obj.id}/'.format(
    #         obj=obj,
    #     )

    @validates('parents_ids')
    def validate_parents_ids(self, ids, **kwargs):
        if len(ids) > 2:
            raise ValidationError("You can not add more than 2 parents for each child.")

    #
    # @validates('emails')
    # def validate_emails(self, emails):
    #     exists_in_contact_emails = []
    #     for d in emails:
    #         email = d.get('email')
    #         if bool(ContactEmail.query.filter_by(email=email).first()):
    #             exists_in_contact_emails.append(email)
    #
    #     if exists_in_contact_emails:
    #         raise ValidationError(
    #             '"{emails}" emails already exists, '
    #             'please try different emails.'.format(
    #                 emails=", ".join(exists_in_contact_emails)
    #             )
    #         )

    # @post_load
    # def create_contact(self, data):
    #     email_list = data.pop('emails', list())
    #     contact = Contact(**data)
    #     contact_emails = [ContactEmail(email=d.get('email')) for d in email_list]
    #     contact.emails.extend(contact_emails)
    #     db.session.add(contact)
    #     db.session.add_all(contact_emails)
    #     db.session.commit()
    #     self.instance = contact
    #
    # def update_parent(self, parent, data):
    #     parent.name = data.get('name', parent.name)
    #     # if emails:
    #     #     ContactEmail.query.filter_by(contact_id=contact.id).delete()
    #     #     db.session.commit()
    #     #     new_contact_emails = [ContactEmail(email=d.get('email')) for d in emails]
    #     #     contact.emails.extend(new_contact_emails)
    #     #     db.session.add_all(new_contact_emails)
    #     db.session.commit()
