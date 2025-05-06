from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .publish import authenticate
def authenitcate (request):
        jwt_auth = JWTAuthentication()
        header = jwt_auth.get_header(request=request)
        if(header):
            token = jwt_auth.get_raw_token(header)
            if(token):
                response = authenticate(token)
                if response:
                    return response , token
                return None,None
            return None,None
        return None,None

class IsAuthenticated(permissions.BasePermission):


    def has_permission(self, request, view):
        user,_ = authenitcate(request)
        # user=None
        if( user):
            request.user = user
            return True
        return False

    def has_object_permission(self, request, view, obj):

        return True

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """

    def has_permission(self, request, view):
        user,_ = authenitcate(request)
        if(user and user.is_superuser):
            request.user = user
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True