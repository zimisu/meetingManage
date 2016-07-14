/**
 * Created by m on 2016/7/14.
 */
window.onload = showMeetingInfo();

function showMeetingInfo() {
    var meetingId = getUrlParam("meetingId");
    console.log("meetingId:" + meetingId);

    $.ajax({
        url: '/new-qr-code/' + meetingId,
        method: 'GET',
        dataType: 'JSON',
        success: function (response) {
            console.log(response);

            if (response.result === "ok") {
                $('.QR-code')[0].outerHTML = "<img class='QR-code' src='" + response.url + "'>";
                // $('body').append(
                //     "<img class='QR-code' src='+"+response.url+"'>"
                // );
            }


            // $.ajax({
            //     url: '/meeting/'+meetingId,
            //     method: 'GET',
            //     dataType: 'JSON',
            //     success: function (response) {
            //         console.log(response);
            //
            //         if(response.result === "ok") {
            //             $('body').append(
            //                
            //             );
            //         }
            //     }
            // });

        }

    });

    $.ajax({
        url: '/meeting/' + meetingId,
        method: 'GET',
        dataType: 'JSON',
        success: function (response) {
            console.log(response);

            if (response.result === "ok") {

                var timestamp = new Date(response.timestamp * 1000);
                var year = timestamp.getFullYear();
                var month = timestamp.getMonth() + 1;
                var date = timestamp.getDate();
                var hour = timestamp.getHours() + 1;
                var minute = timestamp.getMinutes() + 1;

                var show_date = year + "-" + month + "-" + date + " " + hour + ":" + minute;

                $('.meeting-info-section').append(
                    "<p class='meeting-info'>"
                    + response.title
                    + "</p>"
                    + "<p class='meeting-info'>"
                    + "@ " + response.place
                    + "</p>"
                    + "<p class='meeting-info'>"
                    + show_date
                    + "</p>"
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

