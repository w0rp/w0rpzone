from django.db.models import Manager


class ArticleManager (Manager):
    def active_months(self):
        """
        Yield a queryset of all active article months as datetime objects,
        in descending order.
        """
        return (
            self.get_queryset()
            .filter(active=True)
            .datetimes("creation_date", "month", order="DESC")
        )
