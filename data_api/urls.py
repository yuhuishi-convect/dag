from django.urls import path

from . import views

urlpatterns = [
    path("apps/", views.list_app, name="list_app"),
    path("apps/<int:app_id>/", views.get_app, name="get_app"),
    path("apps/<int:app_id>/schema", views.openapi, name="openapi_schema"),
    path("apps/<int:app_id>/swagger", views.render_swagger, name="swagger"),
    path("apps/<int:app_id>/datasets/", views.list_dataset, name="list_dataset"),
    path(
        "apps/<int:app_id>/datasets/<int:dataset_id>/dump",
        views.dump_dataset,
        name="dump_dataset",
    ),
    path(
        "apps/<int:app_id>/datasets/<int:dataset_id>/<str:resource_type>/<int:resource_id>",
        views.resource_detail_gateway,
        name="list_resource",
    ),
    path(
        "apps/<int:app_id>/datasets/<int:dataset_id>/<str:resource_type>/",
        views.resource_gateway,
        name="list_resource",
    ),
]
