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
        this.dom.find(".hide-alert").on("click", function() {
            this.dom.removeClass("open")
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
        session_request("/api/organization/users", "DELETE", {"user_id": id}, success, error)
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
$(document).ready(() => {
    notice = new Notice("base-notice");
})

class Validators {
    static email(email) {
        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))
        {
            return (true)
        }
        return (false)
    }
}