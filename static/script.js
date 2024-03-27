$(document).ready(function () {

    $(".reality_action").click(function () {
        clicked_element = $(this);
        var id = clicked_element.attr("data-reality-id");
        var action = clicked_element.attr("data-action");
        var current_state = clicked_element.attr("data-current-state");
        $.ajax({
            type: 'POST',
            url: "/reality_set",
            data: { reality_id: id, action: action, current_state: current_state },
            dataType: "text",
            success: function (data) {
                var new_state = 1 - current_state;
                console.log("Updated reality " + id + " as " + action);
                UIkit.notification({ message: "Updated id: " + id + " as " + (new_state==0?"NOT ":"") + action, status: 'success' });
                clicked_element.attr("data-current-state", new_state);
                clicked_element.removeClass("state-" + current_state);
                clicked_element.addClass("state-" + new_state);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error: " + errorThrown);
                UIkit.notification({ message: "Error: " + errorThrown, status: 'danger' });
            }
        });
    });
    // if clicked toggle_all_histories execute click on each .uk-accordion li a
    $("#toggle_all_histories").click(function () {
        console.log("toggled")
        $(".uk-accordion li a").click();
    });

});

