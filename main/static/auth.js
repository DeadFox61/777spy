$(document).ready(function () {  
    
    //нажатие энтер или эскейп
    $(document).keydown(function(e) {
        if(e.keyCode === 13) {    //энтер   
            signin();
        }
    }); 

    $(".signin_input").on("input",function() {
        $('.signin_input').removeClass('input_error');
    });   
    $(".menu_input").on("input",function() {
        $('.menu_input').removeClass('input_error');
    });  
 
    $("#user_input_login, #user_input_pass").on("input",function() {
        $('#user_input_login, #user_input_pass').removeClass('input_error');
    });  

    $("#menu_telega_input").on("input",function() {
        $('#menu_telega_input').removeClass('input_error');
    });
    

}); 

function langs(){
    //подгрузка нужного языка в js
    let text = [];
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'text'}),         
        dataType: "html",   
        async:false,            
        success: function (data) {
            data = JSON.parse(data); // обязательно
            // console.log(data); 
            text = data;
        }        
    });
    return text;
}

function signin() { 
    var lang = langs();
    $('#signin_error').hide().text(''); 
    login = $('#signin_login').val();
    password = $('#signin_password').val();
    password2 = $('#signin_password2').val();
    signin_phone = $('#signin_phone').val();
    signin_telegram = $('#signin_telegram').val();
    text = $('.signin_button').text();
    refid = $('#signin_refid').text();
    if (text.toUpperCase() == lang['reg'].toUpperCase()) {button = 2;}//регистрация
    else if (text.toUpperCase() == lang['enter'].toUpperCase()) {button = 1;}//вход
    if (!login) {$('#signin_login, #signin_password').addClass('input_error');}
    if (!password) {$('#signin_password').addClass('input_error');}
    if (!password2 && button == 2) {$('#signin_password2').addClass('input_error');}
    if ((button == 1 && login && password) || (button == 2 && login && password && password2)) {
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'signin', login: login, password: password, button: button,  password2: password2,  signin_phone: signin_phone,  signin_telegram: signin_telegram, refid: refid}),         
            dataType: "html",               
            success: function (data) { 
                if (data == '1_ok' || data == '2_ok') {location.href=location.href;}
                else if (data == '1_no'){
                    $('#signin_login, #signin_password').addClass('input_error');
                    $('#signin_error').show().text(lang['js']['signin']['1']);//Логин и пароль не верен.
                    info = $('.signin_info').text();
                    if (!info || info == 0){
                        $('.signin_info').text('1');
                    } else if (info == 1){
                        $('.signin_info').text(lang['js']['signin']['2']+' @Lucky777wheel').show().attr('style', 'display: block');//Проблемы со входом? писать в телеграмм
                    }
                } else if (data == '0_mail'){
                    $('#signin_login').addClass('input_error');
                    $('#signin_error').show().text(lang['js']['signin']['3']+'.');//Почта введена не верно
                } else if (data == '2_pass'){
                    $('#signin_password, #signin_password2').addClass('input_error');
                    $('#signin_error').show().text(lang['js']['signin']['4']+'.');//Пароли не совпадают
                } else if (data == '0_pass_1'){
                    $('#signin_password').addClass('input_error');
                    $('#signin_error').show().text(lang['js']['signin']['5']+'.');//Пароль должен состоять из 6 и более символов, и содержать только цифры и буквы
                } else if (data == '0_pass_2'){
                    $('#signin_password2').addClass('input_error');
                    $('#signin_error').show().text(lang['js']['signin']['6']+'.'); //Пароль должен состоять из 6 и более символов, и содержать только цифры и буквы
                } else if (data == '2_login'){
                    $('#signin_login').addClass('input_error');
                    $('#signin_error').show().text(lang['js']['signin']['7']+'.');//Такая почта уже зарегистрирована
                } else if (data == '2_phone'){
                    $('#signin_phone').addClass('input_error');
                    $('#signin_error').show().text(lang['js']['signin']['8']+'.');//Телефон должен состоять только из цифр, и может содержать знак + в начале номера
                } else if (data == '2_telegram'){
                    $('#signin_telegram').addClass('input_error');
                    $('#signin_error').show().text(lang['js']['signin']['9']+'.');//Телеграм должен состоять из 3 и более символов, и содержать только цифры, или буквы и цифры
                } 
            }        
        });
    }

}

function signin_tab(param) { 
    var lang = langs();
    $('.signin_title').removeClass('signin_title_no');
    $('.signin_title_'+param).addClass('signin_title_no');
    if (param == 1){$('.signin_inpur_reg').slideDown(0); $('.signin_button').text(lang['reg'].toUpperCase());}
    else if (param == 2){$('.signin_inpur_reg').slideUp(0); $('.signin_button').text(lang['enter'].toUpperCase());}
}