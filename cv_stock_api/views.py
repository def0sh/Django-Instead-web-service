from rest_framework.viewsets import ModelViewSet
from cv_stock_api.permissions import IsOwnerAndAuthOrReadOnly
from cv_stock_api.serializers import ProjectSerializer, ProfileSerializer
from projects.models import Project
from users.models import Profile


class ProjectVieSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'title'
    permission_classes = (IsOwnerAndAuthOrReadOnly,)

    def get_object(self):
        return self.queryset.get(title__icontains=self.kwargs['title'])  # search case insensitive


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    permission_classes = (IsOwnerAndAuthOrReadOnly,)




