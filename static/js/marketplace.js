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