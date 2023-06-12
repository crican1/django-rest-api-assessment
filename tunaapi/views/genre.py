from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, SongGenre

class GenreView(ViewSet):
    """Tuna genres view"""

    def retrieve (self, request, pk):
        """Handle GET requests for single genre"""
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]},
            status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all genres"""
        genre = Genre.objects.all()

        serializer = GenreSerializer(genre, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
    
        Returns
          Response -- JSON serialized genre instance
        """
        genre = Genre.objects.create(
          description=request.data["description"]
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a genre
        
        Returns -- Empty body with 204 status code
        """

        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]

        genre.save()

        return Response(None, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """Handle DELETE requests for a genre"""
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SongGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGenre
        fields = ( 'song_id', )
        depth = 1


class SongsGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for event"""
    song = SongGenreSerializer(many=True, read_only=True)
    song_count = serializers.SerializerMethodField()
    class Meta:
        model = SongGenre
        fields = ('id', 'description', 'song', 'song_count')
        depth = 2

    def get_song_count(self, obj):
        """To get the song count for a song"""
        return obj.song_count

class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for event"""
    class Meta:
        model = Genre
        fields = ('id' ,'description')
        depth=2
    