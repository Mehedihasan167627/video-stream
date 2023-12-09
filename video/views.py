from rest_framework.views import APIView
from rest_framework.response import Response
import mimetypes,os,re
from .models import Video
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

class VideoStreamAPIView(APIView):
    def get(self, request,video_id, *args, **kwargs):
        video_path =Video.objects.get(id=video_id).video_file.path   # Replace with the path to your video file
        start_time = float(request.GET.get('start_time', 0))
        
        if not os.path.exists(video_path):
            return Response({'error': 'Video not found'}, status=404)

        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        
        file_size = os.path.getsize(video_path)
        start_byte = 0
        end_byte = file_size - 1
        
        if range_match:
            start_byte = int(range_match.group(1))
            end_byte = int(range_match.group(2)) if range_match.group(2) else file_size - 1

        if start_time > 0:
            start_byte = int(start_time * file_size)

        chunk_size = 819234  # You can adjust the chunk size based on your requirements
        content_type, encoding = mimetypes.guess_type(video_path)
        content_type = content_type or 'application/octet-stream'

        file_wrapper = FileWrapper(open(video_path, 'rb'), chunk_size)

        response = StreamingHttpResponse(file_wrapper, content_type=content_type)
        response['Content-Length'] = str(end_byte - start_byte + 1)
        response['Content-Range'] = f'bytes {start_byte}-{end_byte}/{file_size}'
        response['Accept-Ranges'] = 'bytes'
        
        return response