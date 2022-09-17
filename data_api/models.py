from django.db import models


class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    schemas = models.JSONField(null=False, blank=False)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "schemas": self.schemas,
        }


class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="datasets")

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "app": self.app.pk,
        }


class Resource(models.Model):
    resource_type = models.CharField(max_length=100)
    dataset = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, related_name="resources"
    )
    value = models.JSONField(null=False, blank=False)

    def __str__(self):
        return f"{self.resource_type} - {self.value}"

    def to_json(self):
        return {
            "id": self.id,
            "resource_type": self.resource_type,
            "dataset": self.dataset.pk,
            "value": self.value,
        }
