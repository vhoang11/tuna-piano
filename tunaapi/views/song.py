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
            serializer = SongSerializer(song, context={'request': request})
            return Response(serializer.data)
        except Artist.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        
        songs = Song.objects.all()
        
        # title = request.query_params.get('title', None)
        # if title is not None:
        #     songs = songs.filter(title=title)
            
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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
        
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        
        song = Song.objects.get(pk=pk)
        song.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
# class SongGenreSerializer(serializers.ModelSerializer):
#     """JSON serializer for genres"""

#     class Meta:
#         model = SongGenre
#         fields = ('genre_id')
#         depth = 1

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""

    artist = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'length', 'genres')
        
    def get_genres(self, obj):
      genres = obj.genres.all()
      return [{'id': genre.genre_id.id, 'description': genre.genre_id.description} for genre in genres]
  
    def get_artist(self, obj):
      artist = obj.artist_id
      return [{'id': artist.id, 'name': artist.name,'age': artist.age, 'bio': artist.bio}]
