from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Job, Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','password', 'email', 'is_employer']
        write_only_fields = ['password']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['posted_by', 'title', 'description', 'time_posted', 'num_applicants']
        read_only_fields = ['posted_by', 'time_posted']
    
    def create(self, validated_data):
        validated_data['posted_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_posted_by(self, obj):
        return obj.posted_by.email

    def __str__(self):
        return self.title


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.SerializerMethodField()
    listing = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['applicant', 'listing', 'cv', 'time_applied']
        read_only_fields = ['listing', 'applicant', 'time_applied']

    def create(self, validated_data):
        validated_data['applicant'] = self.context['request'].user
        return super().create(validated_data)

    def get_applicant(self, obj):
        return (
            f"Name: {obj.applicant.first_name} {obj.applicant.last_name}, Email: {obj.applicant.email}"
        )
    def get_listing(self, obj):
        return (
            f"Job Title: {obj.listing.title}, Posted By: {obj.listing.posted_by.email}"
        )

    def __str__(self):
        return f"Job Title: {self.job.title}, Applicant: {self.applicant}"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
    
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        data['user'] = user
        return data
