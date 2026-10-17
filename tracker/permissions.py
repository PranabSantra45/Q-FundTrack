from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages


def get_user_profile(user):
    """Safely return UserProfile for authenticated user or None."""
    if not user or not user.is_authenticated:
        return None
    try:
        return user.profile
    except AttributeError:
        return None


def get_user_org(user):
    """Safely return Organization for authenticated user or None."""
    profile = get_user_profile(user)
    return profile.organization if profile else None


def check_org_access(obj, organization):
    """
    Verifies that the object belongs to the user's organization.
    Raises PermissionDenied (403) if there is an organization mismatch.
    """
    if not organization or not hasattr(obj, 'organization') or obj.organization != organization:
        raise PermissionDenied("Access Denied: You do not have permission to access records belonging to another organization.")


def login_required_org(view_func):
    """
    Decorator enforcing that user is authenticated and associated with an organization.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to access your organization dashboard.")
            return redirect('login')
        
        profile = get_user_profile(request.user)
        if not profile or not profile.organization:
            messages.error(request, "Your account is not assigned to an active organization.")
            return redirect('login')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def role_required(allowed_roles):
    """
    Decorator enforcing Role-Based Access Control (RBAC).
    allowed_roles: list of role strings, e.g. ['ORG_ADMIN', 'FINANCE']
    Superusers bypass role restrictions.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            profile = get_user_profile(request.user)
            if not profile or profile.role not in allowed_roles:
                raise PermissionDenied(f"Permission Denied: This action requires one of the following roles: {', '.join(allowed_roles)}")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
