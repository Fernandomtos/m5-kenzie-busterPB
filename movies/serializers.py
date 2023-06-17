from rest_framework import serializers
from .models import Rating_Choice, MovieOrder
from movies.models import Movie
from users.models import User


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(
        max_length=10, allow_null=True, default=None
    )
    rating = serializers.ChoiceField(
        choices=Rating_Choice,
        default=Rating_Choice.G,
        allow_null=True,
    )
    synopsis = serializers.CharField(allow_null=True, default=None)

    added_by = serializers.SerializerMethodField()

    def create(self, validated_data: dict) -> Movie:
        return Movie.objects.create(**validated_data)

    def get_added_by(self, obj: Movie):
        return obj.user.email


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="movie.id", read_only=True)
    title = serializers.CharField(source="movie.title", read_only=True)
    buyed_by = serializers.EmailField(source="order.email", read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data: dict) -> MovieOrder:
        return MovieOrder.objects.create(**validated_data)
