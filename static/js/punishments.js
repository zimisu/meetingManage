/**
 * Created by m on 2016/7/14.
 */

window.onload = function () {

    // var meetingId = getUrlParam('meetingid');

    // $.ajax({
    //     url: '/punishments',
    //     method: 'GET',
    //     dataType: 'JSON',
    //     success: function (response) {
    //         console.log(response);
    //
    //         if (response.result === 'ok') {
    //             var length = response.punishments.length;
    //
    //             for (var i = 0; i < length; i++) {
    //                 var punishment =  response.punishments[i];
    //                 var item = "";
    //
    //                 if(punishment.ptype === '0') {
    //
    //                     item = "<div class='punishment-item ptype0'>"
    //                         + "<span class='punishment-rule'>如果迟到，就要"
    //                         + "<span class='punishment-description'>" + punishment.content0
    //                     + "</span>"
    //                     + "</span>"
    //                     + "</div>";
    //
    //                     // item = "<div class='punishment-item ptype1'>"
    //                     //     + "<span class='punishment-rule'>每迟到"
    //                     //     + "<span class='punishment-minute'>" + punish.content
    //                     // ;
    //                 }
    //
    //                 $('#punishments').append(item);
    //             }
    //         }
    //     }
    // });


    // var $pu = $('#punishments').html('');

    var mid = getUrlParam('meetingid');

    $.ajax({
        method: 'GET',
        url: "/punishments",
        dataType: 'JSON',
        success: function (result) {
            if (result.result === 'ok') {
                var len = result.punishments.length;
                for (var i = 0; i < len; ++i) {
                    const p = result.punishments[i];
                    var el = '';
                    if (p.ptype === '0') {
                        el = "<div class='punishment-item ptype0'>"
                            + "<span class='punishment-rule'>如果迟到，就要"
                            + "<span class='punishment-description'>" + p.content[0]
                            + "</span>"
                            + "</span>"
                            + "</div>";
                    } else if (p.ptype === '1') {
                        el = "<div class='punishment-item ptype1'>" +
                            "<span class='punishment-rule'>每迟到<span class='punishment-minute'>" +
                            p.content[0] +
                            "</span>分钟，交出<span class='punishment-amount'>" + p.content[1]
                            + "</span>人民币！</span></div>"
                    } else if (p.ptype === '2') {
                        el = "<div class='punishment-item ptype2'><span" +
                            " class='punishment-rule'>每迟到<span class='punishment-minute'>"
                            + p.content[0] + "</span>分钟，<span class='punishment-count'>"
                            + p.content[1] + "</span>个<span class='punishment-way'>"
                            + p.content[2] + "</span>！</span>" +
                            "</div>"
                    }

                    $("#punishments").append(el);

                    el = $(el);
                    console.log(el);
                    console.log($(el));

                    $(el).on('click', 'div', function () {

                        console.log("click!");

                        if (mid != null) {
                            $.ajax({
                                type: 'POST',
                                url: '/bind_meeting_punishment',
                                data: {
                                    meetingid: mid,
                                    punishment_id: p.punishment_id
                                },
                                contentType: 'application/json;charset=UTF-8',
                                success: function (result) {
                                    $('body').html('<p>已成功绑定😏</p>')
                                }
                            });
                        }

                    });

                    // $pu.append(el);
                }
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