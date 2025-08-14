import frappe
from frappe.utils.safe_exec import check_safe_sql_query

def get_context(context):
    logger = frappe.logger("samaaja", allow_site=True, file_count=5)

    context.no_cache = 1
    
    samaaja_settings = frappe.get_cached_doc("Samaaja Settings")
    
    context.samaaja_settings = samaaja_settings
    
    # Users with most actions
    context.leaderboard_data = frappe.db.sql(
        """
        SELECT u.name, u.username, u.first_name, u.user_image, u.city as location, sum(e.hours_invested) as hours_invested, count(*) as total_actions from `tabUser` u 
        inner join `tabEvents` e on e.user = u.name where u.enabled = 1
        and DATE(e.creation) > current_date - interval %(day)s day
        group by u.name order by count(*) desc limit %(page_size)s;
        """,
        values={
            "page_size": 15 if samaaja_settings.leaderboard_page_size is None else samaaja_settings.leaderboard_page_size,
            "day": 60 if samaaja_settings.leaderboard_max_days is None else samaaja_settings.leaderboard_max_days
        },
        as_dict=1
    )

    # Top cities with most checkins
    context.top_cities = frappe.db.sql(
        """
        SELECT l.city, count(*) as count from `tabLocation` l inner join `tabEvents` e on e.location = l.name
        where DATE(e.creation) > current_date - interval %(day)s day
        and l.city is NOT NULL
        group by city order by count(*) desc limit %(page_length)s
        """,
        values={
            "page_length": 10 if samaaja_settings.top_cities_max_cities is None else samaaja_settings.top_cities_max_cities,
            "day": 60 if samaaja_settings.top_cities_max_days is None else samaaja_settings.top_cities_max_days
        },
        as_dict=1
    )
    context.first_city_action_count = context.top_cities[0]["count"] if len(context.top_cities) else 0
    
    # Recent actions with images
    context.recent_actions_with_images = frappe.db.sql(
        """ 
            SELECT e.name, e.creation, 
            CASE WHEN e.attachment1 is not null and e.attachment1 != '' THEN e.attachment1
            ELSE e.attachment2
            END as image
            , l.district, l.city from `tabEvents` e inner join `tabLocation` l on l.name = e.location 
            where (e.attachment1 is not null and e.attachment1 != '') OR (e.attachment2 is not null and e.attachment2 != '')  
            order by creation desc limit 10;
        """,
        as_dict=1
    )
    
    context.map_points = []
    map_points_query = frappe.db.get_single_value("Samaaja Settings", "map_stats_query")
    if map_points_query and check_safe_sql_query(map_points_query, throw=False):
        try:
            context.map_points = frappe.db.sql(map_points_query, as_dict=1)
        except Exception as e:
            logger.error("Invalid map points sql {0}".format(e))
    