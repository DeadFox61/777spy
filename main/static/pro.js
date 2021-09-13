function pro_active(param, price, desc, sign) {
    $('.pro').removeClass('pro_active');
    $('#pro_'+param).addClass('pro_active');
    $('#submit').removeClass('line_button_no_active');
    $('#us_service').val(param);
    $('#sum').val(price);
    $('#desc').val(desc);
    $('#s').val(sign);
    $('#submit').removeAttr("disabled");
}