$(document).ready(function () {
    'use strict';
    var windowHeight = $(window).height(),
        bodyHeight = $("body").height(),
        mainBodyHeight = $("#main_body").height(),
        offset = windowHeight - bodyHeight;
    if (bodyHeight < windowHeight) {
        $('#main_body').height(mainBodyHeight + offset + "px");
    }
});