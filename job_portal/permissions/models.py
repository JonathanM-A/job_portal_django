from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from api.models import Job, Application

def create_groups_and_permissions():
    job_content_type = ContentType.objects.get_for_model(Job)
    application_content_type = ContentType.objects.get_for_model(Application)

    employers_group = Group.objects.get_or_create(name="Employers")[0]
    job_seekers_group = Group.objects.get_or_create(name="JobSeekers")[0]

    Permission.objects.get_or_create(codename="post_a_job", name="Can post a job", content_type=job_content_type)
    Permission.objects.get_or_create(codename="apply_for_job", name="Can apply for a job", content_type = application_content_type)

    employers_group.permissions.add(Permission.objects.get(codename="post_a_job"))
    job_seekers_group.permissions.add(Permission.objects.get(codename="apply_for_job"))
