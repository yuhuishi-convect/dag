import json

import jsonschema
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from .dump_utils import dump_to_excel, dump_to_json
from .models import App, Dataset, Resource
from .schema_util import generate_openapi_schema_for_app


def create_app(request):
    """
    Take an json request with the app name and description and create a new app.
    Return the app in json format.
    """
    # convert the request body to json
    body = json.loads(request.body)
    # create a new app with the name and description from the request body
    app = App(
        name=body["name"], description=body["description"], schemas=body["schemas"]
    )
    app.save()
    return JsonResponse(app.to_json(), status=201)


@require_http_methods(["GET", "POST"])
def list_app(request):
    """
    Return a list of all apps in json format.
    """
    if request.method == "GET":
        apps = App.objects.all()
        apps_json = [app.to_json() for app in apps]
        return JsonResponse(apps_json, safe=False, status=200)
    elif request.method == "POST":
        return create_app(request)


@require_http_methods(["GET"])
def get_app(request, app_id):
    """
    Return a single app in json format.
    """
    app = App.objects.get(id=app_id)
    return JsonResponse(app.to_json(), status=200)


def create_dataset(request, app_id):
    """
    Take an json request with the dataset name and description and create a new dataset.
    Return the dataset in json format.
    """
    # convert the request body to json
    body = json.loads(request.body)
    # create a new dataset with the name and description from the request body
    dataset = Dataset(
        name=body["name"],
        description=body["description"],
        app=App.objects.get(id=app_id),
    )
    dataset.save()
    return JsonResponse(dataset.to_json(), status=201)


@require_http_methods(["GET", "POST"])
def list_dataset(request, app_id):
    """
    Return a list of all datasets in json format.
    """
    if request.method == "GET":
        datasets = Dataset.objects.filter(app=app_id)
        datasets_json = [dataset.to_json() for dataset in datasets]
        return JsonResponse(datasets_json, safe=False, status=200)
    elif request.method == "POST":
        return create_dataset(request, app_id)


def dump_dataset(request, app_id, dataset_id):
    """
    Return a single dataset in json format.
    """
    dataset = Dataset.objects.get(id=dataset_id)
    dump_type = request.GET.get("type", "json")

    if dump_type == "json":
        return JsonResponse(dump_to_json(dataset_id), status=200)
    elif dump_type == "xlsx":
        excel_bytes = dump_to_excel(dataset_id)
        # return the excel file as an attachment
        response = HttpResponse(
            excel_bytes,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response[
            "Content-Disposition"
        ] = f"attachment; filename=dataset_{dataset.id}.xlsx"
        return response
    return JsonResponse({"error": f"Invalid dump type {dump_type}"}, status=400)


def validate_resource_type(app_id, resource_type):
    # validate if the resource type is valid
    app = App.objects.get(id=app_id)
    schemas = app.schemas
    supported_resource_types = [r["title"].lower() for r in schemas]
    if resource_type not in supported_resource_types:
        raise Exception(
            f"Resource type not supported. Supported resource types: {supported_resource_types}"
        )


def validate_resource_value(app_id, resource_type, value):
    # validate if the resource type is valid
    app = App.objects.get(id=app_id)
    schemas = app.schemas
    resource_schema = [r for r in schemas if r["title"].lower() == resource_type][0]
    supported_resource_types = [r["title"].lower() for r in schemas]
    if not resource_schema:
        raise Exception(
            f"Resource type not supported. Supported resource types: {supported_resource_types}"
        )
    try:
        jsonschema.validate(value, resource_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise e


def get_resource(request, app_id, dataset_id, resource_type, resource_id):
    """
    Return a single resource in json format.
    """
    resource = Resource.objects.get(id=resource_id, resource_type=resource_type)
    return JsonResponse(resource.to_json(), status=200)


def create_resource(request, app_id, dataset_id, resource_type):
    """
    Take an json request with the resource type and value and create a new resource.
    Return the resource in json format.
    """
    # convert the request body to json
    body = json.loads(request.body)

    # validate if the resource value is valid
    value = body
    try:
        validate_resource_type(app_id, resource_type)
        validate_resource_value(app_id, resource_type, value)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    # create a new resource with the type and value from the request body
    dataset = Dataset.objects.get(id=dataset_id)
    resource = Resource(resource_type=resource_type, value=value, dataset=dataset)
    resource.save()
    return JsonResponse(resource.to_json(), status=201)


def update_resource(request, app_id, dataset_id, resource_type, resource_id):
    """
    Take an json request with the resource type and value and update the resource.
    Return the resource in json format.
    """
    # convert the request body to json
    body = json.loads(request.body)
    value = body
    # update the resource with the type and value from the request body
    resource = Resource.objects.get(id=resource_id, resource_type=resource_type)
    resource.resource_type = resource_type
    try:
        validate_resource_value(app_id, resource_type, value)
    except Exception as e:
        return JsonResponse({"error": e.message}, status=400)
    resource.value = value
    resource.save()
    # return a resource updated response
    return JsonResponse(resource.to_json(), status=200)


def delete_resource(request, app_id, dataset_id, resource_type, resource_id):
    """
    Delete the resource.
    Return the resource in json format.
    """
    # delete the resource
    resource = Resource.objects.get(id=resource_id, resource_type=resource_type)
    resource.delete()
    # return a no content response
    return JsonResponse({}, status=204)


def list_resource(request, app_id, dataset_id, resource_type):
    """
    Return a list of all resources in json format.
    """
    print(app_id, dataset_id, resource_type)
    resources = Resource.objects.filter(dataset=dataset_id, resource_type=resource_type)
    resources_json = [resource.to_json() for resource in resources]
    return JsonResponse(resources_json, safe=False, status=200)


@require_http_methods(["GET", "POST"])
def resource_gateway(request, app_id, dataset_id, resource_type):
    """
    This methods serves as the gateway to the resource methods.
    """
    # validate if the resource type is valid
    try:
        validate_resource_type(app_id, resource_type)
    except Exception as e:
        return JsonResponse({"error": e.message}, status=400)

    if request.method == "GET":
        return list_resource(request, app_id, dataset_id, resource_type)
    elif request.method == "POST":
        return create_resource(request, app_id, dataset_id, resource_type)


@require_http_methods(["GET", "PUT", "DELETE"])
def resource_detail_gateway(request, app_id, dataset_id, resource_type, resource_id):
    """
    This methods serves as the gateway to the resource detail methods.
    """
    try:
        validate_resource_type(app_id, resource_type)
    except Exception as e:
        return JsonResponse({"error": e.message}, status=400)

    if request.method == "GET":
        return get_resource(request, app_id, dataset_id, resource_type, resource_id)
    elif request.method == "PUT":
        return update_resource(request, app_id, dataset_id, resource_type, resource_id)
    elif request.method == "DELETE":
        return delete_resource(request, app_id, dataset_id, resource_type, resource_id)


@require_http_methods(["GET"])
def openapi(request, app_id):
    """
    Return the openapi schema.
    """
    openapi_schema = generate_openapi_schema_for_app(app_id)
    return JsonResponse(openapi_schema, status=200)


def render_swagger(request, app_id):
    """
    Render the swagger ui.
    """
    app_schema_url = reverse_lazy("openapi_schema", kwargs={"app_id": app_id})
    return render(request, "swagger.html", {"schema_url": app_schema_url})
