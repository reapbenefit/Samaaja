import frappe
import json
from samaaja.api.common import custom_response
from frappe.utils import flt

@frappe.whitelist()
def new():
    """
    Creates a new Location if it does not already exist based on latitude and longitude.
    If the location already exists, it returns the existing location.

    TODO: Implement deduplication logic to prevent multiple locations with the same coordinates.

    Returns:
        Response: A custom HTTP response containing the location data or an error message.
    """
    # Parse incoming data from the request
    location_data = json.loads(frappe.request.data)
    
    try:
        # Attempt to create or fetch the location
        loc_data = new_location(location_data)
        
        # Return success response with location data
        return custom_response(loc_data, 200)
    
    except Exception as e:
        # Rollback any changes if an error occurs
        frappe.db.rollback()
        
        # Return error response
        return custom_response(str(e), None, 500, True)


def new_location(location_data):
    """
    Creates a new Location or retrieves an existing one based on latitude and longitude.
    
    If a location with the same latitude and longitude already exists, it is returned.
    Otherwise, a new location is created and returned.

    Parameters:
        location_data (dict): The data containing latitude, longitude, and other location details.

    Returns:
        dict: A dictionary representing the location.
    """
    
    # Set precision for latitude and longitude
    precision = 9
    latitude = flt(location_data.get("latitude"), precision)
    longitude = flt(location_data.get("longitude"), precision)

    loc_name = None
    
    # Check if the location already exists
    if latitude and longitude:
        loc_name = frappe.db.exists(
            "Location",
            {
                "latitude": latitude,
                "longitude": longitude,
            },
        )

    if loc_name:
        # Location exists, fetch it and mark it as not new
        location = frappe.get_doc("Location", loc_name)
        location = location.as_dict()
        location["is_new"] = False
    else:
        # Location does not exist, create a new one
        location = frappe.get_doc(
            {
                "doctype": "Location",
                **location_data,
            }
        )
        location.insert(ignore_permissions=True)
        location = location.as_dict()
        location["is_new"] = True
    
    return location



@frappe.whitelist(allow_guest=True)
def get_districts(state):
    return frappe.get_all(
        "District",
        filters={"state": state},
        fields=["name", "district_name"],
        order_by="district_name asc"
    )

@frappe.whitelist(allow_guest=True)
def get_states():
    return frappe.get_all(
        "State",
        fields=["name", "state_name"],
        order_by="state_name asc"
    )