$(function() {
    $("#menu-toggle").click(function() {
        $("#navbar").toggleClass("open");
    })
    $("#search-form").on("submit", function(e) {
        const value = $.trim($(this).find("input[type='text']").val());
        if(value) {
            window.location.href = "/market/search/" + value;
        }
        return false;
    })
})
const loader = $('<div class="tac"><img src="/static/images/loader.gif" class="loader"></div>');
const no_search_results = $('<h2 class="tac no-results">No results found</h2>')
function build_app_thumbnail(app) {
    const parent = $('<a href="/market/seller/' + app.organization.id + '/app/' + app.id + '" class="app-thumb"></a>');
    const image = $('<div class="app-image" style="background-image: url(' + app.image + ')"></div>')
    const info = $('<div class="app-info"></div>')
    info.append($('<div class="left"></div>').append('<img src="' + app.organization.image + '">'));
    const right = $('<div class="right"></div>');
    right.append('<p class="app-name">' + app.name + '</p>').append('<p class="app-creator">' + app.organization.name + '</p>')
    const stars = $('<div class="app-stars"></div>');
    for(let a = 0; a < 5; a++) {
        if(a == 4 && app.reputation % 1 != 0) {
            stars.append('<i class="fa-solid fa-star-half-stroke"></i>');
            break;
        }
        if(a < app.reputation) {
            stars.append('<i class="fa-solid fa-star"></i>')
        } else {
            stars.append('<i class="fa-regular fa-star"></i>')
        }
    }
    right.append(stars);
    info.append(right)
    parent.append(image)
    parent.append(info)
    return parent
}
function add_search_results(data) {
    data = JSON.parse(data.replaceAll("&quot;", "\""))
    const els = []
    $("#search-results-count").html(data.data.length)
    if(data.data.length == 0) {
        $("#search-results-objects").html(no_search_results);
        return;
    }
    for(let a = 0; a < data.data.length; a++) {
        const app = data.data[a]
        els.push(build_app_thumbnail(app));
    }
    $("#search-results-objects").empty();
    for(let a = 0; a < els.length; a++) {
        $("#search-results-objects").append(els[a]);
    }
}