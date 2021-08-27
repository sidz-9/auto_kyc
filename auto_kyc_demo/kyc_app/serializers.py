from rest_framework import serializers
from .models import user_details, pan_db

class user_detailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_details
        # fields = ('first_name', 'last_name')
        fields = '__all__'

class pan_dbSerializer(serializers.ModelSerializer):

    class Meta:
        model = pan_db
        # fields = ('first_name', 'last_name')
        fields = '__all__'