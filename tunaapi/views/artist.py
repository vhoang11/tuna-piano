"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist


class ArtistView(ViewSet):
    """Tuna Piano artist view"""

    def retrieve(self, request, pk):
        
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        
        artists = Artist.objects.all()
        
        name = request.query_params.get('name', None)
        if name is not None:
            artists = artists.filter(name=name)
            
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        
        artist = Artist.objects.create(
					name=request.data["name"],
					age=request.data["age"],
					bio=request.data["bio"],
        )
        
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for an artist

        Returns:
            Response -- Empty body with 204 status code
        """

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]
        artist.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')
        depth = 1
