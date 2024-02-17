function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$.fn.extend({
    loader: function() {
        return this.each(function() {
            $(this).attr("org-text", $(this).text())
            this.innerHTML = "<img class='loader' src='/static/images/loader-white.gif'>";
        })
    },
    clear: function() {
        return this.each(function() {
            this.innerHTML = $(this).attr("org-text")
        })
    }
})
$(function() {
    $(".border-slider").each(function() {
        const slider = $(this);
        const lis = $(this).find("li:not(.active-border)");
        const border = $(this).find(".active-border");
        const padding = $(lis[0]).css("padding").split(" ")[1].slice(0, -2)
        function getLiWidth(li) {
            return $(li).width() + (padding * 2)
        }
        border.css("width", getLiWidth(lis[0]));
        $(lis).on("click", function(e) {
            $(lis).removeClass("active");
            $(this).addClass("active");
            border.animate({
                "width": getLiWidth(e.target),
                "left": -($(slider).offset().left - $(e.target).offset().left)
            }, 200)
        }) 
    });
    $(".list .dropdown-btn").click(function() {
        const item = $(this).parents("li");
        const dropdownList = $(item).find(".list-dropdown")
        $(dropdownList).toggle();
        $(dropdownList).parent().toggleClass("dropdown-indicator")
    })
})

class Modal {
    constructor(id) {
        this.id = id;
        const dom = $("#" + id);
        this.dom = $("#" + id);
        this.dom.find(".modal-bg, .modal-close").on("click", function() {
            dom.removeClass("open");
        })
    }
    show() {
        this.dom.toggleClass("open")
    }
    close() {
        this.dom.removeClass("open")
    }
}

class Alert {
    constructor(id = "alert") {
        this.dom = $("#" + id);
        this.text = this.dom.find("p");
        const el = this;
        this.dom.find(".hide-alert").on("click", function() {
            el.close();
        })
        this.interval;
    }
    show(type, text, time = 5000) {
        clearInterval(this.interval);
        this.dom.addClass("alert-" + type);
        this.text.html(text)
        this.dom.addClass("open")
        const ob = this;
        this.interval = setInterval(function() {
           ob.close() 
        }, time)
    }
    close() {
        this.dom.removeClass("open").removeClass("alert-notice").removeClass("alert-error")
    }
}

class Notice {
    constructor(id) {
        this.dom = $("#" + id);
    }
    show(text) {
        this.dom.css({
            "bottom": "25px",
            "opacity": "1"
        }).find("p").html(text);
        setTimeout(() => {
            this.hide();
        }, 4000)
    }
    error(text) {
        this.dom.addClass("notice-red");
        this.show(text);
    }
    hide(remove = false) {
        let css = {
            "opacity": "0"
        }
        if(remove) {
            css["bottom"] = "-250px";
        } else {
            setTimeout(() => {
                this.hide(true);
            }, 300)
        }
        this.dom.css(css).removeClass("notice-red");
    }
}
function session_request(url, type, data={}, success=function(){}, error=function(){}) {
    const token = getCookie("csrftoken");
    $.ajax({
        url: url,
        type: type,
        headers: {
            "X-CSRFToken": token
        },
        data: data,
        success: function(data) {
            success(data)
        },
        error: function(data) {
            error(data)
        }
    })
}
class User {
    static create_organization(data, success=function(){}, error=function(){}) {
        session_request("/api/user/organizations", "POST", data, success, error);
    }
    static get_organizations(success, error) {
        session_request("/api/user/organizations", "GET", {}, success, error)
    }
    static cancel_purchase(id, success, error) {
        session_request("/api/user/purchases/" + id, "DELETE", {}, success, error)
    }
}

class Permissions {
    static get_all(success=function(){}, error=function(){}) {
        session_request("/api/permissions/", "GET", "", success, error)
    }
}

class Organization {
    static create_app(data, success=function(){}, error=function(){}) {
        session_request("/api/organization/apps", "POST", data, success, error)
    }
    static get_apps(success=function(){}, error=function(){}) {
        session_request("/api/organization/apps", "GET", "", success, error)
    }
    static get_users(order="", success=function(){}, error=function(){}) {
        session_request("/api/organization/users?order=" + order, "GET", "", success, error)
    }
    static add_user(email, success=function(){}, error=function(){}) {
        session_request("/api/organization/users", "POST", {"email": email}, success, error)
    }
    static remove_user(id, success=function(){}, error=function(){}) {
        session_request("/api/organization/users/" + id, "DELETE", "", success, error)
    }
    static replace_permissions(userid, permissions, success=function(){}, error=function(){}) {
        //Removes the old permissions and replaces with the new ones
        session_request("/api/organization/users/" + userid + "/permissions", "POST", {"permissions": permissions}, success, error)
    }
    static add_permission(userid, permissions, success=function(){}, error=function(){}) {
        //Add one permission to the list
        session_request("/api/organization/users/" + userid + "/permissions", "UPDATE", {"permission": permissions}, success, error)
    }
    static get_permissions(userid, success=function(){}, error=function(){}) {
        session_request("/api/organization/users/" + userid + "/permissions?user_id=", "GET", "", success, error)
    }
    static get_licenses(success=function(){}, error=function(){}) {
        session_request("/api/organization/licenses", "GET", "", success, error)
    }
}

class Application {
    static create_license(data, success=function(){}, error=function(){}) {
        session_request("/api/organization/apps/" + data["app_id"] + "/licenses", "POST", data, success, error)
    }
    static get_licenses(app_id, success=function(){}, error=function(){}) {
        session_request("/api/organization/apps/" + app_id + "/licenses", "GET", "", success, error)
    }
    static get_statistics(app_id, success=function(){}, error=function(){}) {
        session_request("/api/organization/apps/" + app_id + "/statistics", "GET", "", success, error)
    }
}

class Product {
    static get_statistics(appid, license_id, success=function(){}, error=function(){}) {
        session_request("/api/organization/apps/" + appid + "/licenses/" + license_id + "/statistics", "GET", "", success, error)
    }
}

class Stripe {
    static get_connect_url(success=function(){}, error=function(){}) {
        session_request("/api/organization/stripe/connect/url", "GET", "", success, error)
    }
    static get_connected_accounts(success=function(){}, error=function(){}) {
        session_request("/api/organization/stripe/connect/accounts", "GET", "", success, error)
    }
}



const date_format = (date, format) => {
    const split = date.split("-");
    const year = split[0];
    let month = split[1];
    let day = split[2];

    if(day.length > 1 && day[0] == "0") {
        day = day.substring(1);
    }
    if(month.length > 1 && month[0] == "0") {
        month = month.substring(1);
    }

    return format.replace("y", year).replace("m", month).replace("d", day)
}

let notice = null;
$(document).ready(function () {
    notice = new Notice("base-notice");
})

class Validators {
    static email(email) {
        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))
        {
            return true
        }
        return false
    }
    static int(val) {
        return (val != "" && isNaN(val) == false);
    }
    static float(val) {
        return /^(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$/.test(val);
    }
    static price(val) {
        val = val.replace(",", ".")
        const float = Validators.float(val)
        if(float == false) {
            return false
        }
        let colon = null;
        if(val.indexOf(".") != -1) colon = ".";
        if(colon != null) {
            let sp = val.split(".")
            if(sp[1].length > 2) {
                return false
            }
        }
        return val;
    }
}

function display_page_loader(show=true) {
    const el = $("#page-loader")
    if(el) {
        if(show) {
            el.addClass("open")
        } else {
            el.removeClass("open")
        }
    }
}

function toggle_page_loader() {
    const el = $("#page-loader")
    if(el) {
        display_page_loader(!el.hasClass("open"));
    }
}

function get_url_parameter(param) {
    var url_string = window.location.href; 
    var url = new URL(url_string);
    var c = url.searchParams.get(param);
    return c;
}

function convert_django_json(value) {
    value = value.replaceAll("'", '"')
    if(value != "None") {
        try {
            return JSON.parse(value)
        } catch(e) {
            return null
        }
    }
    return null
}