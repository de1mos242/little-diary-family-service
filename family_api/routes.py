from family_api.views.family_member_view import FamilyMemberListView, FamilyMemberTokenView
from family_api.views.family_view import FamilyListView, FamilyView


def setup_routes(app):
    app.router.add_view('/v1/family', FamilyListView)
    app.router.add_view(r'/v1/family/{family_id:\d+}', FamilyView)
    app.router.add_view(r'/v1/family/{family_id:\d+}/member', FamilyMemberListView)
    app.router.add_view(r'/v1/family/{family_id:\d+}/member/token', FamilyMemberTokenView)
