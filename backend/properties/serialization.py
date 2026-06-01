from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Agent, Category, ContactMessage, Property, PropertyImage, Wishlist


class UserSummarySerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'display_name']
        read_only_fields = fields

    def get_display_name(self, obj):
        return obj.get_full_name() or obj.username


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AgentSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = ['id', 'user', 'phone', 'bio', 'photo', 'photo_url']
        read_only_fields = ['id', 'user', 'photo_url']

    def get_photo_url(self, obj):
        if not obj.photo:
            return None
        request = self.context.get('request')
        url = obj.photo.url
        return request.build_absolute_uri(url) if request else url


class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ['id', 'property', 'image', 'image_url', 'caption']
        read_only_fields = ['id', 'image_url']

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class PropertySerializer(serializers.ModelSerializer):
    owner = UserSummarySerializer(read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    amenities_list = serializers.SerializerMethodField()
    default_image_url = serializers.SerializerMethodField()
    is_in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id',
            'owner',
            'title',
            'description',
            'price',
            'location',
            'property_type',
            'listing_type',
            'bedrooms',
            'bathrooms',
            'area_sqft',
            'amenities',
            'amenities_list',
            'furnished',
            'is_featured',
            'approval_status',
            'status',
            'category',
            'category_detail',
            'images',
            'default_image_url',
            'is_in_wishlist',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'owner',
            'approval_status',
            'created_at',
            'updated_at',
        ]

    def get_amenities_list(self, obj):
        return obj.amenity_list()

    def get_default_image_url(self, obj):
        return obj.default_image_url()

    def get_is_in_wishlist(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Wishlist.objects.filter(user=request.user, property=obj).exists()


class WishlistSerializer(serializers.ModelSerializer):
    property_detail = PropertySerializer(source='property', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'property', 'property_detail', 'added_at']
        read_only_fields = ['id', 'added_at']

    def validate_property(self, value):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if Wishlist.objects.filter(user=request.user, property=value).exists():
                raise serializers.ValidationError('This property is already in your wishlist.')
        return value


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'property', 'name', 'email', 'phone', 'message', 'sent_at']
        read_only_fields = ['id', 'sent_at']
