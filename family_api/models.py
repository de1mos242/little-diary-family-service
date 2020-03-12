from sqlalchemy import MetaData, Table, Integer, Column, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

meta = MetaData()

families_table = Table(
    'family', meta,

    Column('id', Integer, primary_key=True),
    Column('title', Text, nullable=False)
)

family_members_table = Table(
    'family_member', meta,

    Column('id', Integer, primary_key=True),
    Column('user_uuid', UUID, unique=True, nullable=False),
    Column('family_id', Integer, ForeignKey('family.id', ondelete='CASCADE')),

    UniqueConstraint('family_id', 'user_uuid', name="family_member_family_id_user_uuid_uidx")
)

babies_table = Table(
    'baby', meta,

    Column('id', Integer, primary_key=True),
    Column('baby_uuid', UUID, unique=True, nullable=False),
    Column('first_name', Text, nullable=False),
    Column('date_of_birth', DateTime),
    Column('family_id', Integer, ForeignKey('family.id', ondelete='CASCADE'), index=True)
)
