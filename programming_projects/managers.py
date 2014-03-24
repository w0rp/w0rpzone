from django.db.models import Manager


class ProjectManager (Manager):
    def active_projects_for_user(self, user):
        """
        Return all active projects for a given user.
        """
        queryset = self.get_queryset().all()

        if not user.is_staff:
            queryset = queryset.filter(active=True)

        return queryset

    def load_project(self, user, slug):
        """
        Try to load a project. raise DoesNotExist if the project
        cannot be loaded.
        """
        return self.active_projects_for_user(user).get(slug=slug)
