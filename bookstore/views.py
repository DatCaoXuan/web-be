from django.http import FileResponse
from rest_framework import viewsets, renderers
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser, MultiPartParser
from wsgiref.util import FileWrapper
import mimetypes, os
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from bookstore.utils import APICode

class PassthroughRenderer(renderers.BaseRenderer):
    media_type = ''
    format = ''
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class MediaViewSet(viewsets.ReadOnlyModelViewSet):
	parser_classes = (MultiPartParser, )
	permission_classes = [AllowAny, ]

	@extend_schema(
		summary='Download a file', 
		parameters=[
			OpenApiParameter(name='file', description='File path', type=str),
		]
	)
	@action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
	def download(self, request):
		file_name = request.GET.get('file')
        
		if not file_name:
			return Response({
				'code': APICode.REQUEST_FAIL,
				'message': 'Request failed',
			}, status=status.HTTP_400_BAD_REQUEST)

		file_name = file_name[len(settings.MEDIA_URL):]
		file_path = f'{settings.MEDIA_ROOT}\{file_name}'.replace('/', '\\')
		file_wrapper = FileWrapper(open(file_path, 'rb'))
		file_mimetype = mimetypes.guess_type(file_name)

		response = FileResponse(file_wrapper, content_type=file_mimetype)
		response['X-Sendfile'] = file_path
		response['Content-Length'] = os.stat(file_path).st_size
		response['Content-Disposition'] = f'attachment; filename={file_name}'

		return response
	
	extend_schema(
        request={
			'multipart/form-data': {
				'type': 'object',
				'properties': {
					'file': {
						'type': 'string',
						'format': 'binary'
					}
				}
			}
		},
    )
	def upload(self, request):
		try:
			path = request.data['path']
			path = path.strip('/') + ('/' if path else '')

			sys_path = path.replace('/', '\\')
			up_file = request.FILES['file']
			destination = open(f'{settings.MEDIA_ROOT}\\{sys_path}{up_file.name}', 'wb+')
			for chunk in up_file.chunks():
				destination.write(chunk)
			destination.close()

			return Response({
				'code': APICode.RESOURCE_CREATED,
				'message': 'Uploaded file',
				'data': f'{settings.MEDIA_URL}{path}{up_file.name}',
			}, status=status.HTTP_201_CREATED)
		except Exception as e:
			print(e)
			return Response({
				'code': APICode.REQUEST_FAIL,
				'message': 'Request failed',
			}, status=status.HTTP_400_BAD_REQUEST)