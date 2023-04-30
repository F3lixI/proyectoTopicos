from django.db import models


class ToDo(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self) -> str:
        return f"{self.text}"