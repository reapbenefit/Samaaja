from math import log, floor

def human_format(number):
	units = ['', 'K', 'M', 'G', 'T', 'P']
	k = 1000.0
	magnitude = int(floor(log(number, k)))
	return '%.2f%s' % (number / k**magnitude, units[magnitude])

def make_image_public(path):
    if path and "/private" in path:
        file = frappe.get_doc("File", {"file_url": path})
        file.is_private = 0
        file.save(ignore_permissions=True)
        return file.file_url
    return path