from rest_framework import serializers

from .models import GlobalCategory


class GlobalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalCategory
        fields = "__all__"
