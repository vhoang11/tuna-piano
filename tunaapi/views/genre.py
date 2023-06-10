"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, SongGenre
from django.db.models import Count

class GenreView(ViewSet):
    """Tuna Piano genre view"""

    def retrieve(self, request, pk):
        
        try:
            genre = Genre.objects.annotate(song_count=Count('songs')).get(pk=pk)
            serializer = SongsGenreSerializer(genre)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        
        genre = Genre.objects.annotate(song_count=Count('songs')).all()
            
        serializer = SongsGenreSerializer(genre, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        
        genre = Genre.objects.create(
					description=request.data["description"],
        )
        
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a genre

        Returns:
            Response -- Empty body with 204 status code
        """
    
        genre = Genre.objects.annotate(song_count=Count('songs')).get(pk=pk)
        genre.description = request.data["description"]
        genre.save()
        
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def popular_genres(self, request):
        """
        Retrieve a list of popular genres based on the number of songs associated with each genre
        """
        
        genres = Genre.objects.annotate(song_count=Count('songs')).order_by('-song_count')[:1]

        serializer = SongsgitGenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class SongGenreSerializer(serializers.ModelSerializer):
  class Meta:
      model = SongGenre
      fields = ( 'song_id', )
      depth = 1
      
class SongsGenreSerializer(serializers.ModelSerializer):
  """JSON serializer for genres"""
  songs = SongGenreSerializer(many=True, read_only=True)
  song_count = serializers.SerializerMethodField()
  
  class Meta:
      model = Genre
      fields = ('id', 'description', 'songs', 'song_count')
      depth = 2
      
  def get_song_count(self, obj):
        return obj.song_count

class GenreSerializer(serializers.ModelSerializer):
  """JSON serializer for genres"""
  songs = SongGenreSerializer(many=True, read_only=True)
  
  class Meta:
      model = Genre
      fields = ('id', 'description', 'songs')
      depth = 2
