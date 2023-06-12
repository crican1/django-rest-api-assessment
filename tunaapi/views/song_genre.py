"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre, Song, Genre

class SongGenreView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            songgenre = SongGenre.objects.get(pk=pk)
            serializer = SongGenreSerializer(songgenre)
            return Response(serializer.data)
        except SongGenre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        songgenre = SongGenre.objects.all()

        serializer = SongGenreSerializer(songgenre, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        song_id = Song.objects.get(pk=request.data["song_id"])
        genre_id = Genre.objects.get(pk=request.data["genre_id"])

        songgenre = SongGenre.objects.create(
            song_id=song_id,
            genre_id=genre_id,
        )

        serializer = SongGenreSerializer(songgenre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """Delete Artists
        """
        songgenre = SongGenre.objects.get(pk=pk)
        songgenre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class  SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = SongGenre
        fields = ('id', 'song_id', 'genre_id')
        depth = 2
