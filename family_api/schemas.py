from marshmallow import Schema, fields


class BabySchema(Schema):
    baby_uuid = fields.UUID(dump_only=True, data_key='uuid')
    first_name = fields.Str(required=True)
    date_of_birth = fields.DateTime()


class FamilyMemberSchema(Schema):
    id = fields.Int(dump_only=True)
    user_uuid = fields.UUID(dump_only=True)


class FamilySchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, allow_none=False)

    babies = fields.Nested(BabySchema, many=True, dump_only=True)
    members = fields.Nested(FamilyMemberSchema, many=True, dump_only=True)
