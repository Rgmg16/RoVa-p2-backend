from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser,Volunteer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('id','username', 'email', 'password', 'confirm_password', 'name', 'profile_image')
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data.get('name', ''),
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','name','username', 'email', 'name', 'profile_image')

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ('name', 'username', 'email', 'password', 'profile_image')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):
        # Ensure that username and email validations are only done if they are being updated
        if 'username' in data and CustomUser.objects.filter(username=data['username']).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})
        if 'email' in data and CustomUser.objects.filter(email=data['email']).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class VolunteerSerializer(serializers.ModelSerializer):
    creator_id = serializers.ReadOnlyField(source='user.id')  # Include creator's user ID
    creator_username = serializers.ReadOnlyField(source='user.username')  # Include creator's username

    class Meta:
        model = Volunteer
        fields = ['id', 'full_name', 'email', 'phone_number', 'age', 'id_number', 'description', 'profile_photo', 'creator_id', 'creator_username']  # Include creator_id and creator_username fields

    def create(self, validated_data):
        user = self.context['request'].user  # Get the user from the request context
        validated_data['user'] = user  # Set the user field separately
        volunteer = Volunteer.objects.create(**validated_data)
        return volunteer

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.age = validated_data.get('age', instance.age)
        instance.id_number = validated_data.get('id_number', instance.id_number)
        instance.description = validated_data.get('description', instance.description)
        profile_photo = validated_data.get('profile_photo', None)
        if profile_photo is not None:
            instance.profile_photo = profile_photo
        elif 'remove_profile_photo' in self.context['request'].data:
            instance.profile_photo = None
        instance.save()
        return instance