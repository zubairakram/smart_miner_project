$('document').ready(function () {
    'use strict';
    debugger;
    var mainBodyHeight = $("#main_body").height(),
        mainBodyPadding = $("main_body").css('padding-top'),
        windowHeight = $(window).height(),
        footerHeight = $("#footer").height();

    if (windowHeight > mainBodyHeight) {
        var marginTop = windowHeight - (footerHeight + mainBodyHeight + mainBodyPadding);
        $("#footer").css("margin-top", marginTop);
    }

});