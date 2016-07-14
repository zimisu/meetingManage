/**
 * Created by m on 2016/7/13.
 */
window.onload = showMembers();
// setInterval(showMembers, 5000);

//test
function showMembers() {
    $('.attended-members').html("");
    $('.absent-members').html("");

    $.ajax({
        url: '/meeting/0',
        method: 'GET',
        dataType: 'JSON',
        success: function (response) {
            console.log(response);
            if (response.result == "ok") {
                $('.meeting-name')[0].innerText = response.title;
                $('.meeting-time')[0].innerText = response.time;

                console.log(response.attendee);
                var length = response.attendee.length;
                var attendedCount = 0;

                for (var i = 0; i < length; i++) {
                    if (response.attendee[i].status === "checked") {
                        $('.attended-members').append(
                            "<div class='attended-user'>"
                            + "<img class='attended-user-avatar' src='" + response.attendee[i].headimgurl + "'>"
                            + "<span class='attended-username'>"
                            + response.attendee[i].nickname + "</span>"
                            + "</div>"
                        );

                        attendedCount++;
                    } else if (response.attendee[i].status === "not checked") {
                        $('.absent-members').append(
                            "<div class='absent-user'>"
                            + "<img class='absent-user-avatar' src='" + response.attendee[i].headimgurl + "'>"
                            + "<span class='absent-username'>"
                            + response.attendee[i].nickname + "</span>"
                            + "</div>"
                        );
                    }

                }
                $('.attended-count')[0].innerText = attendedCount + "/" + length;
            }
        }
    });
}