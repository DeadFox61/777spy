// Переключение вкладок
function tab(param) {
    $('.tab').hide(0);
    $('.tab_'+param).show(0);
    $('.tab_button').removeClass('tab_button_active');
    $('.tab_button_'+param).addClass('tab_button_active');
}

// Разворачивет меню редактирования информации о ссылке
function partner_ref_edit(refid) {
    $('.partner_ref_edit_show_'+refid).show(0);
    $('.partner_ref_edit_hide_'+refid).hide(0);
    $('.partner_ref_edit_hide_'+refid+'_source').hide(0);
    $('.partner_ref_edit_hide_'+refid+'_comment').hide(0);
}

// Сворачивет меню редактирования информации о ссылке
function partner_ref_edit_cancel(refid) {
    $('.partner_ref_edit_show_'+refid).hide(0);
    $('.partner_ref_edit_hide_'+refid).show(0);
    if ($('.partner_ref_edit_hide_'+refid+'_source').hasClass('source_show')) {$('.partner_ref_edit_hide_'+refid+'_source').show(0);}
    if ($('.partner_ref_edit_hide_'+refid+'_comment').hasClass('comment_show')) {$('.partner_ref_edit_hide_'+refid+'_comment').show(0);}
}

// Добавляет новую ссылку
function add_new_ref_link() {
    $.ajax ({ 
        url: "partner_ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'add_new_ref_link'}),         
        dataType: "json",               
        success: function (data) {
            location.href=location.href;
        }        
    });
}

// Удаляет ссылку
function del_ref_link(value) {
    if (confirm("Удалить реферальную ссылку?")) {//Удалить реферальную ссылку?
        $.ajax ({ 
            url: "partner_ajax", 
            type: "POST",
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'del_ref_link', value: value}),         
            dataType: "json",               
            success: function (data) { 
                $('#partner_ref_'+value).detach();                  
            }        
        });
    }
}

// Изменяет информацию о ссылке
function partner_ref_edit_save(refid) {
    promo = $('#partner_ref_edit_promo_'+refid+' option:selected').text();
    source = $('#partner_ref_edit_source_'+refid).val();
    comment = $('#partner_ref_edit_comment_'+refid).val();
    $.ajax ({ 
        url: "partner_ajax", 
        type: "POST",
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'partner_ref_edit_save', promo_value: promo, source: source, comment: comment, ref_value: refid}),         
        dataType: "json",               
        success: function (data) {
            $('#partner_ref_edit_promo_text_'+refid).text(promo);
            $('#partner_ref_edit_source_text_'+refid).text(source);
            $('#partner_ref_edit_comment_text_'+refid).text(comment);
            $('.partner_ref_edit_show_'+refid).hide(0);
            $('.partner_ref_edit_hide_'+refid).show(0);
            if (!source) {$('.partner_ref_edit_hide_'+refid+'_source').removeClass('source_show');} 
            else {$('.partner_ref_edit_hide_'+refid+'_source').addClass('source_show');} 
            if ($('.partner_ref_edit_hide_'+refid+'_source').hasClass('source_show')) {$('.partner_ref_edit_hide_'+refid+'_source').show(0);}
            if (!comment) {$('.partner_ref_edit_hide_'+refid+'_comment').removeClass('comment_show');}
            else  {$('.partner_ref_edit_hide_'+refid+'_comment').addClass('comment_show');}
            if ($('.partner_ref_edit_hide_'+refid+'_comment').hasClass('comment_show')) {$('.partner_ref_edit_hide_'+refid+'_comment').show(0);}
        }        
    });  

}