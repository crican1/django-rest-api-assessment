"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song, SongGenre

class SongView(ViewSet):
    """Tuna songss view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single song"""
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all songs"""
        song = Song.objects.all()

        artist = request.query_params.get('id', None)
        if artist is not None:
            song = song.filter(artist_id=artist)

        genre = request.query_params.get('description', None)
        if genre is not None:
            genre = genre.filter(description=genre)

        serializer = SongSerializer(song, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized event instance
        """
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

        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.album = request.data["album"]
        song.length = request.data["length"]

        artist_id = Artist.objects.get(pk=request.data["artist_id"])
        song.artist_id = artist_id
        song.save()

        return Response(None, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """Handle DELETE requests for a song"""
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for Song Genre"""
    class Meta:
        model = SongGenre
        fields = ('genre_id', )
        depth = 2

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for song"""
    genre = SongGenreSerializer(many=True, read_only=True)
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length', 'genre')
        depth = 1
