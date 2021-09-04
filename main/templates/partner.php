<?php 
include_once 'config.php';
if ($user_id AND $user[partner_on]) {
    include_once 'function.php';
    include_once 'header.php';
    include_once 'partner_page.php'; 
    include_once 'footer.php'; 
} else {
    header("Location: https://stat.777spy.ru");
} 
?> 