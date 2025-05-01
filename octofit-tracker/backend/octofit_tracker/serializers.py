from rest_framework import serializers
from bson import ObjectId
from .models import User, Team, Activity, Leaderboard, Workout

class ObjectIdSerializer(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, (list, tuple)):
            return [str(item) if isinstance(item, ObjectId) else item for item in value]
        if isinstance(value, ObjectId):
            return str(value)
        return value

    def to_internal_value(self, data):
        if isinstance(data, (list, tuple)):
            return [ObjectId(item) for item in data]
        return ObjectId(data)

class UserSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer()
    class Meta:
        model = User
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer()
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['_id', 'name', 'members']

class ActivitySerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ['_id', 'user', 'activity_type', 'duration', 'date']

class LeaderboardSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer()
    user = ObjectIdSerializer()
    class Meta:
        model = Leaderboard
        fields = '__all__'

class WorkoutSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer()
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Workout
        fields = '__all__'