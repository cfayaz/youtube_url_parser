from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from youtubeRESTapp.parser import Parser


class MyRESTView(APIView):

    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kw):
        video_id = self.kwargs['video_id']       
        my_parser = Parser(video_id)
        result = my_parser.do_parse()        
        return Response(result)