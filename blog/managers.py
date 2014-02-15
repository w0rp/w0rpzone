from django.db.models import Manager

class ArticleManager (Manager):
    def active_months(self):
        """
        Yield a queryset of all active article months as datetime objects,
        in descending order.
        """
        return (
            self.get_queryset()
            .filter(active= True)
            .datetimes("creation_date", "month", order="DESC")
        )

class CommenterManager (Manager):
    def create_for_ip(self, ip_address):
        """
        Return a model instance for a given IP address. The result of this
        function will be saved to the database if it does not yet exist.
        """
        commenter_list = tuple(
            self.get_queryset()
            .filter(ip_address= ip_address)
        )

        if len(commenter_list) > 0:
            return commenter_list[0]

        instance = self.model(ip_address= ip_address)
        instance.save()

        return instance

