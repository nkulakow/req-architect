from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
import MyServer.restHandlersHelpers
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# Views - they are really request handlers, byt Django has weird naming style


class ReqView(APIView):
    def __init__(self):
        self._serverInfo = MyServer.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ReqView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._getReqs(request)

    def post(self, request, *args, **kwargs):
        return self._addRequirement(request)

    def delete(self, request, *args, **kwargs):
        return self._deleteRequirement(request)

    def put(self, request, *args, **kwargs):
        return self._editRequirement(request)

    def _deleteRequirement(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to delete requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.deleteUserRequirement(request.DELETE.get("docId"), request.DELETE.get("reqId"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to delete requirement. Specified requirement does not exist or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _editRequirement(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to modify requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.editUserRequirement(request.PUT.get("docId"), request.PUT.get("reqId"), request.PUT.get("reqText"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to modify requirement. At least one of specified uids is invalid or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _addRequirement(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to add requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.addUserRequirement(request.POST.get("docId"), request.POST.get("reqNumberId"), request.POST.get("reqText"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to add requirement. Invalid document uid or invalid req number or could not build document tree.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _getReqs(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to get requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        reqs = MyServer.restHandlersHelpers.getDocReqs(
            request.GET.get("docId"), self._serverInfo["usersFolder"] + "/user")
        if not reqs:
            return JsonResponse([], safe=False)
        serialized = MyServer.restHandlersHelpers.serializeDocReqs(reqs)
        return JsonResponse(serialized, safe=False)


class DocView(APIView):
    def __init__(self):
        self._serverInfo = MyServer.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DocView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._getDocuments(request)

    def post(self, request, *args, **kwargs):
        return self._addDocument(request)

    def delete(self, request, *args, **kwargs):
        return self._deleteDocument(request)

    def _addDocument(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to add document. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.addUserDocument(request.POST.get("docId"), request.POST.get("parentId"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to add document. Could not build documents tree or root document exists and you need to specify the parent document.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _deleteDocument(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to delete document. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.deleteUserDocument(request.DELETE.get("docId"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to delete document. Specified document does not exist or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _getDocuments(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to get documents. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        serialized = MyServer.restHandlersHelpers.serializeDocuments(
            self._serverInfo["usersFolder"] + "/user")
        return JsonResponse(serialized, safe=False)


class LinkView(APIView):
    def __init__(self):
        self._serverInfo = MyServer.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")

    def put(self, request, *args, **kwargs):
        return self._addLink(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LinkView, self).dispatch(*args, **kwargs)

    def _addLink(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to link requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.addUserLink(request.PUT.get("req1Id"), request.PUT.get("req2Id"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to link requirements. At least one invalid requirement id or could not build document tree.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


class UnlinkView(APIView):
    def __init__(self):
        self._serverInfo = MyServer.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")

    def put(self, request, *args, **kwargs):
        return self._removeLink(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LinkView, self).dispatch(*args, **kwargs)

    def _removeLink(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to unlink requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.deleteUserLink(request.PUT.get("req1Id"), request.PUT.get("req2Id"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to unlink requirements. At least one invalid requirement id or could not build document tree.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


def seyHello(request) -> HttpResponse:
    """A simple hello world function to check if connection between the app and the server is correctly established"""
    return HttpResponse('Hello from backend')
