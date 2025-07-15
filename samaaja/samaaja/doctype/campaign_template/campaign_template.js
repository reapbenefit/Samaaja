// Copyright (c) 2025, FOSS United and contributors
// For license information, please see license.txt

frappe.ui.form.on('Campaign Template', {
	refresh: function(frm) {
		frm.trigger("setup_example_message");
	},
	validate: function (frm) {
		if (frm.doc.title && !frm.doc.route) {
			frm.set_value("route", "campaign/" + frappe.scrub(frm.doc.title, "-"));
		}
	},
	setup_example_message: function (frm) {
	const template = `<h5>Thank You Email Example</h5>
<pre>
Subject: Thank you for signing the {{ doc.campaign }} petition, {{ doc.first_name }}!

Dear {{ doc.first_name }} {{ doc.last_name }},

Thank you for supporting the {{ doc.campaign }} campaign.

Subject: {{ doc.subject }}

Your message:
----------------------
{{ doc.message_body }}
----------------------

Your Address:
{{ doc.address_line_1 }}, {{ doc.town }} - {{ doc.pincode }}

Your Email: {{ doc.email }}
First Name: {{ doc.first_name }}
Last Name: {{ doc.last_name }}

Selected Recipients Table (Count): {{ doc.recipients | length }}

{% if doc.recipients %}
Recipients:
{% for row in doc.recipients %}
- {{ row.recipient_name }} ({{ row.email }})
{% endfor %}
{% endif %}

Warm regards,
Samaaja Team
</pre>
`;
	frm.get_field("message_examples").$wrapper.html(template);
},

});