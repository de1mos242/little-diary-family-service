from marshmallow import Schema, fields


class BabySchema(Schema):
    baby_uuid = fields.UUID(dump_only=True, data_key='uuid')
    first_name = fields.Str(required=True)
    date_of_birth = fields.Date()


class FamilyMemberSchema(Schema):
    member_uuid = fields.UUID(dump_only=True, data_key='uuid')
    user_uuid = fields.UUID(dump_only=True)


class FamilySchema(Schema):
    family_uuid = fields.UUID(dump_only=True, data_key='uuid')
    title = fields.Str(required=True, allow_none=False)

    babies = fields.Nested(BabySchema, many=True, dump_only=True)
    members = fields.Nested(FamilyMemberSchema, many=True, dump_only=True)


class InvitationTokenSchema(Schema):
    token = fields.Str(required=True, allow_none=False)
