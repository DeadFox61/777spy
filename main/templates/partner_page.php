<?php
if ($user_id AND $user[partner_on]) {
    echo '
    <div class="user_width tab_box mt_40">
        <div class="cont cont_111 cont_hor cont_nowrap">
            <div class="tab_button tab_button_active tab_button_1 max" onclick="tab(1)">'.$text[partner][tabs][1].'</div>
            <div class="tab_button_separator"></div>
            <div class="tab_button tab_button_4 max" onclick="tab(4)">'.$text[partner][tabs][2].'</div>
            <div class="tab_button_separator"></div>
            <div class="tab_button tab_button_3 max" onclick="tab(3)">'.$text[partner][tabs][3].'</div>
            <div class="tab_button_separator"></div>
            <div class="tab_button tab_button_2 max" onclick="tab(2)">'.$text[partner][tabs][4].'</div>
        </div>
        <div class="tab tab_1">';
            $sum_0 = mysqli_fetch_row(mysqli_query($CONNECT, "SELECT SUM(money) FROM partner WHERE paid = 0 AND user_id = '$user_id'"));
            $sum_1 = mysqli_fetch_row(mysqli_query($CONNECT, "SELECT SUM(money) FROM partner WHERE paid = 1 AND user_id = '$user_id'"));
            $sum_2 = mysqli_fetch_row(mysqli_query($CONNECT, "SELECT SUM(money) FROM partner WHERE paid = 2 AND user_id = '$user_id'")); 
            $user_money[paid_no] = 0 + $sum_0[0];
            $user_money[paid_wait] = 0 + $sum_1[0];
            $user_money[paid] = 0 + $sum_2[0];
            $user_money[all] = 0 + $sum_0[0] + $sum_1[0] + $sum_2[0];            
            $sql77 = mysqli_query($CONNECT, "SELECT * FROM refid_link WHERE user_id = '$user_id' ORDER BY id");
            while($row77 = mysqli_fetch_assoc($sql77) ){
                $sum77_link = mysqli_fetch_row(mysqli_query($CONNECT, "SELECT COUNT(1) FROM refid WHERE refid = '$row77[link]' AND user = 0"));                 
                $sum_refid[link] += $sum77_link[0];  
                $sum77_reg = mysqli_fetch_row(mysqli_query($CONNECT, "SELECT COUNT(1) FROM refid WHERE refid = '$row77[link]' AND user != 0"));                 
                $sum_refid[reg] += $sum77_reg[0];                
            }
            echo '
            <div class="cont cont_111 cont_nowrap cont_hor">
                <div class="line_border max bg_white">
                    <div class="title">'.$sum_refid[link].'</div>
                    <div class="text tac mb_20 fs_16">'.$text[partner][tab_1][1].'</div>
                </div>                       
                <div class="line_border max ml_20 bg_white">
                    <div class="title">'.$sum_refid[reg].'</div>
                    <div class="text tac mb_20 fs_16">'.$text[partner][tab_1][2].'</div>
                </div>  
                <div class="line_border max ml_20 bg_white">
                    <div class="title">'.$user_money[all].'</div>
                    <div class="text tac mb_20 fs_16">'.$text[partner][tab_1][3].'</div>
                </div>
            </div>';
            /* 
            echo '<div class="tab_title mt_20">Пополнения по реферальным ссылкам</div>
            <div class="cont cont_111 cont_nowrap cont_hor mt_20">
                <div class="line_p width_18">Дата:</div>
                <div class="line_p max">Почта пользователя:</div>
                <div class="line_p width_25 fs_13">Реферальная ссылка пользователя:</div>
                <div class="line_p width_10 tar">Прибыль</div>
            </div>';
            $sql = mysqli_query($CONNECT, "SELECT * FROM buy WHERE refid_user_id = $user_id ORDER BY id DESC");
            while($row = mysqli_fetch_assoc($sql) ){
                $part_money = $row[money]/ 100 * $user[partner_percent];  
                $part_user = mysqli_fetch_assoc(mysqli_query($CONNECT, "SELECT * FROM user WHERE id = '$row[user_id]'"));                   
                echo '
                <div class="cont cont_111 cont_nowrap cont_hor line mb_20">
                    <div class="line_text width_18">'.$row[date].'</div>
                    <div class="line_separator"></div>
                    <div class="line_text max">'.hidestring($part_user[login]).'</div>
                    <div class="line_separator"></div>
                    <div class="line_text width_25 fs_13">https://777spy.ru/?refid='.$row[refid].'</div>
                    <div class="line_separator"></div>
                    <div class="line_text width_10 tar">'.$part_money.'</div>
                </div>';
            }  */          
        echo '
        </div>
        <div class="tab tab_4 display_none">';
            echo '
            <div class="cont cont_111 cont_nowrap cont_hor">
                <div class="line_border max bg_white">
                    <div class="title">'.$user_money[paid_no].'</div>
                    <div class="text tac mb_20 fs_16">'.$text[partner][tab_4][1].'</div>
                </div>                       
                <div class="line_border max ml_20 bg_white">
                    <div class="title">'.$user_money[all].'</div>
                    <div class="text tac mb_20 fs_16">'.$text[partner][tab_4][2].'</div>
                </div>  
            </div>';
            $paid_0 = mysqli_fetch_row(mysqli_query($CONNECT, "SELECT COUNT(1) FROM partner WHERE user_id = $user_id AND paid = 0")); 
            $paid_other = mysqli_fetch_row(mysqli_query($CONNECT, "SELECT COUNT(1) FROM partner WHERE user_id = $user_id AND paid > 0")); 
            if ($paid_other[0] OR $paid_0[0]) {
                echo '
                <div class="cont cont_111 cont_nowrap cont_hor mt_20">';
                    if ($paid_0[0]) {echo '<div class="line_button fs_13" onclick="partner_paid_now()">'.mb_strtoupper($text[partner][tab_4][3], 'UTF-8').'</div> ';}//ЗАКАЗАТЬ ВЫПЛАТУ
                    echo '<div class="max"></div>';
                    if ($paid_other[0]) {echo '<div class="line_button ml_20 fs_13" onclick="partner_paid_more()">'.mb_strtoupper($text[partner][tab_4][4], 'UTF-8').'</div>';} //ВЫПЛАТЫ
                echo '
                </div>
                <div class="display_none " id="partner_paid_now">
                    <div class="cont cont_111 cont_nowrap cont_hor line mt_20">
                        <div class="line_title">'.$text[partner][tab_4][5].':</div>
                        <div class="line_separator"></div>
                        <input type="text" class="line_input max" placeholder="" value="'.$user_money[paid_no].'" id="partner_paid_now_sum">
                    </div>';
                    $partner_score_count = mysqli_fetch_row(mysqli_query($CONNECT, "SELECT COUNT(1) FROM partner_score WHERE user_id = '$user_id'")); 
                    if ($partner_score_count[0]) {
                        echo  '                        
                        <div class="cont cont_111 cont_nowrap cont_hor line mt_20">
                            <div class="line_title">'.$text[partner][tab_4][6].':</div>
                            <div class="line_separator"></div>
                            <select id="partner_paid_now_select" class="line_input max" >';
                                $sql_score = mysqli_query($CONNECT, "SELECT * FROM partner_score WHERE user_id = '$user_id' ORDER BY data_last_paid DESC");
                                while($row_score = mysqli_fetch_assoc($sql_score) ){
                                    if ($row_score[type] == 1) {$score_type = $text[partner][tab_4][7];}
                                    else if ($row_score[type] == 2) {$score_type = $text[partner][tab_4][8];}
                                    echo '<option value="'.$row_score[id].'" class="line_option">'.$score_type.': '.srore_hide($row_score[score], $row_score[type]).'</option>';
                                }
                            echo '
                                <option value="0" class="line_option">'.$text[partner][tab_4][9].'</option>
                            </select>
                            <div class="line_button fs_11" onclick="partner_paid_score_del()" id="partner_paid_button_del">'.mb_strtoupper($text[partner][tab_4][10], 'UTF-8').'</div>
                        </div>';
                        $css_partner_paid_now_new = ' display_none ';
                    }
                    echo  '                        
                    <div class="mt_20 '.$css_partner_paid_now_new.'" id="partner_paid_now_new">
                        <div class="cont cont_111 cont_nowrap cont_hor line">
                            <div class="line_title">'.$text[partner][tab_4][11].':</div>
                            <div class="line_separator"></div>
                            <select id="partner_paid_now_type" class="line_input max" >
                                <option value="1" class="line_option">'.$text[partner][tab_4][7].' ('.$text[partner][tab_4][12].' 3,5%)</option>
                                <option value="2" class="line_option">'.$text[partner][tab_4][8].' ('.$text[partner][tab_4][12].' 2%)</option>
                            </select>
                            <div class="line_separator"></div>
                            <div class="line_title">'.$text[partner][tab_4][13].':</div>
                            <div class="line_separator"></div>
                            <input type="text" class="line_input max" placeholder="" id="partner_paid_now_number">
                        </div>
                    </div>';
                    if (!$user[phone]) {
                        echo  '              
                        <div class="cont cont_111 cont_nowrap cont_hor line mt_20" id="partner_paid_phone">
                            <div class="line_title">'.$text[phone].':</div>
                            <div class="line_separator"></div>
                            <input type="text" class="line_input max" placeholder="'.$text[partner][tab_4][14].'" id="partner_user_phone">
                        </div>';
                    }
                    echo '
                    <div class="cont cont_001 cont_nowrap cont_hor mt_20">
                        <div class="line_button fs_13" onclick="partner_paid_button_paid()">'.mb_strtoupper($text[partner][tab_4][15], 'UTF-8').'</div>
                        <div class="line_button fs_13 ml_20 bg_red" onclick="partner_paid_button_cancel()">'.mb_strtoupper($text[cancel], 'UTF-8').'</div>
                    </div>
                </div>
                <div class="display_none" id="partner_paid_more">';
                    echo '
                        <div class="cont cont_111 cont_nowrap cont_hor ">
                            <div class="line_p width_18">'.$text[date].'</div>
                            <div class="line_p max tar">'.$text[partner][tab_4][16].'</div>
                        </div>';
                        $sql = mysqli_query($CONNECT, "SELECT * FROM partner WHERE user_id = $user_id AND paid > 0 ORDER BY paid ASC, paid_date DESC, id DESC");
                        while($row = mysqli_fetch_assoc($sql) ){
                            echo '
                            <div class="cont cont_111 cont_nowrap cont_hor mb_10 line">
                                <div class="line_title width_18">';
                                    if ($row[paid] == 2) {echo $row[paid_date];}
                                    else if ($row[paid] == 1) {echo $text[partner][tab_4][17];}
                                echo '
                                </div>
                                <div class="line_separator"></div>
                                <div class="line_text max tar">'.$row[money].'</div>
                            </div>';
                        }                                
                echo '
                </div>';
            }
        echo '    
        </div>
        <div class="tab tab_2 display_none">';
            $sql = mysqli_query($CONNECT, "SELECT * FROM promo_user WHERE user_id = '$user_id' ORDER BY id");
            while($row = mysqli_fetch_assoc($sql) ){
                $prom = mysqli_fetch_assoc(mysqli_query($CONNECT, "SELECT * FROM promo WHERE id = '$row[promo_id]'")); 
                if (strtotime($prom[date]) > strtotime('now')) {
                    $prom_on = true;
                    echo '
                    <div class="line cont cont_111 cont_nowrap cont_hor mt_20">
                        <div class="line_title">'.$text[partner][tabs][4].': '.$prom[name].'</div>
                        <div class="u_line_text max fs_14">+'.$prom[pro_day].' '.$text[partner][tab_2][1].'</div>
                        <div class="line_separator"></div>
                        <div class="u_line_text fs_14">'.$text[partner][tab_2][2].' '.$prom[date].'</div>
                    </div>';
                }
            }
            if (!$prom_on) {echo '<div class="tab_p tac">'.$text[partner][tab_2][3].'</div>';}
        echo '
        </div>
        <div class="tab tab_3 display_none">';
            $sql = mysqli_query($CONNECT, "SELECT * FROM refid_link WHERE user_id = '$user_id' ORDER BY id DESC");
            while($row = mysqli_fetch_assoc($sql) ){
                $sum_refid_link_one = mysqli_fetch_row(mysqli_query($CONNECT, "SELECT COUNT(1) FROM refid WHERE refid = '$row[link]' AND user = 0"));    
                $sum_refid_reg_one =  mysqli_fetch_row(mysqli_query($CONNECT, "SELECT COUNT(1) FROM refid WHERE refid = '$row[link]' AND user != 0")); 
                $refid_plus_promo = mysqli_fetch_assoc(mysqli_query($CONNECT, "SELECT * FROM promo_plus_refid WHERE refid_id = '$row[link]'"));
                $refid_plus_promo_name = mysqli_fetch_assoc(mysqli_query($CONNECT, "SELECT * FROM promo WHERE id = '$refid_plus_promo[promo_id]'"));

                echo '
                <div class="line_box mt_40" id="partner_ref_'.$row[link].'">
                    <div class=" cont cont_111 cont_nowrap cont_hor line_box_title pt_20_pl_20">
                        <div class="u_clear">'.$text[partner][tab_3][1].':</div>
                        <div class="u_clear tar max">https://777spy.ru/?refid='.$row[link].'</div>
                    </div>
                    <div class="padding_20">
                        <div class=" cont cont_111 cont_nowrap cont_hor">
                            <div class="line_p max partner_ref_edit_hide_'.$row[link].'">'.$text[partner][tab_3][2].': '.$sum_refid_link_one[0].'</div>
                            <div class="line_p max partner_ref_edit_hide_'.$row[link].'">'.$text[reg].': '.$sum_refid_reg_one[0].'</div>                           
                            <div class="line_p ">'.$text[partner][tabs][4].': </div>  
                            <span class="line_p p_0 max partner_ref_edit_hide_'.$row[link].' " id="partner_ref_edit_promo_text_'.$row[link].'">'.$refid_plus_promo_name[name].'</span>
                            <select class="line_border line_input max partner_ref_edit_show partner_ref_edit_show_'.$row[link].'"  id="partner_ref_edit_promo_'.$row[link].'">
                                <option value="0"></option>'; 
                                $xxx_sql = mysqli_query($CONNECT, "SELECT * FROM promo_user WHERE user_id = '$user_id' ORDER BY id");
                                while($xxx = mysqli_fetch_assoc($xxx_sql) ){
                                    $yyy = mysqli_fetch_assoc(mysqli_query($CONNECT, "SELECT * FROM promo WHERE id = $xxx[promo_id]")); 
                                    if (strtotime($yyy[date]) > strtotime('now')) {                                        
                                        $zzz = mysqli_fetch_assoc(mysqli_query($CONNECT, "SELECT * FROM promo_plus_refid WHERE refid_id = '$row[link]' AND promo_id = '$yyy[id]'"));
                                        if ($zzz[id]) {$yyyy = ' selected  ';} else {$yyyy = '  ';}
                                        echo '<option '.$yyyy.' value="'.$yyy[id].'">'.$yyy[name].'</option>';
                                    }
                                }                            
                            echo '
                            </select>
                            <div class="line_i pt_10_pl_10 bg_green cursor color_white partner_ref_edit_hide_'.$row[link].'" onclick="partner_ref_edit(&quot;'.$row[link].'&quot;)"><i class="fa fa-pencil"></i></div>';
                            $count_link = mysqli_fetch_row(mysqli_query($CONNECT, "SELECT COUNT(1) FROM refid WHERE refid = '$row[link]'")); 
                            if ($count_link[0]) {echo '<div class="line_i pt_10_pl_10 bg_green cursor color_white ml_10 partner_ref_edit_hide_'.$row[link].'" onclick="partner_ref_more(&quot;'.$row[link].'&quot;)"><i class="fa fa-angle-double-down"></i></div>';}
                            if (!$count_link[0]) {echo '<div class="line_i pt_10_pl_10 bg_red cursor color_white ml_10 partner_ref_edit_hide_'.$row[link].'" onclick="partner_ref_delete(&quot;'.$row[link].'&quot;)"><i class="fa fa-trash-o"></i></div>';}
                        echo '
                        </div>';
                        if ($row[source]) {$css_source = ' source_show ';} else {$css_source = ' display_none  ';}
                        echo '
                        <div class=" mt_10 '.$css_source.' partner_ref_edit_hide_'.$row[link].'_source">
                            <div class="cont cont_111 cont_nowrap cont_hor">
                                <div class="line_p">Источник:</div>
                                <div class="line_p p_0 max partner_ref_edit_hide_'.$row[link].'" id="partner_ref_edit_source_text_'.$row[link].'">'.$row[source].'</div>                                    
                            </div>                            
                        </div>
                        <div class="mt_10 partner_ref_edit_show partner_ref_edit_show_'.$row[link].'">
                            <div class="cont cont_111 cont_nowrap cont_hor">
                                <div class="line_p">Источник:</div>
                                <input type="text" class="line_input line_border max partner_ref_edit_show partner_ref_edit_show_'.$row[link].'" value="'.$row[source].'" id="partner_ref_edit_source_'.$row[link].'">
                            </div>
                        </div>';   
                        if ($row[comment]) {$css_comment = ' comment_show ';} else {$css_comment = ' display_none  ';}
                        echo '
                        <div class=" mt_10 '.$css_comment.' partner_ref_edit_hide_'.$row[link].'_comment">
                            <div class="cont cont_111 cont_nowrap cont_hor">
                                <div class="line_p">'.$text[partner][tab_3][3].':</div>
                                <div class="line_p p_0 max partner_ref_edit_hide_'.$row[link].'" id="partner_ref_edit_comment_text_'.$row[link].'">'.$row[comment].'</div>                                    
                            </div>                            
                        </div>
                        <div class="mt_10 partner_ref_edit_show partner_ref_edit_show_'.$row[link].'">
                            <div class="cont cont_111 cont_nowrap cont_hor">
                                <div class="line_p">'.$text[partner][tab_3][3].':</div>
                                <input type="text" class="line_input line_border max partner_ref_edit_show partner_ref_edit_show_'.$row[link].'" value="'.$row[comment].'" id="partner_ref_edit_comment_'.$row[link].'">
                            </div>
                        </div>
                        <div class=" partner_ref_edit_show partner_ref_edit_show_'.$row[link].' mt_10">
                            <div class=" cont cont_001 cont_nowrap cont_hor">
                                <div class="line_button" onclick="partner_ref_edit_save(&quot;'.$row[link].'&quot;)">'.mb_strtoupper($text[save], 'UTF-8').'</div>
                                <div class="line_button bg_red ml_10" onclick="partner_ref_edit_cancel(&quot;'.$row[link].'&quot;)">'.mb_strtoupper($text[cancel], 'UTF-8').'</div>
                            </div>
                        </div>
                        <div class="partner_ref_more display_none fs_13 mt_10 " id="partner_ref_more_'.$row[link].'">
                            <div class="tab_hr mb_10"></div>';
                            $sql2 = mysqli_query($CONNECT, "SELECT * FROM refid WHERE refid = '$row[link]' ORDER BY active DESC, date DESC");
                            while($row2 = mysqli_fetch_assoc($sql2) ){
                                if ($row2[active]) {
                                    $xxff = mysqli_fetch_assoc(mysqli_query($CONNECT, "SELECT * FROM user WHERE id = '$row2[user]'"));                                 
                                    echo '
                                    <div class=" cont cont_100 cont_nowrap cont_hor mt_m10 ">
                                        <div class="line_p width_15">'.$text[reg].'</div>
                                        <div class="line_p width_15">'.$row2[date].'</div>
                                        <div class="line_p width_20">Ip: '.$row2[ip].'</div>
                                        <div class="line_p width_20"><span class="line_span fs_12">'.$text[mail].': </span> '.hidestring($xxff[login]).'</div>
                                    </div>';                            
                                } else {
                                    echo '
                                    <div class=" cont cont_100 cont_nowrap cont_hor mt_m10 ">
                                        <div class="line_p width_15">'.$text[partner][tab_3][4].'</div>
                                        <div class="line_p width_15">'.$row2[date].'</div>
                                        <div class="line_p width_20">Ip: '.$row2[ip].'</div>
                                    </div>'; 
                                }
                            }                        
                        echo '
                        </div>
                    </div>
                </div>';            
            }     
            echo '        
            <div class="cont cont_001 cont_nowrap cont_hor mt_20">
                <div class="u_button" onclick="add_new_ref_link()">'.$text[partner][tab_3][5].'</div>
            </div>';
        echo '
        </div>';   
    echo '
    </div>';
} 
?>