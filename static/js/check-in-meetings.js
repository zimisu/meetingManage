/**
 * Created by m on 2016/7/14.
 */
window.onload = showRecentMeetings();


function showRecentMeetings() {
    var openId = getUrlParam("openid");
    console.log("openId: " + openId);

    $('body').html("");

    $.ajax({
        url: '/meeting?openid=' + openId,
        method: 'GET',
        dataType: 'JSON',
        success: function (response) {
            console.log(response);

            if (response.result === "ok") {
                var length = response.meetings.length;
                for (var i = 0; i < length; i++) {

                    var timestamp = new Date(response.meetings[i].timestamp * 1000);
                    var year = timestamp.getFullYear();
                    var month = timestamp.getMonth() + 1;
                    var date = timestamp.getDate();
                    var hour = timestamp.getHours() + 1;
                    var minute = timestamp.getMinutes() + 1;

                    var show_date = year + "-" + month + "-" + date + " " + hour + ":" + minute;

                    $('body').append(
                        "<a class='meeting-item' href='/show-QR-code?meetingId=" + response.meetings[i].meetingid + "'>"
                        + "<h2 class='meeting-name'>"
                        + response.meetings[i].title
                        + "</h2>"
                        + "<span class='meeting-location'>"
                        + "@ " + response.meetings[i].place
                        + "</span>"
                        + "<span class='meeting-times'>"
                        + show_date
                        + "</span>"
                        + "</a>"
                    );
                }

                if (length == 0) {
                    $('body').append(
                        "<p>一个小时内没有即将召开的会议_(:зゝ∠)_</p>"
                    );
                }
            } else {
                $('body').append(
                    "<p>枣糕！出问题了！可能是账号授权失效，请重新绑定~</p>"
                );
            }

        }
    });
}


function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return unescape(r[2]);
    return null; //返回参数值
}