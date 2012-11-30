from flask import render_template
from auslib.admin.views.base import AdminView
from auslib.admin.base import db


class IndexPageView(AdminView):
    """/index.html"""
    def get(self):
        data = {
            'count_rules': db.rules.countRules(),
            'count_releases': db.releases.countReleases(),
            'count_users': db.permissions.countAllUsers(),
        }
        return render_template('index.html', **data)
