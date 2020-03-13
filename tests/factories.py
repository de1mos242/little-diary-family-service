from datetime import datetime, timedelta
from uuid import uuid4

import factory


class FamilyFactory(factory.Factory):
    class Meta:
        model = dict

    title = factory.Sequence(lambda n: f'Family title {n}')


class FamilyMemberFactory(factory.Factory):
    class Meta:
        model = dict

    user_uuid = factory.LazyFunction(lambda: str(uuid4()))
    family_id = factory.Sequence(lambda n: n)


class BabyFactory(factory.Factory):
    class Meta:
        model = dict

    baby_uuid = factory.LazyFunction(lambda: str(uuid4()))
    first_name = factory.Sequence(lambda n: f"Baby name {n}")
    date_of_birth = factory.Sequence(lambda n: datetime.now() - timedelta(days=n))
    family_id = factory.Sequence(lambda n: n)
