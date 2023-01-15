from rest_framework import serializers
from projects.models import Project, Tag
from users.models import Profile, Skill


class ProjectOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('project_owner',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name',)


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Project
        fields = ('title', 'slug', 'description')

    def to_representation(self, instance):
        data = super(ProjectSerializer, self).to_representation(instance)
        list_tags = [tag['name'] for tag in data['tags']]
        data['tags'] = list_tags
        return data


class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillsSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('username', 'email', 'intro', 'city', 'intro', 'bio', 'skills')

    def to_representation(self, instance):
        data = super(ProfileSerializer, self).to_representation(instance)
        list_skills = [skill['name'] for skill in data['skills']]
        data['skills'] = list_skills
        return data
