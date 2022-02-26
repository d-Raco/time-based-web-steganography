<?php
  header("Content-Type:image/png");

  $image_id = $_GET["image_id"];

  if($image_id == 0)
    $ms = 2;
  elseif($image_id == 1)
    $ms = 104;
  elseif($image_id == 2)
    $ms = 111;
  elseif($image_id == 3)
    $ms = 108;
  elseif($image_id == 4)
    $ms = 97;
  elseif($image_id == 5)
    $ms = 32;
  elseif($image_id == 6)
    $ms = 54;
  elseif($image_id == 7)
    $ms = 49;
  elseif($image_id == 8)
    $ms = 32;
  elseif($image_id == 9)
    $ms = 43;
  elseif($image_id == 10)
    $ms = 39;
  elseif($image_id == 11)
    $ms = 191;
  elseif($image_id == 12)
    $ms = 47;
  elseif($image_id == 13)
    $ms = 106;
  elseif($image_id == 14)
    $ms = 100;
  elseif($image_id == 15)
    $ms = 64;
  elseif($image_id == 16)
    $ms = 126;
  elseif($image_id == 17)
    $ms = 38;
  elseif($image_id == 18)
    $ms = 3;
  else
    $ms = rand(65,122);

  usleep( $ms * 12 * 1000 );

  if($image_id < 0)
    $image_id = 0;

  $theImage = "./img/". ($image_id % 7) .".jpg";
  if(is_file($theImage))
    echo file_get_contents($theImage);
?>