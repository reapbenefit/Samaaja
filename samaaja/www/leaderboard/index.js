frappe.ready(function() {
    // get_verified_users()
    
    reset_limit_and_start()
    get_city_wise_action_count_user_based()
    get_users(get_filters())
    $("#search").click(()=>{
        reset_limit_and_start()
        // $(".lb_content").empty()
        get_users(get_filters())
    })
    $("#rank-based-on").change(()=>{
        reset_limit_and_start()
        // $(".lb_content").empty()
        get_users(get_filters())
    })
    $("#rank-based-on-city").change(()=>{
        get_city_wise_action_count_user_based()
    })
    $("#clear").click(()=>{
        reset_limit_and_start()
        clear_filters()
        get_users()
    })
    $("#change_maker").keyup(function(event) {
        if (event.keyCode === 13) {
            $("#search").click();
        }
    });
    $("#btn_load_more").click(()=>{ 
        get_users(get_filters())
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
});

var get_filters = function() {
    // $("#btn_load_more").hide()
    return {
        "change_maker": $("#change_maker").val(),
        "organization": $("#organization").val(),
        "city": $("#city").val(),
        "hr_range": $("#hr-range").val(),
        "recent_rank_based_on": $("#rank-based-on").val(),
    }
};

var clear_filters = function() {
    $("#change_maker").val("")
    $("#organization").val("")
    $("#city").val("")
    $("#hr-range").val("")
    $("#btn_load_more").show()
    frappe.flags.start = 0;
}
var get_users = function(filters={}) {
    let rank_img = {
        1: "files/rank-1.png",
        2: "files/rank-2.png",
        3: "files/rank-3.png",
    }

    let org_based = 0
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("org")) {
        filters["organization"] = urlParams.get("org")
    }
    frappe.call({
        method: "samaaja.api.leaderboard.search_users_",
        args: {
                "filters": filters,
                "page_length": frappe.flags.leader_page_length,
                "start": frappe.flags.leader_start,
        },
        freeze: true,
        freeze_message: "...Searcing Users",
        callback: function(result) {
            let html = '';
            if (result.message.length > 0) {
                $("#btn_load_more").show()
                // let rrh = ["Last Month", "Last 15 Days"].includes(filters.recent_rank_based_on) ? "<div class='lb_col col_rank'>Recent Rank</div>" : "" 
                // if (lb_rows < 1) {
                //     html = `<div class="lb_row row_header">
                //         <div class="lb_col col_rank">Overall Rank</div>
                //         ${rrh}
                //         <div class="lb_col col_name">Name</div>
                //         <div class="lb_col col_city">City</div>
                //         <div class="lb_col col_hours">Hours</div>
                //         <div class="lb_col col_actions">Actions</div>
                //     </div>`
                // }
                result.message.forEach(leader => {
                    let rank = leader.rank ? leader.rank : "";
                    if (rank){
                        if(rank_img[rank]) {
                            rank = `<img src="${rank_img[rank]}" />`;
                        }
                    }
                    let city = leader.city ? leader.city : "";
                    let rr = leader.recent_rank ? leader.recent_rank : leader.rank;
                    let rrh = ["Last Month", "Last 15 Days"].includes(filters.recent_rank_based_on) ? `<div class="lb_col col_rank">${rr}</div>` : "" 
                    html = `
                        <div class="lb_row lb_row_result">
                            <div class="lb_col col_rank">${rank}</div>
                            ${rrh}
                            <div class="lb_col col_name"><a href="/user-profile/${leader.username}">${leader.full_name}</a></div>
                            <div class="lb_col col_city">${city}</div>
                            <div class="lb_col col_hours">${leader.hours_invested}</div>
                            <div class="lb_col col_actions">${leader.contribution_count}</div>
                        </div>
                    `
                    $(".lb_content").append(html)
                });
                // lb_rows = $('.lb_row').length
                frappe.flags.leader_page_length = 20
                frappe.flags.leader_start = $('.lb_row_result').length
            }
            
            else if(frappe.flags.leader_start == 0) {
                html=`<div class="container">
                    <div class="no-record">
                        No Record Found
                    </div>
                </div>`
                $(".lb_content").html(html)
                $("#btn_load_more").hide()
            }
            else {
                $("#btn_load_more").hide()
            }
            // $(".lb_content").append(html)
        }
    });
}

var get_city_wise_action_count_user_based = function() {
    frappe.call({
        method: "samaaja.api.leaderboard.get_city_wise_action_count_user_based",
        args: {
            "recent_rank_based_on": $("#rank-based-on-city").val(),
        },
        callback: function(result) {
            let html = '';

            if (result.message && result.message.length > 0) {
                result.message.forEach(r => {
                    html += `
                        <div class="ac_item_box">
                            <strong>${r.city}</strong>
                            <div class="progress_bar">
                                <div class="progress" style="width: ${r.percentage}%"></div>
                                <span>${r.action_count}</span>
                            </div>
                        </div>
                    `;
                });
            } else {
                html = "<p>No data available</p>";
            }

            $("#ac_list_item").html(html);
        },
        error: function(err) {
            console.error("API call failed:", err);
            $("#ac_list_item").html("<p>Failed to load data</p>");
        }
    });
};

var get_verified_users = function() {
    frappe.call({
        method: "samaaja.api.user.get_change_makers",
        args: {
                "verified": true,
                "page_length": frappe.flags.page_length,
                "start": frappe.flags.start,
        },
        freeze: true,
        freeze_message: "...Searcing Users",
        callback: function(result) {
            if (result.message?.length) {
                $(".vn_content").html("")
                result.message.forEach(user => {
                    let city = user.city ? `, ${user.city}`: ""
                    let html = `<div class="vn_box"><a href="${user.user_profile}"`;
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
                frappe.flags.start += $('.vn_box').length
            }
            // $(".lb_content").html(html)
        }
    });
}

var get_city_wise_action_count = function() {
    frappe.call({
        method: "samaaja.api.leaderboard.get_city_wise_action_count",
        callback: function(result) {
            if (result.message?.length) {
                let labels = result.message.map(obj => obj.city);
                let data = result.message.map(obj => obj.action_count);
                const ctx = document.getElementById('myChart').getContext('2d');
                const myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Action Taken',
                            data: data,
                            barThickness: 10,
                            backgroundColor: "#51A76A",
                            borderColor: "#51A76A",
                            borderWidth: 1
                        }]
                    },
                    options: {
                        plugins: {
                            legend: { display: false },
                            datalabels: {
                                anchor: 'end', // Position of the labels (start, end, center, etc.)
                                align: 'end', // Alignment of the labels (start, end, center, etc.)
                                color: 'blue', // Color of the labels
                                font: {
                                    weight: 'bold',
                                },
                                formatter: function (value, context) {
                                    return value; // Display the actual data value
                                }
                            }
                        },
                        indexAxis: 'y', // This makes the chart horizontal
                        scales: {
                            x: {
                                display: false,
                                beginAtZero: true,
                                grid: {
                                    display: false,
                                },
                                ticks: {
                                    display: false //this will remove only the label
                                }
                            },
                            y: {
                                // display: false,
                                grid: {
                                    display: false
                                },
                                ticks: {
                                    display: true //this will remove only the label
                                }
                            },
                        }
                    }
                });
            }
        }
    });
}

var setup_leaderboad_html = function(filters={}) {
	let html = '';
	let rrh = ["Last Month", "Last 15 Days"].includes(filters.recent_rank_based_on) ? "<div class='lb_col col_rank'>Recent Rank</div>" : "" 
	html = `<div class="lb_row row_header">
        <div class="lb_col col_rank">Overall Rank</div>
        ${rrh}
        <div class="lb_col col_name">Name</div>
        <div class="lb_col col_city">City</div>
        <div class="lb_col col_hours">Hours</div>
        <div class="lb_col col_actions">Actions</div>
    </div>`
    $(".lb_content").html(html)
	// $("#Ranktable").html(html)
}

// if (window.matchMedia('(max-width: 1023px)').matches) {
//     frappe.flags.page_length = 6;
// } else if (window.matchMedia('(max-width: 1241px)').matches){
//     frappe.flags.page_length = 8;
// } else {
//     frappe.flags.page_length = 10;
// }
// frappe.flags.start = 0;

var reset_limit_and_start = function(){
    setup_leaderboad_html(get_filters())
	frappe.flags.leader_page_length = 10
	frappe.flags.leader_start = 0
}