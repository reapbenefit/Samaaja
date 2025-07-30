frappe.ready(function() {
    $("#btn_load_more").click(()=>{ 
        get_users()
    })
    $("#clear").click(()=>{
        clear_filters()
        get_users()
    })
    $(".contribute-button").click(()=>{
        if (navigator.doNotTrack != 1 && !window.is_404) {
            let browser = frappe.utils.get_browser();
            frappe.call("frappe.website.doctype.web_page_view.web_page_view.make_view_log", {
                path: "contribute",
                referrer: null,
                browser: browser.name,
                version: browser.version,
                url: location.origin,
                user_tz: Intl.DateTimeFormat().resolvedOptions().timeZone
            })
        }
        window.open("http://wa.me/918095500118?text=cmp")
    })
    if ($('.vn_box').length == 0) {
        get_users()
    }
});

var get_users = function() {
    frappe.call({
        method: "samaaja.api.user.get_change_makers",
        args: {
                "verified": true,
                "page_length": frappe.flags.page_length,
                "start": frappe.flags.start,
        },
        freeze: true,
        freeze_message: "...Searching Users",
        callback: function(result) {
            if (result.message?.length) {
                result.message.forEach(user => {
                    let city = user.city ? `, ${user.city}`: ""
                    let html = `<div class="vn_box"><a href="${user.user_profile}">`;
                    if (user.user_image) {
                        html += `<div class="img_wrapper">
                                    <img src="${ user.user_image}" alt="" />
                                </div>`
                    }
                    else {
                        html += `<div class="user_avatar">
                            ${frappe.get_abbr(user.full_name)}
                        </div>`
                    }
                    html += `<div class="vn_box_content">
                            <p class="name">${ user.full_name } ${ city }</p>
                            <div class="vnb_stats">
                                <p class="vnb_focus">
                                    <span>Focus area:</span>
                                    <span><i>${ user.focus_area }</i></span>
                                </p>
                            </div>
                        </div>`
                    
                    if (user.verified_by) {
                        html += `<div class="verified_badge">
                                <svg id="Layer_1" data-name="Layer 1" viewBox="0 0 122.88 116.87"><polygon fill="#00ade9" points="61.37 8.24 80.43 0 90.88 17.79 111.15 22.32 109.15 42.85 122.88 58.43 109.2 73.87 111.15 94.55 91 99 80.43 116.87 61.51 108.62 42.45 116.87 32 99.08 11.73 94.55 13.73 74.01 0 58.43 13.68 42.99 11.73 22.32 31.88 17.87 42.45 0 61.37 8.24 61.37 8.24"></polygon><path fill="#ffffff" d="M37.92,65c-6.07-6.53,3.25-16.26,10-10.1,2.38,2.17,5.84,5.34,8.24,7.49L74.66,39.66C81.1,33,91.27,42.78,84.91,49.48L61.67,77.2a7.13,7.13,0,0,1-9.9.44C47.83,73.89,42.05,68.5,37.92,65Z"></path></svg>
                            </div>`
                    }
                    html += "</a></div>"
                    $(".vn_content").append(html)
                });
                frappe.flags.start = $('.vn_box').length
            }
            else {
                $(".vn_all").hide()
            }
            // $(".lb_content").html(html)
        }
    });
}
if (window.matchMedia('(max-width: 1023px)').matches) {
    frappe.flags.page_length = 6;
} else if (window.matchMedia('(max-width: 1241px)').matches){
    frappe.flags.page_length = 8;
} else {
    frappe.flags.page_length = 10;
}
frappe.flags.start = 0;