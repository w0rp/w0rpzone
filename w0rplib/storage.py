from pipeline.storage import PipelineMixin
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class Django2PipelineCachedStorage(PipelineMixin, ManifestStaticFilesStorage):
    pass
