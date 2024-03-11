from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .publish import auth
def authenitcate (request):
        jwt_auth = JWTAuthentication()
        header = jwt_auth.get_header(request=request)
        token = jwt_auth.get_raw_token(header)
        response =auth(token,'verify','commerce')
        if response:
            response = response
            user= response['user']
            token = response ['token']
            return user , token
        return None,None

class IsAuthenticatedM(permissions.BasePermission):

    # edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        user,token = authenitcate(request)
        if( user):
            request.user = user
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # if request.user.is_superuser:
        #     return True

        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # if obj.author == request.user:
        #     return True

        # if request.user.is_staff and request.method not in self.edit_methods:
        #     return True

        return True