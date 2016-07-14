/**
 * Created by m on 2016/7/14.
 */
window.onload = showRecentMeetings();


function showRecentMeetings() {
    $('body').html("");

    $.ajax({
        url: '/meeting/',
        method: 'GET',
        dataType: 'JSON',
        success: function (response) {
            console.log(response);

            if (response.result === "ok") {
                var length = response.meetings.length;
                for (var i = 0; i < length; i++) {
                    $('body').append(
                        "<div class='meeting-item'>"
                        + "<h2 class='meeting-name'>"
                        + response.meetings[i].title
                        + "</h2>"
                        + "<span class='meeting-location'>"
                        + response.meetings[i].room
                        + "</span>"
                        + "<span class='meeting-time'>"
                        + response.meetings[i].time
                        + "</span>"
                        + "</div>"
                    );
                }
            }

        }
    });
}