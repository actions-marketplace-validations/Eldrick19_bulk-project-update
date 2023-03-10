#!/usr/bin/env python3

# Import the required modules
from src import helpers
import os

def main():
    # Read in input values
    if not os.environ.get("INPUT_TOKEN"):
        print("No token provided! 'token' is a required input.")
        exit(1)
    else:
        token = os.environ.get("INPUT_TOKEN")

    if not os.environ.get("INPUT_PROJECT-NUMBER"):
        print("No project number provided! 'project-number' is a required input.")
        exit(1)
    else:
        project_number = os.environ.get("INPUT_PROJECT-NUMBER")

    if not os.environ.get("INPUT_UPDATE-FIELD"):
        print("No update field provided! 'update-field' is a required input.")
        exit(1)
    else:
        update_field = os.environ.get("INPUT_UPDATE-FIELD")

    if not os.environ.get("INPUT_UPDATE-VALUE"):
        print("No update value provided! 'update-value' is a required input.")
        exit(1)
    else:
        update_value = os.environ.get("INPUT_UPDATE-VALUE")

    if not os.environ.get("INPUT_ORG"):
        org = os.environ.get("GITHUB_REPOSITORY_OWNER")
    else:
        org = os.environ.get("INPUT_ORG")

    filter_field = os.environ.get("INPUT_FILTER-FIELD")

    conditional = os.environ.get("INPUT_CONDITIONAL")

    filter_value = os.environ.get("INPUT_FILTER-VALUE")

    # Get the data from the project
    print('Fetching project data using the API...')
    project_id, data = helpers.get_project_data(
        org, 
        project_number, 
        token
    )
    
    # Apply filters (if they exist)
    item_ids, item_names = helpers.filter_items_to_update(
        data, 
        filter_field, 
        conditional, 
        filter_value
    )
    
    # Output to Actions Workflow
    # Commenting this out for now, in a future version we'll use this to output the items to update to the workflow or to a JSON file
    # name = 'items_to_update'
    # value = item_ids
    # with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    #     print(f'{name}={value}', file=fh)
    
    # Set up update data
    update = {
        "project_id": project_id,
        "field_id": helpers.get_filter_field_parameter(data, update_field, 'id'),
        "field_type": helpers.get_filter_field_parameter(data, update_field, 'dataType').lower(), # We need to convert to lower case for the GraphQL mutation, since the field type is all caps
    }

    # Set the update value. If the field type is a number, we won't need to wrap the value in quotes
    if update['field_type'] == 'number':
        update['field_value'] = update_value
    else:
        update['field_value'] = '"' + update_value + '"'

    # Loop through each item and update it
    print("Updating items...")
    for item in item_ids:
        update['item_id'] = item
        helpers.update_item(update, token)
    
    # Print success message
    if len(item_ids) == 0:
        print("No items to update! ?????????????")
    else:
        print("Successfully updated {} items! ???".format(len(item_ids)))
        print("Here are the items updated:")
        while len(item_ids) > 0:
            print(item_names.pop(0) + " (ID: " + item_ids.pop(0) + ")")

if __name__ == "__main__":
    main()