<?php
  header("Content-Type:image/png");

  $image_id = $_GET["image_id"];

  if($image_id == 0)
    $ms = 0;
  if($image_id == 1)
    $ms = 0;
  elseif($image_id == 2)
    $ms = 4;
  elseif($image_id == 3)
    $ms = 1;
  elseif($image_id == 4)
    $ms = 8;
  elseif($image_id == 5)
    $ms = 0;
  elseif($image_id == 6)
    $ms = 7;
  elseif($image_id == 7)
    $ms = 7;
  elseif($image_id == 8)
    $ms = 6;
  elseif($image_id == 9)
    $ms = 6;
  elseif($image_id == 10)
    $ms = 1;
  elseif($image_id == 11)
    $ms = 3;
  elseif($image_id == 12)
    $ms = 0;
  elseif($image_id == 13)
    $ms = 1;
  elseif($image_id == 14)
    $ms = 7;
  elseif($image_id == 15)
    $ms = 8;
  elseif($image_id == 16)
    $ms = 8;
  elseif($image_id == 17)
    $ms = 6;
  elseif($image_id == 18)
    $ms = 7;
  elseif($image_id == 19)
    $ms = 9;
  elseif($image_id == 20)
    $ms = 6;
  elseif($image_id == 21)
    $ms = 9;
  elseif($image_id == 22)
    $ms = 8;
  elseif($image_id == 23)
    $ms = 0;
  elseif($image_id == 24)
    $ms = 1;
  elseif($image_id == 25)
    $ms = 5;
  elseif($image_id == 26)
    $ms = 0;
  elseif($image_id == 27)
    $ms = 1;
  elseif($image_id == 28)
    $ms = 5;
  elseif($image_id == 29)
    $ms = 0;
  elseif($image_id == 30)
    $ms = 8;
  elseif($image_id == 31)
    $ms = 6;
  elseif($image_id == 32)
    $ms = 7;
  elseif($image_id == 33)
    $ms = 0;
  elseif($image_id == 34)
    $ms = 0;
  elseif($image_id == 35)
    $ms = 1;
  elseif($image_id == 36)
    $ms = 8;
  elseif($image_id == 37)
    $ms = 5;
  elseif($image_id == 38)
    $ms = 6;
  elseif($image_id == 39)
    $ms = 6;
  elseif($image_id == 40)
    $ms = 7;
  elseif($image_id == 41)
    $ms = 7;
  elseif($image_id == 42)
    $ms = 3;
  elseif($image_id == 43)
    $ms = 2;
  elseif($image_id == 44)
    $ms = 0;
  elseif($image_id == 45)
    $ms = 0;
  elseif($image_id == 46)
    $ms = 1;
  elseif($image_id == 47)
    $ms = 9;
  elseif($image_id == 48)
    $ms = 0;
  elseif($image_id == 49)
    $ms = 0;
  elseif($image_id == 50)
    $ms = 0;
  else
    $ms = rand(0,9);

  usleep( $ms * 4 * 1000 );

  if($image_id < 0)
    $image_id = 0;

  $theImage = "./img/". ($image_id % 19) .".png";
  if(is_file($theImage))
    echo file_get_contents($theImage);
?>