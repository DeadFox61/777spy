$(document).ready(function () {  
    menu_rules_show();
    menu_rules_show_bacc();
    


    $("#menu_add_tables").on("input",function() {
        menu_check_select();
    }); 

    setInterval(function(){
        add_sec()
    },1000);
    update_stats();
    update_stats_bacc();

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
                if(stat.ind_stats)
                    write_if_not_writen('#row_no_'+stat.roul_id+'_fav',stat.ind_stats.fav_num,rules_data,10,false);  
                
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

//МЕНЮ изменить любимые числа
function menu_fav_num_switch(param){
    turned_on = $('.menu_num_table_ico_'+param).hasClass('fa-check');

    $('.menu_num_table_ico_'+param).addClass('fa-spinner fa-pulse').removeClass('fa-check').removeClass('fa-times');
    $.ajax ({ 
        url: "change_fav_num", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'menu_fav_num_switch', num: param}),         
        dataType: "json",               
        success: function (data) {
            $('.menu_num_table_ico_'+param).removeClass('fa-spinner').removeClass('fa-pulse');
            if(turned_on){
                $('.menu_num_table_ico_'+param).addClass('fa-times');
                $('.menu_num_table_ico_'+param).parent().addClass('menu_check_line_off');
            }
            else{
                $('.menu_num_table_ico_'+param).addClass('fa-check');
                 $('.menu_num_table_ico_'+param).parent().removeClass('menu_check_line_off');
            }
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

function menu_quit() {
    $.ajax ({ 
        url: "ajax", 
        type: "POST",         
        data: ({csrfmiddlewaretoken: window.CSRF_TOKEN, type: 'quit'}),         
        dataType: "json",               
        success: function (data) {
            location.href=location.href;
        }        
    });
}

// функции редактирования информации в меню
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