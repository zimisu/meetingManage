/**
 * Created by m on 2016/7/12.
 */

window.onload = getAppArgs();

var appId, timestamp, nonceStr, signature, isArgsLoaded;

function getAppArgs() {
    $.ajax(
        {
            url: "http://bxchidao.qwert42.org/app_args",
            type: "GET",
            dataType: "JSON",
            success: function (response) {
                console.log(response);

                appId = response.addId;
                timestamp = response.timestamp;
                nonceStr = response.nonceStr;
                signature = response.signature;
            }
        }
    );



    wx.config({
        debug: true,
        appId: appId,
        timestamp : timestamp,
        signature: signature,
        jsApiList: [
            'checkJsApi',
            'scanQRCode'
        ]
    });

    isArgsLoaded = true;

}


wx.ready(function() {

    window.onload = function () {
        if(isArgsLoaded) {
            wx.scanQRCode({
                needResult: 1, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，
                scanType: ["qrCode","barCode"], // 可以指定扫二维码还是一维码，默认二者都有
                success: function (res) {
                    var result = res.resultStr; // 当needResult 为 1 时，扫码返回的结果
                    console.log(result);
                    alert(result);
                }
            });
        }

    };

    document.getElementById("scan-code-btn").onclick = function () {
        wx.scanQRCode({
            needResult: 1, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，
            scanType: ["qrCode","barCode"], // 可以指定扫二维码还是一维码，默认二者都有
            success: function (res) {
                var result = res.resultStr; // 当needResult 为 1 时，扫码返回的结果
                console.log(result);
                alert(result);
            }
        });
    }


});