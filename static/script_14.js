$(document).ready(function () {  
    menu_rules_show();
    menu_rules_show_bacc();
    
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
    

    $("#menu_add_tables").on("input",function() {
        menu_check_select();
    }); 

   //  $('#partner_paid_now_select').change(function(){
   //      if ($('#partner_paid_now_select').val() == 0) {
   //          $('#partner_paid_now_new').show();
   //          $('#partner_paid_button_del').hide();
   //      } else {
   //          $('#partner_paid_now_new').hide();
   //          $('#partner_paid_button_del').show();
   //      }
   // })

    setInterval(function(){
        add_sec()
    },1000);
    update_stats();
    update_stats_bacc();

}); 


function write_if_not_writen_bacc(tag, stat_value, rules = false, stat_type = false){
    if (stat_value  !== $(tag).text()) {
        $(tag).text(stat_value);

    }
    if (!rules){
        return;
    }
    is_color = false;
    for (var i = 0; i < rules.length; i++) {
        rule = rules[i];
        

        if ((rule.rule_type == stat_type) && (stat_value >= rule.count)){
            if (rule['color'] == 1) {p_color = 'green';}
            else if (rule['color'] == 2) {p_color = 'yellow';}
            else if (rule['color'] == 3) {p_color = 'red';}
            $(tag).removeClass("green");
            $(tag).removeClass("yellow");
            $(tag).removeClass("red");
            $(tag).addClass(p_color);
            is_color = true;
            break;
        }
    }

    if (!is_color){
        $(tag).removeClass("green");
        $(tag).removeClass("yellow");
        $(tag).removeClass("red");
    }
    
}


function write_if_not_writen(tag, stat_value, rules, stat_type, stat_is_in_order){
    if (stat_value  !== $(tag).text()) {
        $(tag).text(stat_value);

    }
    is_color = false;
    for (var i = 0; i < rules.length; i++) {
        rule = rules[i];
        

        if ((rule.rule_type == stat_type) && (rule.is_in_order == stat_is_in_order) && (stat_value >= rule.count)){
            if (rule['color'] == 1) {p_color = 'green';}
            else if (rule['color'] == 2) {p_color = 'yellow';}
            else if (rule['color'] == 3) {p_color = 'red';}
            $(tag).removeClass("green");
            $(tag).removeClass("yellow");
            $(tag).removeClass("red");
            $(tag).addClass(p_color);
            is_color = true;
            break;
        }
    }

    if (!is_color){
        $(tag).removeClass("green");
        $(tag).removeClass("yellow");
        $(tag).removeClass("red");
    }
    
}

function update_stats_bacc(){
    $.ajax ({ 
        url: "get_stats_bacc", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN}),         
        dataType: "json",               
        success: function (stats) {
            setTimeout(function(){
                update_stats_bacc()
            },1000);
            rules_data = stats.rules_data;
            for (var i = 0; i < stats.bacc_data.length; i++) {
                stat = stats.bacc_data[i];
                if (!stat.is_selected){
                    $('#bacc_'+stat.bacc_id).parent().parent().hide();
                    continue;
                }
                $('#bacc_'+stat.bacc_id).parent().parent().show();
                //вывод цифр на экран / если совпадает то пропускает, если нет, то меняет и мигает / мигают только те что имеют зеленую желтую или красную подсветку
                write_if_not_writen_bacc('#bacc_no_'+stat.bacc_id+'_bank',stat.stats.bank,rules_data,1);
                write_if_not_writen_bacc('#bacc_no_'+stat.bacc_id+'_play',stat.stats.player,rules_data,2);
                write_if_not_writen_bacc('#bacc_no_'+stat.bacc_id+'_tie',stat.stats.tie,rules_data,3);
                write_if_not_writen_bacc('#bacc_col_'+stat.bacc_id+'_total',stat.stats.total_count);
                write_if_not_writen_bacc('#bacc_col_'+stat.bacc_id+'_bank',stat.stats.bank_count);
                write_if_not_writen_bacc('#bacc_col_'+stat.bacc_id+'_play',stat.stats.player_count);
                write_if_not_writen_bacc('#bacc_col_'+stat.bacc_id+'_tie',stat.stats.tie_count);
            }
        },
        error: function (){
            setTimeout(function(){
                update_stats_bacc()
            },5000);
        }
    }); 
}

function update_stats(){
    $.ajax ({ 
        url: "get_stats", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN}),         
        dataType: "json",               
        success: function (stats) {
            setTimeout(function(){
                update_stats();
            },1000);
            
            // Обновление чисел на странице
            numHtml = "";
            is_zero = stats.is_zero;
            if (is_zero.fifty_fifty)
                is_zero.fifty_fifty = "zr_reset";
            else
                is_zero.fifty_fifty = "zr_no_reset";
            if (is_zero.alt_fifty_fifty)
                is_zero.alt_fifty_fifty = "zr_reset";
            else
                is_zero.alt_fifty_fifty = "zr_no_reset";

            if(is_zero.dozen_column)
                is_zero.dozen_column = "zr_reset";
            else
                is_zero.dozen_column = "zr_no_reset";
            if(is_zero.alt_dozen_column)
                is_zero.alt_dozen_column = "zr_reset";
            else
                is_zero.alt_dozen_column = "zr_no_reset";

            rules_data = stats.rules_data;
            for (var i = 0; i < stats.roul_data.length; i++) {
                stat = stats.roul_data[i];
                
                numHtml += '<div class="cont cont_wrap cont_100 cont_hor">';
                if (stat.roul_id == 1) {numHtml += '<p class="numbers_title">Evolution</p></div><div class="cont cont_wrap cont_100 cont_hor">';}
                if (stat.roul_id == 30) {numHtml += '<p class="numbers_title">EZugi</p></div><div class="cont cont_wrap cont_100 cont_hor">';}
                if (!stat.is_selected){
                        continue;
                    }
                numHtml += '<p class="numbers">'+stat.name+'</p>';
                for (var j = 0; j < stat.nums.length; j++) {
                    num = stat.nums[j];
                    if (num.is_zero){
                        color = ' number_green ';
                    }
                    else{
                        if (num.is_red) {
                            color = ' number_red ';
                        }
                        else{
                            color = ' number_black ';
                        }
                    }
                    numHtml += '<p class="numbers '+color+' ">'+num.num+'</p>';
                
                }
                numHtml += '</div>'; 
            }
            if (numHtml != $('#number').html()) {$('#number').html(numHtml)} 

            // Обновление статистики
            for (var i = 0; i < stats.roul_data.length; i++) {
                stat = stats.roul_data[i];
                if (!stat.is_selected){
                    $('#line_1_'+stat.roul_id).parent().hide();
                    $('#line_2_'+stat.roul_id).parent().parent().hide();
                    continue;
                }
                $('#line_1_'+stat.roul_id).parent().show();
                $('#line_2_'+stat.roul_id).parent().parent().show();
                $('#row_no_'+stat.roul_id+'_count').text(stat.count);
                //вывод цифр на экран / если совпадает то пропускает, если нет, то меняет и мигает / мигают только те что имеют зеленую желтую или красную подсветку
                write_if_not_writen('#row_no_'+stat.roul_id+'_red',stat.stats.color.red.inverse[is_zero.fifty_fifty],rules_data,1,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_black',stat.stats.color.black.inverse[is_zero.fifty_fifty],rules_data,1,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_alt_1',stat.stats.color.alt[is_zero.alt_fifty_fifty],rules_data,9,false);

                write_if_not_writen('#row_no_'+stat.roul_id+'_odd',stat.stats.parity.odd.inverse[is_zero.fifty_fifty],rules_data,2,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_even',stat.stats.parity.even.inverse[is_zero.fifty_fifty],rules_data,2,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_alt_2',stat.stats.parity.alt[is_zero.alt_fifty_fifty],rules_data,9,false);

                write_if_not_writen('#row_no_'+stat.roul_id+'_small',stat.stats.bigness.small.inverse[is_zero.fifty_fifty],rules_data,3,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_big',stat.stats.bigness.big.inverse[is_zero.fifty_fifty],rules_data,3,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_alt_3',stat.stats.bigness.alt[is_zero.alt_fifty_fifty],rules_data,9,false);

                write_if_not_writen('#row_no_'+stat.roul_id+'_dz1',stat.stats.dozen.data[0].inverse[is_zero.dozen_column],rules_data,4,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_dz2',stat.stats.dozen.data[1].inverse[is_zero.dozen_column],rules_data,4,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_dz3',stat.stats.dozen.data[2].inverse[is_zero.dozen_column],rules_data,4,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_alt_4',stat.stats.dozen.alt[is_zero.alt_dozen_column],rules_data,9,false);

                write_if_not_writen('#row_no_'+stat.roul_id+'_col1',stat.stats.column.data[0].inverse[is_zero.dozen_column],rules_data,5,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_col2',stat.stats.column.data[1].inverse[is_zero.dozen_column],rules_data,5,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_col3',stat.stats.column.data[2].inverse[is_zero.dozen_column],rules_data,5,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_alt_5',stat.stats.column.alt[is_zero.alt_dozen_column],rules_data,9,false);

                write_if_not_writen('#row_no_'+stat.roul_id+'_ser_1',stat.stats.roul_sector.tiers.inverse,rules_data,8,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_ser_2',stat.stats.roul_sector.orphelins.inverse,rules_data,8,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_ser_3',stat.stats.roul_sector.voisins.inverse,rules_data,8,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_ser_4',stat.stats.roul_sector.zero.inverse,rules_data,8,false);
                write_if_not_writen('#row_no_'+stat.roul_id+'_alt_6',stat.stats.roul_sector.alt,rules_data,9,false);
               
                write_if_not_writen('#row_yes_'+stat.roul_id+'_red',stat.stats.color.red.normal[is_zero.fifty_fifty],rules_data,1,true);
                write_if_not_writen('#row_yes_'+stat.roul_id+'_black',stat.stats.color.black.normal[is_zero.fifty_fifty],rules_data,1,true);

                write_if_not_writen('#row_yes_'+stat.roul_id+'_odd',stat.stats.parity.odd.normal[is_zero.fifty_fifty],rules_data,2,true);
                write_if_not_writen('#row_yes_'+stat.roul_id+'_even',stat.stats.parity.even.normal[is_zero.fifty_fifty],rules_data,2,true); 

                write_if_not_writen('#row_yes_'+stat.roul_id+'_small',stat.stats.bigness.small.normal[is_zero.fifty_fifty],rules_data,3,true);
                write_if_not_writen('#row_yes_'+stat.roul_id+'_big',stat.stats.bigness.big.normal[is_zero.fifty_fifty],rules_data,3,true);

                write_if_not_writen('#row_yes_'+stat.roul_id+'_dz1',stat.stats.dozen.data[0].normal[is_zero.dozen_column],rules_data,4,true);
                write_if_not_writen('#row_yes_'+stat.roul_id+'_dz2',stat.stats.dozen.data[1].normal[is_zero.dozen_column],rules_data,4,true);
                write_if_not_writen('#row_yes_'+stat.roul_id+'_dz3',stat.stats.dozen.data[2].normal[is_zero.dozen_column],rules_data,4,true);

                write_if_not_writen('#row_yes_'+stat.roul_id+'_col1',stat.stats.column.data[0].normal[is_zero.dozen_column],rules_data,5,true);
                write_if_not_writen('#row_yes_'+stat.roul_id+'_col2',stat.stats.column.data[1].normal[is_zero.dozen_column],rules_data,5,true);
                write_if_not_writen('#row_yes_'+stat.roul_id+'_col3',stat.stats.column.data[2].normal[is_zero.dozen_column],rules_data,5,true);
                
                for(var g = 1; g <= 12; g++){
                    gg = 'q' + g;
                    write_if_not_writen('#row_no_'+stat.roul_id+'_'+gg,stat.stats.sector_3.data[g-1].inverse,rules_data,6,false);
                }
                write_if_not_writen('#row_no_'+stat.roul_id+'_alt_7',stat.stats.sector_3.alt,rules_data,11,false);

                for(var g = 1; g <= 11; g++){
                    gg = 'w' + g;
                    write_if_not_writen('#row_no_'+stat.roul_id+'_'+gg,stat.stats.sector_6.data[g-1].inverse,rules_data,7,false);
                }

                for(var g = 0; g <= 36; g++){
                    gg = 'e' + g;
                    write_if_not_writen('#row_no_'+stat.roul_id+'_'+gg,stat.stats.number.data[g].inverse,rules_data,10,false);
                }  
                
            }
            line_color();
        },
        error: function(){
            setTimeout(function(){
                update_stats()
            },5000);
            
        }      
    });
}




// меню  скрыть показать в меню раздел "Учитывать Zero, как сброс"
function menu_block_on(id) {    
    $('#'+id).slideToggle();
    if (id == 'menu_table') {menu_table_show();}
    if (id == 'menu_check') {menu_zero_show();}
    if (id == 'menu_bacc') {menu_bacc_show();}
    
}

//МЕНЮ скрыть.показать.изменить параметр какие БАККАРЫ выводить на экран
function menu_bacc_show(){
    $.ajax ({ 
        url: "get_choice_bacc", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN}),         
        dataType: "json",               
        success: function (data) {
            user = data.user;
            baccs = data.baccarats;
            html_data = "";
            html_data += '<p class="max menu_check_line_p menu_check_line_p_title">Evolution</p>';
            for (var i = 0; i < baccs.Evolution.length; i++) {
                bacc = baccs.Evolution[i];            
                $table = 't'+bacc.bacc_id;
                if (bacc.is_selected) {menu_1_css = ' '; menu_1_ico = ' fa-check ';} else {menu_1_css = ' menu_check_line_off '; menu_1_ico = ' fa-times ';}
                
                
                html_data += `
                <div class="cont cont_111 cont_hor cont_nowrap menu_check_line cursor `+menu_1_css+`" onclick="menu_bacc_switch('`+bacc.bacc_id+`')">
                    <i class="fa `+menu_1_ico+` menu_check_ico menu_table_ico_`+bacc.bacc_id+`"></i>
                    <p class="max menu_check_line_p cursor">`+bacc.name+`</p>
                </div>`; 
                   
            }
            html_data += '<p class="max menu_check_line_p menu_check_line_p_title">EZugi</p>';
            for (var i = 0; i < baccs.Ezugi.length; i++) {
                bacc = baccs.Ezugi[i];            
                $table = 't'+bacc.bacc_id;
                if (bacc.is_selected) {menu_1_css = ' '; menu_1_ico = ' fa-check ';} else {menu_1_css = ' menu_check_line_off '; menu_1_ico = ' fa-times ';}
                
                
                html_data += `
                <div class="cont cont_111 cont_hor cont_nowrap menu_check_line cursor `+menu_1_css+`" onclick="menu_bacc_switch('`+bacc.bacc_id+`')">
                    <i class="fa `+menu_1_ico+` menu_check_ico menu_table_ico_`+bacc.bacc_id+`"></i>
                    <p class="max menu_check_line_p cursor">`+bacc.name+`</p>
                </div>`; 
                   
            }
            $('#menu_bacc').html(html_data);
        }   
    });
}

//МЕНЮ скрыть.показать.изменить параметр какие рулетки выводить на экран
function menu_table_show() {
    $.ajax ({ 
        url: "get_choice_roul", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_table_show', param: 'param'}),         
        dataType: "json",               
        success: function (data) {
            user = data.user;
            rouls = data.roulettes;
            html_data = "";
            for (var i = 0; i < rouls.length; i++) {
                roul = rouls[i];            
                $table = 't'+roul.roul_id;
                if (roul.is_selected) {menu_1_css = ' '; menu_1_ico = ' fa-check ';} else {menu_1_css = ' menu_check_line_off '; menu_1_ico = ' fa-times ';}
                if (roul.roul_id == 1){html_data += '<p class="max menu_check_line_p menu_check_line_p_title">Evolution</p>';}
                else if (roul.roul_id  == 30){html_data += '<p class="max menu_check_line_p menu_check_line_p_title">EZugi</p>';}
                if (roul.roul_id != 2) { 
                    if ((!user.is_pro) && (roul.roul_id == 1)) {
                        html_data +=`
                        <div class="cont cont_111 cont_hor cont_nowrap menu_check_line menu_check_line_off">
                            <i class=" menu_check_ico "></i>
                            <p class="max menu_check_line_p">`+roul.name+`</p>
                        </div>`;
                    }  else { 
                        html_data += `
                        <div class="cont cont_111 cont_hor cont_nowrap menu_check_line cursor `+menu_1_css+`" onclick="menu_table_switch(`+roul.roul_id+`)">
                            <i class="fa `+menu_1_ico+` menu_check_ico menu_table_ico_`+roul.roul_id+`"></i>
                            <p class="max menu_check_line_p cursor">`+roul.name+`</p>
                        </div>`; 
                    }      
                }      
            }
            $('#menu_table').html(html_data);
        }        
    });
}

//МЕНЮ изменить какие баккары выводить на экран
function menu_bacc_switch(param) {  
    $('.menu_table_ico_'+param).addClass('fa-spinner fa-pulse').removeClass('fa-check').removeClass('fa-times');
    $.ajax ({ 
        url: "change_bacc", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, param: param}),         
        dataType: "json",               
        success: function (data) {
            if(data.status == "err"){
                alert("В аккаунте Free вы можете выбрать не более "+data.min_val+" баккарат");
            }
             menu_bacc_show();
        }        
    });
}

//МЕНЮ изменить какие рулетки выводить на экран
function menu_table_switch(param) {  
    $('.menu_table_ico_'+param).addClass('fa-spinner fa-pulse').removeClass('fa-check').removeClass('fa-times');
    $.ajax ({ 
        url: "change_roul", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_table_switch', param: param}),         
        dataType: "json",               
        success: function (data) {
            if(data.status == "err"){
                alert("В аккаунте Free вы можете выбрать не более "+data.min_val+" рулеток");
            }
             menu_table_show();
        }        
    });
}
function menu_zero_show(){
    text = langs();
    $.ajax ({ 
        url: "get_zeros", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN}),         
        dataType: "json",               
        success: function (data) {
            html_data = "";
            if (data.fifty_fifty) {zero_1_css = ' '; zero_1_ico = ' fa-check ';} else {zero_1_css = ' menu_check_line_off '; zero_1_ico = ' fa-times ';}
            if (data.dozen_column) {zero_2_css = ' '; zero_2_ico = ' fa-check ';} else {zero_2_css = ' menu_check_line_off '; zero_2_ico = ' fa-times ';}
            if (data.alt_fifty_fifty) {zero_3_css = ' '; zero_3_ico = ' fa-check ';} else {zero_3_css = ' menu_check_line_off '; zero_3_ico = ' fa-times ';}
            if (data.alt_dozen_column) {zero_4_css = ' '; zero_4_ico = ' fa-check ';} else {zero_4_css = ' menu_check_line_off '; zero_4_ico = ' fa-times ';}
            html_data +=`
                <div class="cont cont_111 cont_hor cont_nowrap menu_check_line `+zero_1_css+`" onclick="menu_zero_switch('fifty_fifty')">
                    <i class="fa `+zero_1_ico+` menu_check_ico menu_check_ico_fifty_fifty"></i>
                    <p class="max menu_check_line_p">50/50</p>
                </div>
                <div class="cont cont_111 cont_hor cont_nowrap menu_check_line `+zero_2_css+`" onclick="menu_zero_switch('dozen_column')">
                    <i class="fa `+zero_2_ico+` menu_check_ico menu_check_ico_dozen_column"></i>
                    <p class="max menu_check_line_p">`+text.ajax.menu_check[1]+`</p>
                </div>
                <div class="cont cont_111 cont_hor cont_nowrap menu_check_line `+zero_3_css+`" onclick="menu_zero_switch('alt_fifty_fifty')">
                    <i class="fa `+zero_3_ico+` menu_check_ico menu_check_ico_alt_fifty_fifty"></i>
                    <p class="max menu_check_line_p">ALT 50/50</p>
                </div>
                <div class="cont cont_111 cont_hor cont_nowrap menu_check_line `+zero_4_css+`" onclick="menu_zero_switch('alt_dozen_column')">
                    <i class="fa `+zero_4_ico+` menu_check_ico menu_check_ico_alt_dozen_column"></i>
                    <p class="max menu_check_line_p">ALT `+text.ajax.menu_check[1]+`</p>
                </div>`;
            $('#menu_check').html(html_data);
        }        
    });
}

function menu_zero_switch(name) {
    $('.menu_check_ico_'+name).addClass('fa-spinner fa-pulse').removeClass('fa-check').removeClass('fa-times');
    $.ajax ({ 
        url: "change_zero", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_check', name: name}),         
        dataType: "json",               
        success: function (data) {
            menu_zero_show();
        }        
    });
}

//сохранить правило Баккара
function menu_add_save_bacc() {   
    name = $('#menu_add_name_bacc').val();   
    tables = $('#menu_add_tables_bacc').val();
    color = $('#menu_add_color_bacc').val();
    count = $('#menu_add_count_bacc').val();
    if (name && count) { 
        
        $.ajax ({ 
            url: "add_rule_bacc", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN,  name: name, tables: tables, color: color, count: count}),         
            dataType: "json",               
            success: function (data) {
                if (data.status == "err"){
                    alert("You can only have "+data.min_val+" Baccarates on Free account");
                }
                else{
                    $('#menu_add_rules_bacc').hide('300');
                    $('#menu_add_name_bacc').val('');
                    $('#menu_add_count_bacc').val('');
                    
                    del_id = $('#menu_edit_id_bacc').text();
                    if (del_id){
                        menu_add_delete_bacc(del_id,false)
                    }
                    $('#menu_edit_id_bacc').text('');
                    menu_rules_show_bacc();
                }
            }        
        });
    }
    if (!name) {$('#menu_add_name').addClass('input_error');} 
    if (!count) {$('#menu_add_count').addClass('input_error');}
    
}
//сохранить правило
function menu_add_save() {   
    name = $('#menu_add_name').val();   
    tables = $('#menu_add_tables').val();
    col = $('#menu_add_col').val();
    color = $('#menu_add_color').val();
    count = $('#menu_add_count').val();
    if (name && count) { 
        
        $.ajax ({ 
            url: "add_rule", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_save_rules', name: name, tables: tables, col: col, color: color, count: count}),         
            dataType: "json",               
            success: function (data) {
                if (data.status == "err"){
                    alert("You can only have "+data.min_val+" rules on Free account");
                }
                else{
                    $('#menu_add_rules').hide('300');
                    $('#menu_add_name').val('');
                    $('#menu_add_count').val('');
                    
                    del_id = $('#menu_edit_id').text();
                    if (del_id){
                        menu_add_delete(del_id,false)
                    }
                    $('#menu_edit_id').text('');
                    menu_rules_show();
                }
            }        
        });
    }
    if (!name) {$('#menu_add_name').addClass('input_error');} 
    if (!count) {$('#menu_add_count').addClass('input_error');}
    
}

// Вывод списка правил
function menu_rules_show_bacc(){
    var lang = langs();
    if ($(".menu_rules").length){ // если меню слева доступна, показывать
        $.ajax ({ 
            url: "get_rules_bacc", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN}),         
            dataType: "json",               
            success: function (data) {
                html_data = "";
                rules = data.rules;
                for (var i = 0; i < rules.length; i++) {
                    rule = rules[i];
                    html_data += `                             
                    <div class="menu_rules_box"> 
                        <div class="cont cont_111 cont_nowrap cont_hor menu_rules_name">
                            <span class="max">`+rule.name+`</span>
                            <i class="fa fa-pencil" onclick="menu_add_edit_bacc(`+rule.id+`)"></i>
                            <i class="fa fa-times " onclick="menu_add_delete_bacc(`+rule.id+`)"></i>
                        </div>
                        <div class="cont cont_111 cont_nowrap cont_hor menu_rules_line">
                            <p>Не выпало</p>
                            <p>`+rule.count+`</p>
                        </div>
                        <div class="cont cont_111 cont_nowrap cont_hor menu_rules_line">
                            <p>`+rule.rule_type+`</p>
                            <div class="menu_rules_color `+rule.color+`"></div>
                        </div>
                        <div class="cont cont_111 cont_nowrap cont_hor menu_rules_line cursor" onclick="menu_add_telegramm_bacc(`+rule.id+`)">`;
                            if (rule.is_tg_on){
                                html_data += `<i class="fa fa-check cursor color_white" id="menu_add_telegramm_bacc_`+rule.id+`"></i>`;
                            }
                            else{
                                html_data += `<i class="fa fa-times cursor" id="menu_add_telegramm_bacc_`+rule.id+`"></i>`;
                            }                
                            html_data += `<p class="max cursor">`+lang.ajax.menu_rules_show["1"]+`</p>
                        </div>
                    </div>`;
                }
                $('.menu_rules_bacc').html(html_data);
            }        
        });
    }
}

function menu_rules_show() {
    var lang = langs();
    if ($(".menu_rules").length){ // если меню слева доступна, показывать
        $.ajax ({ 
            url: "get_rules", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_rules_show'}),         
            dataType: "json",               
            success: function (data) {
                html_data = "";
                rules = data.rules;
                for (var i = 0; i < rules.length; i++) {
                    rule = rules[i];
                    html_data += `                             
                    <div class="menu_rules_box"> 
                        <div class="cont cont_111 cont_nowrap cont_hor menu_rules_name">
                            <span class="max">`+rule.name+`</span>
                            <i class="fa fa-pencil" onclick="menu_add_edit(`+rule.id+`)"></i>
                            <i class="fa fa-times " onclick="menu_add_delete(`+rule.id+`)"></i>
                        </div>
                        <div class="cont cont_111 cont_nowrap cont_hor menu_rules_line">
                            <p>`+rule.is_in_row+`</p>
                            <p>`+rule.how_many_in_row+`</p>
                        </div>
                        <div class="cont cont_111 cont_nowrap cont_hor menu_rules_line">
                            <p>`+rule.rule_type+`</p>
                            <div class="menu_rules_color `+rule.color+`"></div>
                        </div>
                        <div class="cont cont_111 cont_nowrap cont_hor menu_rules_line cursor" onclick="menu_add_telegramm(`+rule.id+`)">`;
                            if (rule.is_tg_on){
                                html_data += `<i class="fa fa-check cursor color_white" id="menu_add_telegramm_`+rule.id+`"></i>`;
                            }
                            else{
                                html_data += `<i class="fa fa-times cursor" id="menu_add_telegramm_`+rule.id+`"></i>`;
                            }                
                            html_data += `<p class="max cursor">`+lang.ajax.menu_rules_show["1"]+`</p>
                        </div>
                    </div>`;
                }
                $('.menu_rules').html(html_data);
            }        
        });
    }
}

//изменение настройки для телеграмма, у каждого правила отдельно, отправлять или нет сообщения в телеграм
function menu_add_telegramm_bacc(rule_id){
    if ($('#menu_add_telegramm_bacc_'+rule_id).hasClass('fa-check')) {
        param = 0;
    } else {
        param = 1;
    }
    $.ajax ({ 
        url: "change_tg_bacc", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, id: rule_id, param: param}),         
        dataType: "json",               
        success: function (data) {
            if(data.status == "err_pro"){
                alert("You need to be pro to do this!");
                if ($('#menu_add_telegramm_bacc_'+rule_id).hasClass('fa-check')) {
                    $('#menu_add_telegramm_bacc_'+rule_id).removeClass('fa-check color_white').addClass('fa-times');
                }            
            }
            else if(data.status == "err"){
                alert("Minial value for this rule should be at least "+data.min_val);
            }
            else{
                if ($('#menu_add_telegramm_bacc_'+rule_id).hasClass('fa-check')) {
                    $('#menu_add_telegramm_bacc_'+rule_id).removeClass('fa-check color_white').addClass('fa-times');
                } else {
                    $('#menu_add_telegramm_bacc_'+rule_id).removeClass('fa-times').addClass('fa-check color_white');
                }
            }
            
            
        }        
    });
}

function menu_add_telegramm(rules){
    if ($('#menu_add_telegramm_'+rules).hasClass('fa-check')) {
        param = 0;
    } else {
        param = 1;
    }
    $.ajax ({ 
        url: "change_tg", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_add_telegramm', id: rules, param: param}),         
        dataType: "json",               
        success: function (data) {
            if(data.status == "err_pro"){
                alert("You need to be pro to do this!");
                if ($('#menu_add_telegramm_'+rules).hasClass('fa-check')) {
                    $('#menu_add_telegramm_'+rules).removeClass('fa-check color_white').addClass('fa-times');
                }            
            }
            else if(data.status == "err"){
                alert("Minial value for this rule should be at least "+data.min_val);
            }
            else{
                if ($('#menu_add_telegramm_'+rules).hasClass('fa-check')) {
                    $('#menu_add_telegramm_'+rules).removeClass('fa-check color_white').addClass('fa-times');
                } else {
                    $('#menu_add_telegramm_'+rules).removeClass('fa-times').addClass('fa-check color_white');
                }
            }
            
            
        }        
    });
}

function menu_add_delete_bacc(id,is_refresh = true) {
    var lang = langs();
    if(is_refresh){
        if (!(confirm(lang['delete']+'?'))) {
            return;
        }
    }
    $.ajax ({ 
        url: "del_rule_bacc", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, id: id}),         
        dataType: "json",               
        success: function (data) {
            if(is_refresh)
                menu_rules_show_bacc();
        }        
    });
    
}

function menu_add_delete(id,is_refresh = true) {
    var lang = langs();
    if(is_refresh){
        if (!(confirm(lang['delete']+'?'))) {
            return;
        }
    }
    $.ajax ({ 
        url: "del_rule", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_rules_delete', id: id}),         
        dataType: "json",               
        success: function (data) {
            if(is_refresh)
                menu_rules_show();
        }        
    });
    
}

function menu_add_edit_bacc(id) {    
    $.ajax ({ 
        url: "get_clean_rule_bacc", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_rules_edit', id: id}),         
        dataType: "json",               
        success: function (rule) {
            $('#menu_edit_id_bacc').text(rule['id']); 
            $('#menu_add_name_bacc').val(rule['name']);
            $('#menu_add_count_bacc').val(rule['count']);
            $('#menu_add_tables_bacc option[value="'+rule['rule_type']+'"]').prop('selected', true);
            $('#menu_add_color_bacc option[value="'+rule['color']+'"]').prop('selected', true);
            $('#menu_add_rules_bacc').slideDown('500');
        }        
    });
}

function menu_add_edit(id) {    
    $.ajax ({ 
        url: "get_clean_rule", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_rules_edit', id: id}),         
        dataType: "json",               
        success: function (rule) {
            $('#menu_edit_id').text(rule['id']); 
            $('#menu_add_name').val(rule['name']);
            $('#menu_add_count').val(rule['how_many_in_row']);
            if(rule["is_in_row"]){table = 1}
            else{table = 0}
            $('#menu_add_tables option[value="'+table+'"]').prop('selected', true);
            $('#menu_add_col option[value="'+rule['rule_type']+'"]').prop('selected', true);
            $('#menu_add_color option[value="'+rule['color']+'"]').prop('selected', true);
            $('#menu_add_rules').slideDown('500');
        }        
    });
}


//сохранение id телеграмма в меню
function menu_telega_save() {
    var lang = langs();
    param = $('#menu_telega_input').val();
    $.ajax ({ 
        url: "save_tg_id", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_telega_save', param: param}),         
        dataType: "html",               
        success: function (data) {
            //alert(data);
            if (data == 'yes') {location.href=location.href;}
            else {
                $('#menu_telega_input').addClass('input_error');
            }
        }        
    });
}

function add_sec(){
    $.ajax ({ 
        url: "add_sec", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN}),         
        dataType: "html",         
        success: function (data) {
        }        
    });
}

//подсветка по полосам в таблице
function line_color(){
    $('.line_hide').removeClass('bg_2 bg_1');
    $('.line_hide:visible:even').addClass('bg_2');
    $('.line_hide:visible:odd').addClass('bg_1');
}


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




// Ниже функции ещё не проверены

function date_time(){// вывод Ведутся профилактические работы  если 10 минут не было сообщений от скрипта значений рулеток
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN,type: 'date_time'}),         
        dataType: "html",               
        success: function (data) {
            $('#date_time').html(data);         
        }        
    });
}
//подсветка иконки в меню, если был запрос на вывод денег партнером
function paid_swith(type) {
    if (type == 0){
        if ($('#paid_swith').length) {type = 1;}
        else if ($('#paid_swith_tab').length) {type = 2;}
    }
    if (type != 0){
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN,type: 'paid_swith'}),         
            dataType: "html",               
            success: function (data) {
                if (type == 1){
                    if (data) {$('#paid_swith').addClass('color_yellow');} else {$('#paid_swith').removeClass('color_yellow');}
                } else {
                    if (data) {$('#paid_swith_tab').addClass('bg_yellow');} else {$('#paid_swith_tab').removeClass('bg_yellow');}
                }
                
            }        
        });
    }
}





function count1() {
    var param = [];
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN,type: 'count'}),         
        dataType: "html",               
        success: function (data) {
            data = JSON.parse(data); // обязательно
            //console.log(data);
            for(var i = 1; i <= data['max']; i++){
                if ($('#roul_'+i).length){
                    param[i] = $('#roul_'+i).text();
                    //alert('Рулетка '+i+' / было '+param[i]+' / стало '+data[i]+' / max '+data['max']);
                    if (param[i] != data[i] && data[i]){
                        count2(i);
                        $('#roul_'+i).text(data[i]);
                        $('#line_1_'+i).parent().slideDown(200);
                        $('#line_2_'+i+', #line_3_'+i).parent().parent().slideDown(200);
                    } else if (param[i] != data[i] || data[i] == 0) {
                        $('#line_1_'+i+', #line_2_'+i+', #line_3_'+i).children(".col_2").text('').removeClass('yellow green red');
                        $('#line_1_'+i).parent().slideUp(200);
                        $('#line_2_'+i+', #line_3_'+i).parent().parent().slideUp(200);
                    }
                }
            }
            line_color();
        }        
    });
}
function count2(roul_id) {
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'count2', roul_id: roul_id}),         
        dataType: "html",               
        success: function (data) {
            data = JSON.parse(data); // обязательно
            console.log(data);
            var r = data['roul_id'];
            //-------------------------------------------ПОДСВЕТКА
            //убираем всю подсветку у данной строки
            //$('#line_1_'+r+', #line_2_'+r+', #line_3_'+r).children('.yellow, .green, .red').removeClass('yellow green red'); 
            //запускаем проверку
            var arr = data['rules'];
            var col = [];
            for (var arr_key in arr) {
                rules = data['rules'][arr_key];
                if (rules['col'] == 1) {col[0] = 'red'; col[1] = 'black';}
                else if (rules['col'] == 2) {col[0] = 'odd'; col[1] = 'even';}
                else if (rules['col'] == 3) {col[0] = 'small'; col[1] = 'big';}
                else if (rules['col'] == 4) {col[0] = 'dz1'; col[1] = 'dz2'; col[2] = 'dz3';}
                else if (rules['col'] == 5) {col[0] = 'col1'; col[1] = 'col2'; col[2] = 'col3';}
                else if (rules['col'] == 6) {for(var c = 0; c <= 11; c++){cc=c+1; col[c]='q'+cc;}}
                else if (rules['col'] == 7) {for(var c = 0; c <= 10; c++){cc=c+1; col[c]='w'+cc;}}
                else if (rules['col'] == 8) {for(var c = 0; c <= 3; c++){cc=c+1; col[c]='ser_'+cc;}}
                else if (rules['col'] == 9) {for(var c = 0; c <= 4; c++){cc=c+1; col[c]='alt_'+cc;}}
                else if (rules['col'] == 10) {for(var c = 0; c <= 36; c++){col[c]='e'+c;}}
                if (rules['color'] == 1) {p_color = 'green';}
                else if (rules['color'] == 2) {p_color = 'yellow';}
                else if (rules['color'] == 3) {p_color = 'red';}
                //включаем подсветку
                if (rules['tables'] == 1) {
                    for(var v = 0; v <= (col.length - 1) ; v++){
                        p_col = col[v];
                        if (data['no'][p_col] >= rules['count']) {
                            if ($('#row_no_'+r+'_'+p_col).hasClass(p_color)) {
                                //telega(p_col, data[p_col], r, t);
                            } else {
                                $('#row_no_'+r+'_'+p_col).addClass(p_color);
                            }
                            
                        } else {
                            $('#row_no_'+r+'_'+p_col).removeClass(p_color);
                        }
                    }
                } else if (rules['tables'] == 2) {
                    for(var v = 0; v <= (col.length - 1) ; v++){
                        p_col = col[v];
                        if (data['yes'][p_col] >= rules['count']) {
                            if ($('#row_yes_'+r+'_'+p_col).hasClass(p_color)) {
                                //telega(p_col, data[p_col], r, t);
                            } else {
                                $('#row_yes_'+r+'_'+p_col).addClass(p_color);
                            }
                            
                        } else {
                            $('#row_yes_'+r+'_'+p_col).removeClass(p_color);
                        }
                    }
                }
                col = [];
                
            }
            //вывод цифр на экран / если совпадает то пропускает, если нет, то меняет и мигает / мигают только те что имеют зеленую желтую или красную подсветку
            if (data['no']['red'] !== $('#row_no_'+r+'_red').text()) {$('#row_no_'+r+'_red').text(data['no']['red']);}
            if (data['no']['black'] !== $('#row_no_'+r+'_black').text()) {$('#row_no_'+r+'_black').text(data['no']['black']);}
            if (data['no']['even'] !== $('#row_no_'+r+'_even').text()) {$('#row_no_'+r+'_even').text(data['no']['even']);}
            if (data['no']['odd'] !== $('#row_no_'+r+'_odd').text()) {$('#row_no_'+r+'_odd').text(data['no']['odd']);}
            if (data['no']['small'] !== $('#row_no_'+r+'_small').text()) { $('#row_no_'+r+'_small').text(data['no']['small']);}
            if (data['no']['big'] !== $('#row_no_'+r+'_big').text()) {$('#row_no_'+r+'_big').text(data['no']['big']);}
            if (data['no']['dz1'] !== $('#row_no_'+r+'_dz1').text()) {$('#row_no_'+r+'_dz1').text(data['no']['dz1']);}  
            if (data['no']['dz2'] !== $('#row_no_'+r+'_dz2').text()) {$('#row_no_'+r+'_dz2').text(data['no']['dz2']);}
            if (data['no']['dz3'] !== $('#row_no_'+r+'_dz3').text()) {$('#row_no_'+r+'_dz3').text(data['no']['dz3']);}
            if (data['no']['col1'] !== $('#row_no_'+r+'_col1').text()) {$('#row_no_'+r+'_col1').text(data['no']['col1']);}      
            if (data['no']['col2'] !== $('#row_no_'+r+'_col2').text()) {$('#row_no_'+r+'_col2').text(data['no']['col2']);}
            if (data['no']['col3'] !== $('#row_no_'+r+'_col3').text()) {$('#row_no_'+r+'_col3').text(data['no']['col3']);}
            if (data['yes']['red'] !== $('#row_yes_'+r+'_red').text()) {$('#row_yes_'+r+'_red').text(data['yes']['red']);}
            if (data['yes']['black'] !== $('#row_yes_'+r+'_black').text()) {$('#row_yes_'+r+'_black').text(data['yes']['black']);}
            if (data['yes']['even'] !== $('#row_yes_'+r+'_even').text()) {$('#row_yes_'+r+'_even').text(data['yes']['even']);}
            if (data['yes']['odd'] !== $('#row_yes_'+r+'_odd').text()) {$('#row_yes_'+r+'_odd').text(data['yes']['odd']);}
            if (data['yes']['small'] !== $('#row_yes_'+r+'_small').text()) { $('#row_yes_'+r+'_small').text(data['yes']['small']);}
            if (data['yes']['big'] !== $('#row_yes_'+r+'_big').text()) {$('#row_yes_'+r+'_big').text(data['yes']['big']);}
            if (data['yes']['dz1'] !== $('#row_yes_'+r+'_dz1').text()) {$('#row_yes_'+r+'_dz1').text(data['yes']['dz1']);}  
            if (data['yes']['dz2'] !== $('#row_yes_'+r+'_dz2').text()) {$('#row_yes_'+r+'_dz2').text(data['yes']['dz2']);}
            if (data['yes']['dz3'] !== $('#row_yes_'+r+'_dz3').text()) {$('#row_yes_'+r+'_dz3').text(data['yes']['dz3']);}
            if (data['yes']['col1'] !== $('#row_yes_'+r+'_col1').text()) {$('#row_yes_'+r+'_col1').text(data['yes']['col1']);}      
            if (data['yes']['col2'] !== $('#row_yes_'+r+'_col2').text()) {$('#row_yes_'+r+'_col2').text(data['yes']['col2']);}
            if (data['yes']['col3'] !== $('#row_yes_'+r+'_col3').text()) {$('#row_yes_'+r+'_col3').text(data['yes']['col3']);}
            for(var g = 1; g <= 12; g++){
                gg = 'q' + g;
                if (data['no'][gg] !== $('#row_no_'+r+'_'+gg).text()) {$('#row_no_'+r+'_'+gg).text(data['no'][gg]);}
            }
            for(var g = 1; g <= 11; g++){
                gg = 'w' + g;
                if (data['no'][gg] !== $('#row_no_'+r+'_'+gg).text()) {$('#row_no_'+r+'_'+gg).text(data['no'][gg]);}
            }
            for(var g = 0; g <= 36; g++){
                gg = 'e' + g;
                if (data['no'][gg] !== $('#row_no_'+r+'_'+gg).text()) {$('#row_no_'+r+'_'+gg).text(data['no'][gg]);}
            }  
            for(var g = 1; g <= 5; g++){
                gg = 'alt_' + g;
                if (data['no'][gg] !== $('#row_no_'+r+'_'+gg).text()) {$('#row_no_'+r+'_'+gg).text(data['no'][gg]);}
            }
            for(var g = 1; g <= 4; g++){
                gg = 'ser_' + g;
                if (r == 7) {data['no'][gg] = '';}//все кроме 7 рулетки
                if (data['no'][gg] !== $('#row_no_'+r+'_'+gg).text()) {$('#row_no_'+r+'_'+gg).text(data['no'][gg]);}
            }                    
            $('#line_1_'+r+', #line_2_'+r+', #line_3_'+r).children('.yellow, .green, .red').addClass('active'); //цветные клетки данной рулетки получат класс active
            $('#row_yes_'+r+'_count').text(data['count_num']);
            $('#row_no_'+r+'_count').text(data['count_num']);
            // выводим инфу на экран            
            if (data['info']['zero'] != $('.info_'+r+'_info_zero:first').text()) {
                $('.info_'+r+'_info_zero').text(Math.round(data['info']['zero'])+'%');}
            if (data['info']['red'] != $('.info_'+r+'_info_red:first').text()) {
                $('.info_'+r+'_info_red').text(Math.round(data['info']['red'])+'%');
                $('.info_'+r+'_style_red').attr('style', 'height: '+data['info']['red']+'px');
            }
            if (data['info']['black'] != $('.info_'+r+'_info_black:first').text()) {
                $('.info_'+r+'_info_black').text(Math.round(data['info']['black'])+'%');
                $('.info_'+r+'_style_black').attr('style', 'height: '+data['info']['black']+'px');
            }
            if (data['info']['even'] != $('.info_'+r+'_info_even:first').text()) {
                $('.info_'+r+'_info_even').text(Math.round(data['info']['even'])+'%');
                $('.info_'+r+'_style_even').attr('style', 'height: '+data['info']['even']+'px');
            }
            if (data['info']['odd'] != $('.info_'+r+'_info_odd:first').text()) {
                $('.info_'+r+'_info_odd').text(Math.round(data['info']['odd'])+'%');
                $('.info_'+r+'_style_odd').attr('style', 'height: '+data['info']['odd']+'px');
            }
            if (data['info']['small'] != $('.info_'+r+'_info_small:first').text()) {
                $('.info_'+r+'_info_small').text(Math.round(data['info']['small'])+'%');
                $('.info_'+r+'_style_small').attr('style', 'height: '+data['info']['small']+'px');
            }
            if (data['info']['big'] != $('.info_'+r+'_info_big:first').text()) {
                $('.info_'+r+'_info_big').text(Math.round(data['info']['big'])+'%');
                $('.info_'+r+'_style_big').attr('style', 'height: '+data['info']['big']+'px');
            }
            if (data['info']['dz1'] != $('.info_'+r+'_info_dz1:first').text()) {
                $('.info_'+r+'_info_dz1').text(Math.round(data['info']['dz1'])+'%');
                $('.info_'+r+'_style_dz1').attr('style', 'width: '+(data['info']['zero'] / 3 + data['info']['dz1'])+'%');
            } 
            if (data['info']['dz2'] != $('.info_'+r+'_info_dz2:first').text()) {
                $('.info_'+r+'_info_dz2').text(Math.round(data['info']['dz2'])+'%');
                $('.info_'+r+'_style_dz2').attr('style', 'width: '+(data['info']['zero'] / 3 + data['info']['dz2'])+'%');
            }
            if (data['info']['dz3'] != $('.info_'+r+'_info_dz3:first').text()) {
                $('.info_'+r+'_info_dz3').text(Math.round(data['info']['dz3'])+'%');
                $('.info_'+r+'_style_dz3').attr('style', 'width: '+(data['info']['zero'] / 3 + data['info']['dz3'])+'%');
            }
            if (data['info']['col1'] != $('.info_'+r+'_info_col1:first').text()) {
                $('.info_'+r+'_info_col1').text(Math.round(data['info']['col1'])+'%');
                $('.info_'+r+'_style_col1').attr('style', 'width: '+(data['info']['zero'] / 3 + data['info']['col1'])+'%');
            }
            if (data['info']['col2'] != $('.info_'+r+'_info_col2:first').text()) {
                $('.info_'+r+'_info_col2').text(Math.round(data['info']['col2'])+'%');
                $('.info_'+r+'_style_col2').attr('style', 'width: '+(data['info']['zero'] / 3 + data['info']['col2'])+'%');
            }
            if (data['info']['col3'] != $('.info_'+r+'_info_col3:first').text()) {
                $('.info_'+r+'_info_col3').text(Math.round(data['info']['col3'])+'%');
                $('.info_'+r+'_style_col3').attr('style', 'width: '+(data['info']['zero'] / 3 + data['info']['col3'])+'%');
            }
            if (data['info']['ser1'] != $('.info_'+r+'_info_ser1:first').text()) {
                $('.info_'+r+'_info_ser1').text(Math.round(data['info']['ser1'])+'%');
                $('.info_'+r+'_style_ser1').attr('style', 'width: '+data['info']['ser1']+'%');
            }
            if (data['info']['ser2'] != $('.info_'+r+'_info_ser2:first').text()) {
                $('.info_'+r+'_info_ser2').text(Math.round(data['info']['ser2'])+'%');
                $('.info_'+r+'_style_ser2').attr('style', 'width: '+data['info']['ser2']+'%');
            }
            if (data['info']['ser3'] != $('.info_'+r+'_info_ser3:first').text()) {
                $('.info_'+r+'_info_ser3').text(Math.round(data['info']['ser3'])+'%');
                $('.info_'+r+'_style_ser3').attr('style', 'width: '+data['info']['ser3']+'%');
            }
            if (data['info']['ser4'] != $('.info_'+r+'_info_ser4:first').text()) {
                $('.info_'+r+'_info_ser4').text(Math.round(data['info']['ser4'])+'%');
                $('.info_'+r+'_style_ser4').attr('style', 'width: '+data['info']['ser4']+'%');
            }
        }        
    });
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
//открыть/закрыть меню
function menu_on(param) { 
    $('.menu_ico_other').toggle();//скроем остальные значки в меню 
    if (param == 1)  {
        $('#menu_ico_2').toggle(0);
        $('#menu_box_1').toggle(300);
        $('#menu_user').toggle(300);
        if ($("#menu_ico.fa-bars").length){ $('#menu_ico.fa-bars').removeClass('fa-bars').addClass('fa-chevron-right turn_180');}
        else {$('#menu_ico.fa-chevron-right').removeClass('fa-chevron-right turn_180').addClass('fa-bars');}
        $('#menu_add_rules').hide(300);
    } else if (param == 2) {
        $('#menu_ico').toggle(0);
        $('#menu_box_2').toggle(300);
        
    }
}
// открыть /закрыть панель добавления в меню правила
function menu_add_bacc() {
    $('#menu_add_rules_bacc').slideToggle('500');
    $('#menu_edit_id_bacc').text(''); 
    $('#menu_add_name_bacc').val('');
    $('#menu_add_count_bacc').val('');
    $('#menu_add_tables_bacc option[value="0"]').prop('selected', true);
    $('#menu_add_color_bacc option[value="1"]').prop('selected', true);
}

function menu_add() {
    $('#menu_add_rules').slideToggle('500');
    $('#menu_edit_id').text(''); 
    $('#menu_add_name').val('');
    $('#menu_add_count').val('');
    $('#menu_add_tables option[value="0"]').prop('selected', true);
    $('#menu_add_col option[value="1"]').prop('selected', true);
    $('#menu_add_color option[value="1"]').prop('selected', true);
    menu_check_select();
}
function menu_check_select() {
    col = $('#menu_add_tables').val();
    if (col == 1) {
        /*$('#menu_add_col option[value="6"]').prop('disabled', true);*/
        $('#menu_add_col option[value="6"]').hide();
        $('#menu_add_col option[value="7"]').hide();
        $('#menu_add_col option[value="8"]').hide();
        $('#menu_add_col option[value="9"]').hide();
        $('#menu_add_col option[value="10"]').hide();
        $('#menu_add_col option[value="11"]').hide();
        col2 = $('#menu_add_col').val();
        if (col2 >= 6) {$('#menu_add_col option[value="1"]').prop('selected', true);}
    } else {
        /*$('#menu_add_col option[value="6"]').prop('disabled', false);*/
        $('#menu_add_col option[value="6"]').show();
        $('#menu_add_col option[value="7"]').show();
        $('#menu_add_col option[value="8"]').show();
        $('#menu_add_col option[value="9"]').show();
        $('#menu_add_col option[value="10"]').show();
        $('#menu_add_col option[value="11"]').show();

    }
}



function show(param) {
    var lang = langs();
    $('.show_'+param).show('200');
    $('.hide_'+param).hide('200');
    if (param == 8) {
        $('.table_header_8').removeClass('table_header_width').text(lang['index']['table']['1']);
        $('.table_header_8_1').removeClass('table_header_width').text('Evolution');
        $('.table_header_8_2').removeClass('table_header_width').text('EZugi');
    }
}
function hide(param) {
    $('.show_'+param).hide('200');
    $('.hide_'+param).show('200');
    if (param == 8) {
        $('.table_header_8').addClass('table_header_width').text('');
        $('.table_header_8_1').addClass('table_header_width').text('');
        $('.table_header_8_2').addClass('table_header_width').text('');
    }
}



function info_open(t,r) {
    //alert($('.info_'+r+'_info_zero:first').text()+' / '+$('.info_'+r+'_info_red:first').text()+' / '+$('.info_'+r+'_info_black:first').text()+' / ');
    if (!($('.info_'+r+'_info_zero:first').text() == '0%' && $('.info_'+r+'_info_red:first').text() == '0%' && $('.info_'+r+'_info_black:first').text() == '0%')) {
        $('.info').fadeOut("slow");
        dd = $('#info_'+t+'_'+r);
        if (dd.is(":visible")) {dd.fadeOut("slow");
        } else {
            $("dd:visible").fadeOut("slow");
            dd.fadeIn("slow");
        }
    } else {
        $('.info').fadeOut("slow");
    }

}


function menu_quit() {
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'quit'}),         
        dataType: "html",               
        success: function (data) {
            location.href=location.href;
        }        
    });
}

function user_add() {
    $('.user_panel_add').slideToggle(500);
    $('#user_input_login, #user_input_pass').removeClass('input_error');
    $('#user_edit').text('');
    $('#user_input_login').val('');
    $('#user_input_pass').val('');
    $('#user_input_level option[value="3"]').prop('selected', true);
}

function user_save() {    
    id = $('#user_edit').text();
    login = $('#user_input_login').val();
    pass = $('#user_input_pass').val();
    level = $('#user_input_level').val();
    if (login && (pass || id) && level) {
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'user_save', id: id, login: login, pass: pass, level: level}),         
            dataType: "html",               
            success: function (data) {
                location.href=location.href;
            }        
        });
    } else {
        if (!login) {$('#user_input_login').addClass('input_error');}
        if (!pass && !id) {$('#user_input_pass').addClass('input_error');}
    }    
}

function user_edit(id, login, level) {
    $('.user_panel_add').show(500);
    $('#user_edit').text(id);
    $('#user_input_login').val(login);
    $('#user_input_level option[value="'+level+'"]').prop('selected', true);
    $('body,html').animate({scrollTop: 0}, 400);  
}

function user_delete(id) {
    var lang = langs();
    if (confirm(lang['js']['user_delete']['1'])) {
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'user_delete', id: id}),         
            dataType: "html",               
            success: function (data) {
                location.href=location.href;
            }        
        });
    }    
}
function user_plus(id, param) { 
    var lang = langs();
    if (param == 1) {param_text = '1 '+lang['pro']['6'];}  
    else if (param == 7) {param_text = '1 '+lang['pro']['11'];}  
    else if (param == 30) {param_text = '1 '+lang['pro']['9'];}   
    if (confirm(lang['add']+" "+param_text+"?")) {
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'user_plus', id: id, param: param}),         
            dataType: "html",               
            success: function (data) {
                location.href=location.href; 
            }        
        });
    }    
}


//МЕНЮ открыть панель НАСТРОЕК
function menu_setting_open() {
    $('#menu_panel_setting').slideToggle('500');
}
//МЕНЮ панель НАСТРОЕК сохранение Кол-во раундов в статистике
function menu_setting_save() {
    $('#menu_panel_setting').slideToggle('500');
    info = $('#menu_setting_count').val();
    number_max = $('#menu_setting_number_max').val();
    if (info > 500) {info = 500;}
    if (number_max > 500) {number_max = 500;}
    if (info > 0 && info <= 500 && number_max > 0 && number_max <= 500) {
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_setting_save', info: info, number_max: number_max}),         
            dataType: "html",               
            success: function (data) {
                location.href=location.href;
            }        
        });
    }
}

//Страница setting изменение ошибок на странице
function setting(action, line) {
    param = $('#input_set_'+line).val();
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'setting', action: action, param: param, line: line}),         
        dataType: "html",               
        success: function (data) {
            location.href=location.href;
        }        
    });
}
// общая кнопка остановить/включить  рассылку в телеграм
function tel_send(action) {
    var lang = langs();
    zzz = 1;
    if (action == 3) {
        if (!confirm(lang['js']['tel_send']['1']+"?")) {zzz = 0;}//Вы действительно хотите удалить ваш id телеграм
    }
    if (zzz) {
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'tel_send', action: action}),         
            dataType: "html",               
            success: function (data) {     
                if (data == 2) {$('#menu_set_tel_send').html('<div class="menu_panel_p max color_white" onclick="tel_send(1)">'+lang['on']+'</div><i class="fa fa-pause color_gr fs_14 ml_10" onclick="tel_send(1)"></i><i class="fa fa-times color_red2 fs_14 ml_10" onclick="tel_send(3)"></i>');}
                else if (data == 1) {$('#menu_set_tel_send').html('<div class="menu_panel_p max" onclick="tel_send(2)">'+lang['off']+'</div><i class="fa fa-play fs_14 ml_10 color_white" onclick="tel_send(2)"></i><i class="fa fa-times color_red2 fs_14 ml_10" onclick="tel_send(3)"></i>');}
                else if (data == 3) {location.href=location.href;}
            }        
        });
    }
}

//страница настроек сайта - сбросить все числа во всех таблицах рулеток
function clean_table() {
    var lang = langs();
    if (confirm(lang['js']['clean_table']['1']+"?")) { //Очистить все таблицы рулеток
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'clean_table'}),         
            dataType: "html",               
            success: function (data) {
                $('#set_button_clean').text('ОК');
            }        
        });
    }
}



//страница user получить данные телеграма телефона
function user_info(param, user_id) {
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'user_info', param: param, user_id: user_id}),         
        dataType: "html",               
        success: function (data) {
            alert(data);
        }        
    });
}

function user_timer(param_rimer){
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'user_timer', param_timer: param_timer}),         
        dataType: "html",               
        success: function (data) {}        
    });
}

function user_partner(id) {
    $("#user_partner_"+id).removeClass('fa-id-card-o').addClass('fa-spinner fa-pulse');
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'user_partner', id: id}),         
        dataType: "html",               
        success: function (data) {
            location.href=location.href;
        }        
    });
}
function send_meassage_all() {
    var lang = langs();  
    if (confirm(lang['js']['send_meassage_all']['1']+"?")) {//Отправить сообщение
        mes = $('#send_meassage_all').val();
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'send_meassage_all', mes: mes}),         
            dataType: "html",               
            success: function (data) {
                $('#send_meassage_all').val('');
            }        
        });
    }
}

function add_new_ref_link() {
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'add_new_ref_link'}),         
        dataType: "html",               
        success: function (data) {
            if (data == 1) {
                //alert(data);
                add_new_ref_link();
            } else {
                location.href=location.href;
            }
        }        
    });
}


function tab(param) {
    $('.tab').hide(0);
    $('.tab_'+param).show(0);
    $('.tab_button').removeClass('tab_button_active');
    $('.tab_button_'+param).addClass('tab_button_active');
}

function set_promocode_user_add(promo) {//страница НАСТРОЙКИ САЙТА таб ПРОМО - добавить юзера в промо
    user  = $('#set_promocode_user_'+promo).val();
    if (user != 0) {
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'set_promocode_user_add', user: user, promo: promo}),         
            dataType: "html",               
            success: function (data) {
                $('.set_promocode_user option[value="0"]').prop('selected', true);
                $('#set_promocode_user_'+promo+' option[value="'+user+'"]').hide(0);
                $('#set_promocode_user_'+promo).parent().before(data);
            }        
        });

    }
}
function set_promocode_user_del(id, promo) {
    var lang = langs();  
    if (confirm(lang['js']['set_promocode_user_del']['1']+"?")) {//Удалить промо у партнера
        $.ajax ({ 
            url: "ajax", 
            type: "POST",         
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'set_promocode_user_del', id: id}),         
            dataType: "html",               
            success: function (data) {
                $('#set_promocode_user_del_'+id).detach();
                $('#set_promocode_user_'+promo).append(data);
                ee = $('#set_promocode_user_'+promo+' option').last().val();

            }        
        });
    }
}

function set_promocode_add() {
    $('#set_promocode_add_line').slideToggle(200);
    $('#set_promocode_add').slideToggle(200);
}

function set_promocode_add_save(param) {
    var lang = langs();  
    if (param){
        input1= $('#set_promocode_add_unput_1').val();
        input2= $('#set_promocode_add_unput_2').val();
        input3= $('#set_promocode_add_unput_3').val();
        id = $('#set_promocode_add_id').text();
        if(input1 && input2){
            $('#set_promocode_add_line').slideToggle(200);
            $('#set_promocode_add').html('<i class="fa fa-spinner fa-pulse fa-fw"></i>').slideToggle(200);
            $.ajax ({ 
                url: "ajax", 
                type: "POST",
                data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'set_promocode_add_save', id: id, input1: input1, input2: input2, input3: input3}),         
                dataType: "html",               
                success: function (data) {
                    $('#set_promocode_add').html(lang['js']['set_promocode_add_save']['1']);//Создать новый промо
                    $('#set_promocode_add_unput_1').val('');
                    $('#set_promocode_add_unput_2').val('');
                    $('#set_promocode_add_unput_3').val('');
                    $('#set_promocode_add_id').text('');
                    if (id) {
                        data = JSON.parse(data);
                        $('#set_promocode_name_'+id).text(data[1]);
                        $('#set_promocode_date_'+id).text(data[2]);
                        $('#set_promocode_pro_'+id).text('+'+data[3]+' дня');
                    } else {
                        $('#set_promocode_add_line').after(data);
                    }
                }        
            });
        }
    } else {
        $('#set_promocode_add_line').slideToggle(200);
        $('#set_promocode_add').slideToggle(200);
        $('#set_promocode_add_unput_1').val('');
        $('#set_promocode_add_unput_2').val('');
        $('#set_promocode_add_unput_3').val('');
        $('#set_promocode_add_id').text('');
    }
}

function set_promocode_del(id) {
    var lang = langs();  
    if (confirm(lang['js']['set_promocode_del']['1']+"?")) {
        $.ajax ({ 
            url: "ajax", 
            type: "POST",
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'set_promocode_del', id: id}),         
            dataType: "html",               
            success: function (data) {
                $('#set_promocode_'+id).detach();
            }        
        });
    }   
}
function set_promocode_edit(id, name, date, pro) {
    $('#set_promocode_add_line').slideToggle(200);
    $('#set_promocode_add').slideToggle(200);
    $('#set_promocode_add_unput_1').val(name);
    $('#set_promocode_add_unput_2').val(date);
    $('#set_promocode_add_unput_3').val(pro);
    $('#set_promocode_add_id').text(id);

}

function pro_active(param, price, desc) {
    var lang = langs();  
    $('.pro').removeClass('pro_active');
    $('#pro_'+param).addClass('pro_active');
    $('#submit').removeClass('line_button_no_active');
    $('#us_service').val(param);
    $('#sum').val(price);
    $('#desc').val(desc);
    //скрипт оплаты
    var min = 1;
    var re = /[^0-9\.]/gi;
    var url = window.location.href;
    var desc = $('#desc').val();
    var sum = $('#sum').val();
    if (re.test(sum)) {sum = sum.replace(re, ''); $('#oa').val(sum);}
    if (sum < min) { $('#error').html(lang['js']['pro_active']['1']+' '+min); $('#submit').attr("disabled", "disabled");return false;} //Сумма должна быть больше
    else {$('#error').html('');}
    if (desc.length < 1) {$('#error').html(lang['js']['pro_active']['2']); return false;}//Необходимо ввести номер заявки
    $.get(url+'?prepare_once=1&l='+desc+'&oa='+sum, function(data) {
        var re_anwer = /<hash>([0-9a-z]+)<\/hash>/gi;
        $('#s').val(re_anwer.exec(data)[1]);
        $('#submit').removeAttr("disabled");
    });
}
function  menu_user_info(action, param) {
    var lang = langs();  
    if (action == 2){
        if (param == 1) {text = lang['js']['menu_user_info']['1']+'?';}//Удалить номер телефона
        else if (param == 2) {text = lang['js']['menu_user_info']['2']+'?';} //Удалить телеграм
        if (confirm(text)) {
            $('#menu_user_info_'+param).text('');
            $.ajax ({ 
                url: "ajax", 
                type: "POST",
                data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_user_info', action: action, param: param}),         
                dataType: "html",               
                success: function (data) {             
                }        
            });
        }
    } else if (action == 1){ 
        $('.menu_user_info_input').detach();
        $('#menu_user_info_'+param).parent().after('<div class="cont cont_111 cont_hor cont_nowrap menu_user_info_input"><input type="text" id="menu_user_info_input_'+param+'"  class="line_input max" value=""><div class="menu_ico_button"  onclick="menu_user_info_save('+param+')"><i class="fa fa-floppy-o  menu_user_info_save"></i></div><i class="fa fa-times menu_ico_button bg_red" onclick="menu_user_info_cancel('+param+')"></i></div>');
    }
}
 
function menu_user_info_cancel(param){
    $('.menu_user_info_input').detach();
}
function menu_user_info_save(param){
    var lang = langs();  
    $('.menu_user_info_save').removeClass('fa-floppy-o').addClass('fa-spinner fa-pulse fa-fw');
    val = $('#menu_user_info_input_'+param).val();
    $.ajax ({ 
        url: "ajax", 
        type: "POST",
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_user_info_save', val: val, param: param}),         
        dataType: "html",               
        success: function (data) {  
            $('.menu_user_info_input').detach();  
            if (data == lang['ajax']['menu_user_info_save']['1']+'!'){
                alert(data);
            } else {
                $('#menu_user_info_'+param).text(data);
            }     
        }        
    });    
}

function partner_ref_more(refid) {
    $('.partner_ref_more').not('#partner_ref_more'+refid).slideUp(100);
    dd = $('#partner_ref_more_'+refid);
    if (dd.is(":visible")) {dd.fadeOut(100);//Открыть закрытое, закрыть открытое
    } else {
        $("dd:visible").fadeOut(100);
        dd.fadeIn(100);
    }
}

function partner_paid_more() {
    $('#partner_paid_now').slideUp(200);
    $('#partner_paid_more').slideToggle(200);
}

function partner_paid_now() {
    $('#partner_paid_more').slideUp(200);
    $('#partner_paid_now').slideToggle(200);
}

function partner_paid_score_del() {  
    var lang = langs();  
    if (confirm(lang['js']['partner_paid_score_del']['1']+"?")) {  //Вы действительно хотите удалить этот счет из памяти сайта?
        id = $('#partner_paid_now_select').val();
        $.ajax ({ 
            url: "ajax", 
            type: "POST",
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'partner_paid_score_del', id: id}),         
            dataType: "html",               
            success: function (data) {
                $('#partner_paid_now_select option[value="0"]').prop('selected', true); 
                $('#partner_paid_now_select option[value="'+id+'"]').detach();
                $('#partner_paid_now_new').show();
                $('#partner_paid_button_del').hide();
            }        
        });  
    }
}

function partner_paid_button_cancel() {
    $('#partner_paid_now').slideUp(200);
}

function partner_paid_button_paid() {
    var lang = langs();  
    score = $('#partner_paid_now_select').val();
    money = $('#partner_paid_now_sum').val();
    score_type = $('#partner_paid_now_type').val();
    score_number = $('#partner_paid_now_number').val();
    if (($('#partner_paid_now_select').length && score != 0) || score_number){
        if ($('#partner_paid_phone').length) {phone = $('#partner_user_phone').val();} else {phone = '';}
        if ($('#partner_paid_phone').length && !phone){
            alert(lang['js']['partner_paid_button_paid']['1']);//Строка "телефон" обязательна для заполнения
        } else {
            $.ajax ({ 
                url: "ajax", 
                type: "POST",
                data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'partner_paid_button_paid', score: score, money: money, score_type: score_type, score_number: score_number, phone: phone}),         
                dataType: "html",               
                success: function (data) {
                    if (data){
                        alert(data);
                    } else {
                        location.href=location.href;
                    }
                }        
            });
        }
    } else {
        alert(lang['js']['partner_paid_button_paid']['2']);//Строка "номер" обязательна для заполнения
    }
}

function partner_ref_edit(refid) {
    $('.partner_ref_edit_show_'+refid).show(0);
    $('.partner_ref_edit_hide_'+refid).hide(0);
    $('.partner_ref_edit_hide_'+refid+'_source').hide(0);
    $('.partner_ref_edit_hide_'+refid+'_comment').hide(0);
}

function partner_ref_edit_cancel(refid) {
    $('.partner_ref_edit_show_'+refid).hide(0);
    $('.partner_ref_edit_hide_'+refid).show(0);
    if ($('.partner_ref_edit_hide_'+refid+'_source').hasClass('source_show')) {$('.partner_ref_edit_hide_'+refid+'_source').show(0);}
    if ($('.partner_ref_edit_hide_'+refid+'_comment').hasClass('comment_show')) {$('.partner_ref_edit_hide_'+refid+'_comment').show(0);}
}
 
function partner_ref_edit_save(refid) {
    promo = $('#partner_ref_edit_promo_'+refid).val();
    promo_text = $('#partner_ref_edit_promo_'+refid+' option:selected').text();
    source = $('#partner_ref_edit_source_'+refid).val();
    comment = $('#partner_ref_edit_comment_'+refid).val();
    $.ajax ({ 
        url: "ajax", 
        type: "POST",
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'partner_ref_edit_save', promo: promo, source: source, comment: comment, refid: refid}),         
        dataType: "html",               
        success: function (data) {
            if (data){
                alert(data);
            } else {
                $('#partner_ref_edit_promo_text_'+refid).text(promo_text);
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
        }        
    });  

}

function setting_partner_percent_edit(id, percent) {
    var lang = langs();  
    new_percent = prompt(lang['js']['setting_partner_percent_edit']['1']+':', percent);
    if (new_percent != percent && new_percent){
        $.ajax ({ 
            url: "ajax", 
            type: "POST",
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'setting_partner_percent_edit', id: id, new_percent: new_percent}),         
            dataType: "html",               
            success: function (data) {
                if (data){
                    alert(data);
                } else {
                    $('#setting_partner_percent_edit_'+id).html(new_percent+'%');
                }
            }        
        });
    }
}
function setting_partner_paid(id) {
    var lang = langs();  
    if (confirm(lang['js']['setting_partner_paid']['1']+"?")) {//Выплаченно
        $.ajax ({ 
            url: "ajax", 
            type: "POST",
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'setting_partner_paid', id: id}),         
            dataType: "html",               
            success: function (data) {
                if (data){ alert(data);}
                $('#setting_partner_paid_'+id).detach();              
            }        
        });
    }
}

function partner_ref_delete(refid) {
    var lang = langs();  
    if (confirm(lang['js']['partner_ref_delete']['1']+"?")) {//Удалить реферальную ссылку?
        $.ajax ({ 
            url: "ajax", 
            type: "POST",
            data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'partner_ref_delete', refid: refid}),         
            dataType: "html",               
            success: function (data) {    
                if (data){
                    alert(data);
                }
                $('#partner_ref_'+refid).detach();                  
            }        
        });
    }
}

function language(lang) {
    $.ajax ({ 
        url: "ajax", 
        type: "POST",
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'language', lang: lang}),         
        dataType: "html",               
        success: function (data) {    
            location.href=location.href;                
        }        
    });
}