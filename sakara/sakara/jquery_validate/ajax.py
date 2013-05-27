from rest_framework.views import APIView
from rest_framework.response import Response


class AjaxView(APIView):
    def ajax_response(self, flag, message):
        return Response({'success': flag, 'message': message})
