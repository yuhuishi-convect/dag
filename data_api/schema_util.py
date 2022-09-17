from .models import App


def generate_openapi_paths(url_prefix, resource_schema):
    """
    Generate openapi path (GET, POST, PUT, DELETE) definition for a jsonschema defined resource
    """
    resource_type = resource_schema["title"].lower()

    paths = {
        f"/{url_prefix}/{resource_type}/": {
            "get": {
                "summary": f"List {resource_type}",
                "description": f"List all {resource_type}",
                "operationId": f"list_{resource_type}",
                "parameters": [{"$ref": "#/components/parameters/dataset_id"}],
                "responses": {
                    "200": {
                        "description": f"List of {resource_type}",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": f"#/components/schemas/{resource_type}"
                                    },
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "summary": f"Create {resource_type}",
                "description": f"Create a new {resource_type}",
                "operationId": f"create_{resource_type}",
                "parameters": [
                    {"$ref": "#/components/parameters/app_id"},
                    {"$ref": "#/components/parameters/dataset_id"},
                ],
                "requestBody": {
                    "description": f"{resource_type} to create",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{resource_type}"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "201": {
                        "description": f"{resource_type} created",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": f"#/components/schemas/{resource_type}"
                                }
                            }
                        },
                    }
                },
            },
        },
        f"/{url_prefix}/{resource_type}/{{resource_id}}/": {
            "get": {
                "summary": f"Get {resource_type}",
                "description": f"Get a {resource_type}",
                "operationId": f"get_{resource_type}",
                "parameters": [
                    {
                        "name": "resource_id",
                        "in": "path",
                        "description": f"{resource_type} id",
                        "required": True,
                        "schema": {"type": "integer", "format": "int64"},
                    },
                    {"$ref": "#/components/parameters/dataset_id"},
                ],
                "responses": {
                    "200": {
                        "description": f"{resource_type} found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": f"#/components/schemas/{resource_type}"
                                }
                            }
                        },
                    }
                },
            },
            "put": {
                "summary": f"Update {resource_type}",
                "description": f"Update a {resource_type}",
                "operationId": f"update_{resource_type}",
                "parameters": [
                    {
                        "name": "resource_id",
                        "in": "path",
                        "description": f"{resource_type} id",
                        "required": True,
                        "schema": {"type": "integer", "format": "int64"},
                    },
                    {"$ref": "#/components/parameters/dataset_id"},
                ],
                "requestBody": {
                    "description": f"{resource_type} to update",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{resource_type}"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": f"{resource_type} updated",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": f"#/components/schemas/{resource_type}"
                                }
                            }
                        },
                    }
                },
            },
            "delete": {
                "summary": f"Delete {resource_type}",
                "description": f"Delete a {resource_type}",
                "operationId": f"delete_{resource_type}",
                "parameters": [
                    {
                        "name": "resource_id",
                        "in": "path",
                        "description": f"{resource_type} id",
                        "required": True,
                        "schema": {"type": "integer", "format": "int64"},
                    },
                    {"$ref": "#/components/parameters/dataset_id"},
                ],
                "responses": {"204": {"description": f"{resource_type} deleted"}},
            },
        },
    }
    return paths


def generate_openapi_schema_common_paths(url_prefix):
    """
    Generate GET, POST, PUT, DELETE for dataset resource
    """
    paths = {
        f"/{url_prefix}/datasets/": {
            "get": {
                "summary": "List dataset",
                "description": "List all dataset",
                "operationId": "list_dataset",
                "responses": {
                    "200": {
                        "description": "List of dataset",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/dataset"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "summary": "Create dataset",
                "description": "Create a new dataset",
                "operationId": "create_dataset",
                "requestBody": {
                    "description": "Dataset to create",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/dataset"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "201": {
                        "description": "Dataset created",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/dataset"}
                            }
                        },
                    }
                },
            },
        },
        f"/{url_prefix}/datasets/{{dataset_id}}/": {
            "get": {
                "summary": "Get dataset",
                "description": "Get a dataset",
                "operationId": "get_dataset",
                "parameters": [{"$ref": "#/components/parameters/dataset_id"}],
                "responses": {
                    "200": {
                        "description": "Dataset found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/dataset"}
                            }
                        },
                    }
                },
            },
            "put": {
                "summary": "Update dataset",
                "description": "Update a dataset",
                "operationId": "update_dataset",
                "parameters": [{"$ref": "#/components/parameters/dataset_id"}],
                "requestBody": {
                    "description": "Dataset to update",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/dataset"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Dataset updated",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/dataset"}
                            }
                        },
                    }
                },
            },
            "delete": {
                "summary": "Delete dataset",
                "description": "Delete a dataset",
                "operationId": "delete_dataset",
                "parameters": [{"$ref": "#/components/parameters/dataset_id"}],
                "responses": {"204": {"description": "Dataset deleted"}},
            },
        },
        f"/{url_prefix}/datasets/{{dataset_id}}/dump": {
            "get": {
                "summary": "Dump dataset",
                "description": "Dump a dataset",
                "operationId": "dump_dataset",
                "parameters": [
                    {"$ref": "#/components/parameters/dataset_id"},
                    # dump_type in query string, default to json. Can be json, xlsx
                    {
                        "name": "dump_type",
                        "in": "query",
                        "description": "Dump type",
                        "required": False,
                        "schema": {"type": "string", "enum": ["json", "xlsx"], "default": "json"},
                    }
                ]
            }
        }
    }
    return paths


def generate_openapi_schema_component(resource_schema):
    """
    Generate openapi schema component for a jsonschema defined resource
    """
    resource_type = resource_schema["title"].lower()
    return {resource_type: resource_schema}


def generate_openapi_parameters_component():
    """
    Generate openapi parameters component for a jsonschema defined resource
    """
    return {
        "dataset_id": {
            "name": "dataset_id",
            "in": "path",
            "description": "dataset id",
            "required": True,
            "schema": {"type": "integer", "format": "int64"},
        }
    }


def generate_openapi_schema_for_app(app_id):
    """
    Generate openapi schema for a given app
    """
    app = App.objects.get(id=app_id)
    url_prefix = f"api/apps/{app_id}/datasets/{{dataset_id}}"
    schemas = app.schemas
    paths = {}
    oas_schemas = {}
    common_paths = generate_openapi_schema_common_paths(url_prefix)
    for schema in schemas:
        resource_paths = generate_openapi_paths(url_prefix, schema)
        paths.update(resource_paths)

        oas_schema = generate_openapi_schema_component(schema)
        oas_schemas.update(oas_schema)

    paths.update(common_paths)

    # add Dataset schema to the oas_schemas
    oas_schemas.update(
        {
            "dataset": {
                "title": "Dataset",
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "format": "int64"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                },
            }
        }
    )

    components = {
        "parameters": generate_openapi_parameters_component(),
        "schemas": oas_schemas,
    }
    return {
        "openapi": "3.0.0",
        "info": {"title": f"{app.name} API", "version": "1.0.0"},
        "description": app.description,
        "paths": paths,
        "components": components,
    }
