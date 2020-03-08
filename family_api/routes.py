from family_api.views.family_view import FamilyListView


def setup_routes(app):
    app.router.add_view('/v1/family', FamilyListView)
