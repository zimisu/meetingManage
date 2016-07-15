/**
 * Created by m on 2016/7/14.
 */

$('.save-punishment-btn')[0].onclick = function () {
    var minute = $('.add-punishment-minute')[0].value;
    var amount = $('.add-punishment-amount')[0].value;

    if ($.isNumeric(minute) && $.isNumeric(amount)) {
        $.ajax({
            url: '/add_punishment',
            method: 'POST',
            data: {

                ptype: 1,
                content0: minute,
                content1: amount
            },
            dataType: 'JSON',
            success: function (response) {
                console.log(response);

                if (response.result === 'ok') {
                    alert("这个点子已加入惩罚库！");
                } else {
                    alert("枣糕...好像哪里不对");
                }
            }
        });
    } else {
        alert("不要填写奇怪的东西？");
    }

};


$('.save-punishment-btn')[1].onclick = function () {
    var minute = $('.add-punishment-minute')[1].value;
    var count = $('.add-punishment-count')[0].value;
    var way = $('.add-punishment-way')[0].value;

    if ($.isNumeric(minute) && $.isNumeric(count)) {
        $.ajax({
            url: '/add_punishment',
            method: 'POST',
            data: {
                ptype: 2,
                content0: minute,
                content1: count,
                content2: way
                //content: [minute, count, way]
            },
            dataType: 'JSON',
            success: function (response) {
                console.log(response);

                if (response.result === 'ok') {
                    alert("这个点子已加入惩罚库！");
                } else {
                    alert("枣糕...好像哪里不对");
                }
            }
        });
    } else {
        alert("不要填写奇怪的东西？");
    }

};

$('.save-punishment-btn')[2].onclick = function () {
    var description = $('.add-punishment-description')[0].value;

    $.ajax({
        url: '/add_punishment',
        method: 'POST',
        data: {
            ptype: 0,
            content0: description
            //content: [description]
        },
        dataType: 'JSON',
        success: function (response) {
            console.log(response);

            if (response.result === 'ok') {
                alert("这个点子已加入惩罚库！");
            } else {
                alert("枣糕...好像哪里不对");
            }
        }
    });
};

function goBack() {
    history.back(-1);
}