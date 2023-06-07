"""View module for handling requests about songs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist


class SongView(ViewSet):
    """Tuna Piano song view"""

    def retrieve(self, request, pk):
        
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        
        songs = Song.objects.all()
        
        title = request.query_params.get('title', None)
        if title is not None:
            songs = songs.filter(title=title)
            
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        
        artist_id = Artist.objects.get(pk=request.data["artist_id"])
        
        song = Song.objects.create(
					title=request.data["title"],
					artist_id=artist_id,
					album=request.data["album"],
					length=request.data["length"],
        )
        
        serializer = SongSerializer(song)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a song

        Returns:
            Response -- Empty body with 204 status code
        """
        
        artist_id = Artist.objects.get(pk=request.data["artist_id"])
    
        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.artist_id = artist_id
        song.album = request.data["album"]
        song.length = request.data["length"]
        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        
        song = Song.objects.get(pk=pk)
        song.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs
    """
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length')
        depth = 1
