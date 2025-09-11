# view/__init__.py
from view.layout import get_app_layout
from view.auth import get_login_layout, get_register_layout
from view.layout import get_home_layout, get_dashboard_layout, get_profile_layout
from view.admin import get_admin_layout, create_users_table
from view.projects import get_projects_layout, create_projects_table
from view.project_detail import get_project_detail_layout, create_member_list
from view.components import create_user_info_display
from view.navigation import get_navbar
from view.modals import (
    create_delete_user_modal, create_promote_user_modal,
    create_project_modal, create_add_member_modal, create_close_project_modal,
    create_delete_project_modal
)

# Re-export all necessary view functions to maintain compatibility with existing imports
__all__ = [
    'get_app_layout', 'get_navbar', 'get_login_layout', 'get_register_layout',
    'get_home_layout', 'get_dashboard_layout', 'get_profile_layout',
    'get_admin_layout', 'get_projects_layout', 'get_project_detail_layout',
    'create_user_info_display', 'create_users_table',
    'create_member_list', 'create_delete_user_modal', 'create_promote_user_modal',
    'create_project_modal', 'create_add_member_modal', 'create_close_project_modal',
    'create_delete_project_modal', 'create_projects_table'
]