frappe.ready(function () {
  let originalType = null;
  let originalSubType = null;
  let isEditMode = false;
  let optionsLoaded = false;
  let formDataLoaded = false;

  // Function to check if we have form data loaded
  function checkFormDataLoaded() {
    // Try multiple ways to get the original values
    originalType = frappe.web_form.get_value("type") || 
                  (frappe.web_form.doc && frappe.web_form.doc.type) ||
                  (frappe.web_form.docname && frappe.web_form.values && frappe.web_form.values.type);
                  
    originalSubType = frappe.web_form.get_value("sub_type") || 
                     (frappe.web_form.doc && frappe.web_form.doc.sub_type) ||
                     (frappe.web_form.docname && frappe.web_form.values && frappe.web_form.values.sub_type);

    isEditMode = !!(frappe.web_form.docname || frappe.web_form.doc?.name || 
                   window.location.href.includes('edit') || 
                   document.querySelector('[data-docname]'));

    if (isEditMode && (originalType || originalSubType)) {
      formDataLoaded = true;
      trySetValues();
    }
    
    return formDataLoaded;
  }

  // Function to try setting values when both options and data are ready
  function trySetValues() {
    if (!optionsLoaded || !formDataLoaded) return;
    
    if (originalType) {
      // Try multiple approaches to set the type
      setTimeout(function() {
        frappe.web_form.set_value("type", originalType);
        frappe.web_form.fields_dict.type.set_input(originalType);
        
        // Trigger subtype loading
        if (originalSubType) {
          loadSubTypes(originalType, originalSubType);
        }
      }, 100);
    }
  }

  // Function to load type options
  function loadTypeOptions() {
    frappe.call({
      method: "frappe.client.get_list",
      args: {
        doctype: "Event Type",
        filters: {
          is_group: 1
        },
        fields: ["name"]
      },
      callback: function (r) {
        if (r.message) {
          const options = r.message.map(row => row.name);
          
          // Set options
          frappe.web_form.fields_dict.type.df.options = options;
          frappe.web_form.fields_dict.type.refresh();
          
          optionsLoaded = true;
          
          // Try to set values if form data is ready
          trySetValues();
        }
      }
    });
  }

  // Function to load subtypes
  function loadSubTypes(typeValue, selectedSubType = null) {
    if (!typeValue) return;
    
    frappe.call({
      method: "frappe.client.get_list",
      args: {
        doctype: "Event Type",
        filters: {
          parent_event_type: typeValue,
          is_group: 0
        },
        fields: ["name"]
      },
      callback: function (r) {
        const subOptions = r.message ? r.message.map(row => row.name) : [];
        
        // Set options
        frappe.web_form.fields_dict.sub_type.df.options = subOptions;
        frappe.web_form.fields_dict.sub_type.refresh();
        
        // Set the selected subtype if provided (for edit mode)
        if (selectedSubType && subOptions.includes(selectedSubType)) {
          setTimeout(function() {
            // Method 1: Direct set_value
            frappe.web_form.set_value("sub_type", selectedSubType);
            
            // Method 2: Set input directly
            frappe.web_form.fields_dict.sub_type.set_input(selectedSubType);
            
            // Method 3: Update the select element directly
            const subTypeSelect = document.querySelector('[data-fieldname="sub_type"] select');
            if (subTypeSelect) {
              subTypeSelect.value = selectedSubType;
              $(subTypeSelect).trigger('change');
            }
          }, 100);
        } else if (!selectedSubType) {
          frappe.web_form.set_value("sub_type", "");
        }
      }
    });
  }

  // Load subtypes when type is selected (user interaction)
  frappe.web_form.on('type', function (field, value) {
    if (!value) {
      frappe.web_form.fields_dict.sub_type.df.options = [];
      frappe.web_form.fields_dict.sub_type.refresh();
      frappe.web_form.set_value("sub_type", "");
      return;
    }

    // Don't clear subtype if we're in edit mode and this is the original type
    const shouldClearSubtype = !(isEditMode && value === originalType);
    loadSubTypes(value, shouldClearSubtype ? null : originalSubType);
  });

  // Multiple attempts to capture form data
  function initializeForm() {
    // Attempt 1: Immediate check
    checkFormDataLoaded();
    
    // Attempt 2: After short delay
    setTimeout(function() {
      checkFormDataLoaded();
      loadTypeOptions();
    }, 200);
    
    // Attempt 3: After longer delay
    setTimeout(function() {
      if (!formDataLoaded) {
        checkFormDataLoaded();
      }
      if (!optionsLoaded) {
        loadTypeOptions();
      }
    }, 1000);
    
    // Attempt 4: Check periodically for a few seconds
    let attempts = 0;
    const maxAttempts = 10;
    const checkInterval = setInterval(function() {
      attempts++;
      if (formDataLoaded && optionsLoaded) {
        clearInterval(checkInterval);
        return;
      }
      
      if (!formDataLoaded) {
        checkFormDataLoaded();
      }
      
      if (attempts >= maxAttempts) {
        clearInterval(checkInterval);
      }
    }, 500);
  }

  // Override the after_load event
  frappe.web_form.after_load = function() {
    setTimeout(function() {
      checkFormDataLoaded();
      if (optionsLoaded) {
        trySetValues();
      }
    }, 100);
  };

  // Start initialization
  initializeForm();

  // Validation before form submission
  frappe.web_form.validate = () => {
    let data = frappe.web_form.get_values();
    if (data.title && data.title.length > 70) {
      frappe.msgprint("Please restrict title to max 70 characters.");
      return false;
    }
    if (
      frappe.web_form.get_value("user") &&
      frappe.web_form.get_value("user") !== "Administrator" &&
      !frappe.utils.validate_type(frappe.web_form.get_value("user"), "email")
    ) {
      frappe.msgprint('Invalid email address');
      return false;
    }
    return true;
  };

  // Title input live validation
  frappe.web_form.on("title", (field, value) => {
    if (value && value.length > 70) {
      frappe.msgprint(
        `Please restrict the title to max 70 characters, <br> You've entered ${value.length} characters in the title`
      );
    }
  });

  // Set max length for title input
  $('*[data-fieldname="title"]').attr("maxlength", "70");

  // Show/hide fields based on user login
  if (frappe.session.user && frappe.session.user != "Guest") {
    frappe.web_form.set_value(["user"], frappe.session.user);
    frappe.web_form.set_df_property("user", "hidden", 1);
    frappe.web_form.set_df_property("anonymous", "hidden", 1);
  } else {
    frappe.web_form.set_df_property("user", "reqd", 1);
    frappe.web_form.on("anonymous", (field, checked) => {
      if (!checked) {
        frappe.web_form.set_value(["user"], "");
        frappe.web_form.set_df_property("user", "hidden", 0);
        frappe.web_form.set_df_property("user", "reqd", 1);
      } else {
        frappe.web_form.set_value(["user"], "");
        frappe.web_form.set_df_property("user", "hidden", 1);
        frappe.web_form.set_df_property("user", "reqd", 0);
      }
    });
    frappe.web_form.set_df_property("user", "hidden", 0);
  }

  // Default map position
  let defaultPosition = [22.1458, 80.0882];

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showMap, showMap);
  } else {
    showMap(null);
  }

  function showMap(position) {
    if (position && position.coords) {
      let lat = position.coords.latitude;
      let long = position.coords.longitude;
      defaultPosition = [lat, long];
    }

    const container = document.getElementById("map");
    if (container) {
      const screenWidth = window.screen.width;
      let mapZoom = screenWidth < 700 ? 4 : 5.4;

      let map = L.map("map").setView(defaultPosition, mapZoom);

      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution:
          '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(map);

      let allMarkers = [];

      // Show existing location marker if editing
      const existingLat = frappe.web_form.get_value("latitude");
      const existingLng = frappe.web_form.get_value("longitude");
      
      if (existingLat && existingLng) {
        let existingMarker = L.marker([existingLat, existingLng]).addTo(map);
        allMarkers.push(existingMarker);
        map.setView([existingLat, existingLng], mapZoom);
      } else {
        map.locate({
          setView: true,
        }).on("locationerror", function (e) {
          console.log(e);
        });
      }

      function onMapClick(e) {
        allMarkers.forEach(marker => map.removeLayer(marker));
        const latlng = e.latlng;

        frappe.web_form.set_value(["latitude"], latlng.lat);
        frappe.web_form.set_value(["longitude"], latlng.lng);

        let marker = L.marker([latlng.lat, latlng.lng]).addTo(map);
        allMarkers.push(marker);
      }

      map.on("click", onMapClick);
    }
  }
});