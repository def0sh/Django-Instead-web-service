from django.db import models
from django.db import models
import uuid
from django.db.models import F
from django.utils.text import slugify
from users.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_delete


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(default='', null=False, unique=True, db_index=True)
    image = models.ImageField(null=True, blank=True, default="project_images/default.jpg", upload_to='project_images')
    description = models.TextField(null=True, blank=True)
    project_owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, related_name='owner')
    demo_link = models.CharField(max_length=500, null=True, blank=True)
    source_link = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    total_votes = models.PositiveIntegerField(default=0, null=True, blank=True)
    votes_ratio = models.PositiveIntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    @property
    def get_vote_count(self):
        proj_name = self.title
        proj_obj = Project.objects.get(title=proj_name)
        proj_q = Project.objects.filter(title=proj_name)
        Project.objects.filter(title=proj_name).update(total_votes=F('total_votes') + 1)
        total = Project.objects.get(title=proj_name).total_votes
        up_votes = proj_obj.review_set.all().filter(value='up').count()
        ratio = (up_votes / total) * 100
        proj_q.update(votes_ratio=ratio)
        return total, ratio  # return data for tests

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    def __str__(self):
        return self.title


class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, auto_created=True)
    VOTE_TYPE = (
        ('up', 'positive review'),
        ('down', 'negative review'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    body = models.TextField(blank=True, max_length=300, null=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


@receiver(post_delete, sender=Review)
def get_rating(sender, instance, **kwargs):
    if instance:
        proj_name = instance.project
        proj_obj = Project.objects.get(title=proj_name)
        if proj_obj.total_votes != 0:
            proj_obj.total_votes -= 1
            total = proj_obj.total_votes
            up_votes = Project.objects.get(title=proj_name).review_set.all().filter(value='up').count()
            try:
                ratio = (up_votes / total) * 100
                proj_obj.votes_ratio = ratio
            except:
                pass
            proj_obj.save()


