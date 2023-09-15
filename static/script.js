$(document).ready(function () {

    $(".reality_action").click(function () {
        var id = $(this).attr("data-reality-id");
        var action = $(this).attr("data-action");
        var current_state = $(this).attr("data-current-state");
        console.log("clicked action reality button " + id + " as " + action, 'current_state: ' + current_state);
        $.ajax({
            type: 'POST',
            url: "/reality_set",
            data: { reality_id: id, action: action, current_state: current_state },
            dataType: "text",
            success: function (data) {
                alert("Updated reality " + id + " as " + action);
            }
        });
    });
    // if clicked toggle_all_histories execute click on each .uk-accordion li a
    $("#toggle_all_histories").click(function () {
        console.log("toggled")
        $(".uk-accordion li a").click();
    });

});

