/**
 * Created by m on 2016/7/12.
 */

init();

function init() {
    $.ajax(
        {
            url: "http://bxchidao.qwert42.org/app_args",
            type: "GET",
            dataType: "JSON",
            success: function (response) {
                console.log(response);
                alert(response);
            }
        }
    );
}