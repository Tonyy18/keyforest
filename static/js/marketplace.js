$(function() {
    $("#search-form").on("submit", function() {
        const val = $.trim($("#search-value").val());
        if(val == "") return false;
        window.location.href = "/market/q/" + val;
        return false;
    })
})