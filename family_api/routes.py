from family_api.views.baby_access_view import BabyAccessView
from family_api.views.baby_view import BabyView
from family_api.views.family_member_view import FamilyMemberListView, FamilyMemberTokenView, FamilyMemberView
from family_api.views.family_view import FamilyView, FamilyListView


def setup_routes(app):
    uuid_regexp = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    app.router.add_view(f'/v1/family', FamilyListView)
    app.router.add_view(f'/v1/family/{{family_uuid:{uuid_regexp}}}', FamilyView)
    app.router.add_view(f'/v1/family/{{family_uuid:{uuid_regexp}}}/member', FamilyMemberListView)
    app.router.add_view(f'/v1/family/{{family_uuid:{uuid_regexp}}}/member/token', FamilyMemberTokenView)
    app.router.add_view(f'/v1/family/{{family_uuid:{uuid_regexp}}}/member/{{member_uuid:{uuid_regexp}}}',
                        FamilyMemberView)
    app.router.add_view(f'/v1/family/{{family_uuid:{uuid_regexp}}}/baby/{{baby_uuid:{uuid_regexp}}}', BabyView)
    app.router.add_view(f'/v1/access/{{user_uuid:{uuid_regexp}}}/baby/{{baby_uuid:{uuid_regexp}}}', BabyAccessView)
