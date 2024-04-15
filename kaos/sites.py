from unfold.sites import UnfoldAdminSite

from .forms import LoginForm


class CustomAdminSite(UnfoldAdminSite):
    login_form = LoginForm


custom_admin_site = CustomAdminSite()
