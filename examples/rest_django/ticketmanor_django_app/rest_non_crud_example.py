from rest_framework import views
from rest_framework.response import Response

class NewsView(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        email = request.DATA.get('news_type', None)  # access the deserialized posted data
        url = request.DATA.get('url', None)
        if email and url:
            self.share_url(email, url)
            return Response({"success": True})
        else:
            return Response({"success": False})

    def share_url(self, email, url):
        pass

# If your arbitrary code execution applies to a model object, but doesn't including retrieving
# or updating that model, simply inherit from the GenericAPIView instead the APIView and
# use the get_object method of the view.

# The one caveat when using APIView is to watch what permissions are applied to the view.
# Since it is not associated with a model, any permission that expects a model object to
# be available, like the DjangoModelPermission that is applied by default, will fail,
# so you should be explicit about permissions.
