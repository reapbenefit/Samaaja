// www/campaign/index.js
frappe.ready(function() {
	console.log('Campaign petition page loaded');
  // 1) Initialize Quill
  const quill = new Quill('#editor-container', {
	theme: 'snow',
	modules: {
	  toolbar: [
		[{ 'header': [1, 2, 3, false] }],
		['bold', 'italic', 'underline', 'strike'],
		[{ 'color': [] }, { 'background': [] }],
		[{ 'script': 'sub'}, { 'script': 'super' }],
		[{ 'list': 'ordered'}, { 'list': 'bullet' }],
		[{ 'indent': '-1'}, { 'indent': '+1' }],
		[{ 'align': [] }],
		['blockquote', 'code-block'],
		['link', 'image'],
		['clean']
	  ]
	}
  });

  const toolbar = quill.getModule('toolbar');

toolbar.addHandler('image', () => {
	if (typeof window.__ !== "function") {
	window.__ = (text) => text;
}

// Inject __ into Vue prototype so Vue components like FileUploader can access it
if (typeof Vue !== "undefined" && typeof Vue.prototype.__ !== "function") {
	Vue.prototype.__ = window.__;
}
	new frappe.ui.FileUploader({
		allow_multiple: false,
		disable_file_browser: true,
		restrictions: {
			allowed_file_types: ['image/*'],
		},
		values: {
			is_private: 0
		},
		on_success(file) {
			if (file && file.file_url) {
				const range = quill.getSelection(true);
				// Construct absolute URL
				const image_url = window.location.origin + file.file_url;
				quill.insertEmbed(range.index, 'image', image_url);
				quill.setSelection(range.index + 1);
			}
		},
	});
});

  // 2) Email‐validation helper
  function validateEmail(email) {
	return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  // 3) Submit handler
  function submitPetition() {
	// clear errors
	document.querySelectorAll('.error').forEach(el => el.style.display = 'none');

	const subject = document.querySelector('[name="subject"]');
	const email   = document.querySelector('[name="email"]');
	const town    = document.querySelector('[name="town"]');
	const messageContent = quill.getText().trim();

	let hasError = false;

	if (!subject.value.trim()) {
	  subject.closest('.form_item').querySelector('.error').style.display = 'block';
	  hasError = true;
	}
	if (!email.value.trim() || !validateEmail(email.value)) {
	  email.closest('.form_item').querySelector('.error').style.display = 'block';
	  hasError = true;
	}
	if (!town.value.trim()) {
	  town.closest('.form_item').querySelector('.error').style.display = 'block';
	  hasError = true;
	}
	if (!messageContent) {
		document.getElementById('message-error').style.display = 'block';
		hasError = true;
	}
	if (hasError) return;

	// dump Quill HTML into hidden field
	document.getElementById('message_body').value = quill.root.innerHTML;

	// build payload
	let payload = {
	  campaign:       document.querySelector('.campaign_email_wrapper').dataset.name, // you can set this global via a data-attr
	  subject:        subject.value,
	  message_body:   document.getElementById('message_body').value,
	  first_name:     document.querySelector('[name="first_name"]').value,
	  last_name:      document.querySelector('[name="last_name"]').value,
	  email:          email.value,
	  address_line_1: document.querySelector('[name="address_line_1"]').value,
	  town:           town.value,
	  pincode:        document.querySelector('[name="pincode"]').value,
	  recipients:     Array.from(document.querySelectorAll('[name="recipients"]:checked'))
						   .map(el => ({ recipient: el.value }))
	};

	frappe.call({
	  method:        'samaaja.api.campaign.submit_campaign_petition',
	  args:          { data: payload },
	  freeze:        true,
	  freeze_message:'Submitting your petition...',
	  callback(r) {
		if (r.message === 'ok') {
		  	frappe.msgprint({ message: 'Petition submitted successfully!', title: 'Success', indicator: 'green' });
			setTimeout(() => {
				window.location.href = '/leaderboard';
			}, 5000);
		} else {
		  frappe.msgprint('Error submitting petition.');
		}
	  },
	  error() {
		frappe.msgprint('Server error occurred.');
	  }
	});
  }

  // 4) Wire up the button
  document.querySelector('#submit').addEventListener('click', submitPetition);
});
