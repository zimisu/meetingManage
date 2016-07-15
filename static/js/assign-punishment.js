/**
 * Created by m on 2016/7/14.
 */


window.onload = function () {

    var openId = getUrlParam('openid');

    $('#ct').html('');

    $.ajax({
        url: '/meeting?openid=' + openId,
        method: 'GET',
        dataType: 'JSON',
        success: function (response) {
            console.log(response);

            if (response.result === 'ok') {
                var len = response.meetings.length;

                for (var i = 0; i < len; ++i) {
                    var m = response.meetings[i];

                    console.log(m);

                    var timestamp = new Date(m.timestamp * 1000);
                    var year = timestamp.getFullYear();
                    var month = timestamp.getMonth() + 1;
                    var date = timestamp.getDate();
                    var hour = timestamp.getHours() + 1;
                    var minute = timestamp.getMinutes() + 1;
                    var show_date = year + '-' + month + '-' + date + ' ' + hour + ':' + minute;
                    $('#ct').append(
                        "<a class='meeting-item' href='/punishment_?a=1&meetingid=" + m.meetingid + "'>"
                        + "<h2 class='meeting-name'>" + m.title + "</h2>"
                        + "<span class='meeting-location'>@ " + m.place + "</span>"
                        + "<span class='meeting-times'>" + show_date + "</span>" + "</a>"
                    )
                }

                if (len === 0) {
                    $('#ct').append(
                        "<p>xxx内没有即将召开的会议_(:зゝ∠)_</p>"
                    );
                }

            } else {
                $('#ct').append(
                    "<p>枣糕！出问题了！可能是账号授权失效，请重新绑定~</p>"
                );
            }
        }
    })
};

function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return unescape(r[2]);
    return null; //返回参数值
}
