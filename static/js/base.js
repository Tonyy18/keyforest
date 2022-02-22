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
        this.dom.addClass(type);
        this.text.html(text)
        this.dom.addClass("open")
        const ob = this;
        this.interval = setInterval(function() {
           ob.close() 
        }, time)
    }
    close() {
        this.dom.removeClass("open")
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

class User {
    static token = getCookie("csrftoken");
    static create_organization(data, success=function(){}, error=function(){}) {
        $.ajax({
            url: "/api/user/organizations",
            type: "POST",
            headers: {
                "X-CSRFToken": this.token
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
    static get_organizations(success, error) {
        $.ajax({
            url: "/api/user/organizations",
            type: "GET",
            headers: {
                "X-CSRFToken": this.token
            },
            success: success,
            error: error
        })
    }
}

const date_format = (date, format) => {
    const split = date.split("-");
    const year = split[0];
    const month = split[1];
    const day = split[2]
    return format.replace("y", year).replace("m", month).replace("d", day)
}

let notice = null;
$(document).ready(() => {
    notice = new Notice("base-notice");
})