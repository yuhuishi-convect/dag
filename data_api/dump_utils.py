from io import BytesIO

from openpyxl import Workbook

from .models import Dataset, Resource


def dump_to_json(dataset_id):
    """
    Convert all the resources under a dataset to json format.
    """
    dataset = Dataset.objects.get(id=dataset_id)
    resources = dataset.resources.all()

    # group the resources by resource type
    grouped_resources = {}
    for resource in resources:
        if resource.resource_type not in grouped_resources:
            grouped_resources[resource.resource_type] = []
        grouped_resources[resource.resource_type].append(resource.value)

    return grouped_resources


def dump_to_excel(dataset_id):
    """
    Convert all the resources under a dataset to an excel spreadsheet.
    With each resource type has its own sheet.
    All the resource records under one resource type correspond to rows under the sheet.
    """
    dataset = Dataset.objects.get(id=dataset_id)
    resources = dataset.resources.all()

    # group the resources by resource type
    grouped_resources = {}
    for resource in resources:
        if resource.resource_type not in grouped_resources:
            grouped_resources[resource.resource_type] = []
        grouped_resources[resource.resource_type].append(resource.value)

    # convert the grouped resources to excel
    workbook = Workbook()
    for resource_type in grouped_resources:
        # create a new sheet
        sheet = workbook.create_sheet(resource_type)
        # get the resource records
        resource_records = grouped_resources[resource_type]
        # write the header
        header = list(resource_records[0].keys())
        sheet.append(header)
        # write the records
        for record in resource_records:
            sheet.append(list(record.values()))

    # delete the default sheet
    workbook.remove(workbook["Sheet"])

    # write the workbook to a byteio
    byte_io = BytesIO()
    workbook.save(byte_io)
    byte_io.seek(0)

    return byte_io
