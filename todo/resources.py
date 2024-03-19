from import_export import resources
from .models import Reviews

class ReviewResource(resources.ModelResource):
    class Meta:
        model = Reviews
        