import os, os.path, sys, argparse

images_per_char = 2

def generate_HTML(num):
    #HTML file

    # Open file index.html (frontend of the webpage)
    f = open("index.html", "w")

    # Write the header of index.html
    f.write('<!DOCTYPE html>\n<html lang="en" dir="ltr">\n  <head>\n    <meta charset="utf-8">\n    <title>Enterprise icons store</title>\n  </head>\n  <body>\n    <h1>Enterprise icons store:</h1>\n')

    # Create as many HTML <img> elements as specified by the arguments passed to the program
    for j in range (0, num):
        f.write('    <img id="' + str(j) + '" src="./image.php?image_id=' + str(j) + '" width="64" height="64">\n')

    # Finish the file and close
    f.write('  </body>\n</html>')
    f.close()


def dec_to_base(num, base):  #Maximum base - 36
    base_num = ""
    while num>0:
        dig = int(num%base)
        if dig<10:
            base_num += str(dig)
        else:
            base_num += chr(ord('A')+dig-10)  #Using uppercase letters
        num //= base

    base_num = base_num[::-1]  #To reverse the string
    return base_num


def generate_PHP(msg):
    #PHP file

    # Open the file image.php (backend of the webpage, in charge of serving the images with a specific delay)
    f = open("image.php", "w")

    # Write the header of image.php and get the value of "image_id" from the URL
    f.write('<?php\n  header("Content-Type:image/png");\n\n  $image_id = $_GET["image_id"];\n\n')

    # If it is the images before the message itself, have a delay of 10
    f.write('  if($image_id == 0)\n    $ms = 10;\n')
    f.write('  if($image_id == 1)\n    $ms = 10;\n')

    base = 11

    # For each character of the message, specify the delay of the corresponding images using the ascii value of the character itslef
    for i in range (images_per_char, (len(msg)+images_per_char)):
        f.write('  elseif($image_id == ' + str(2*i - 2) + ')\n    $ms = ' + str(int(dec_to_base((ord(msg[i-images_per_char])-32), base).rjust(2, '0')[0], base)) + ';\n')
        f.write('  elseif($image_id == ' + str(2*i - 1) + ')\n    $ms = ' + str(int(dec_to_base((ord(msg[i-images_per_char])-32), base).rjust(2, '0')[1], base)) + ';\n')

    # If it is the images after the message itself, have a delay of 10
    f.write('  elseif($image_id == ' + str((len(msg)+1) * images_per_char) + ')\n    $ms = 10;\n')
    f.write('  elseif($image_id == ' + str((len(msg)+1) * images_per_char+1) + ')\n    $ms = 10;\n')

    # If it is any additional image, have a random delay
    f.write('  else\n    $ms = rand(0,10);\n\n')

    # Sleep as many milliseconds as specified; usleep is specified by microseconds, so multiply by 1000; also multiply by 100 to have more delay, making it more robust
    f.write('  usleep( $ms * 100 * 1000 );\n\n')

    # Check how many images there are under the "img" directory
    img_dir = './img'
    img_num = len([name for name in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, name))])

    # If "image_id" is negative, change it to 0
    f.write('  if($image_id < 0)\n    $image_id = 0;\n\n')

    # Serve an image from the "img" directory following this logic: $image_id % img_num + ".jpg"; note that the name of the images is a number starting from 0 and going up
    f.write('  $theImage = "./img/". ($image_id % ' + str(img_num) + ') .".png";\n  if(is_file($theImage))\n    echo file_get_contents($theImage);\n?>')
    f.close()


if __name__ == '__main__':
    # Parse the arguments passed to the program
    parser = argparse.ArgumentParser(description='Generate the Stego page')
    parser.add_argument('-msg', type=str, required=True, help='the message to hide')
    parser.add_argument('-num', type=int, default=100, help='the number of images displayed in the page (one character is added before and after the message, so len(msg)+2*2 is the minimum number of images needed); Default: 100; If a number less than or equal to 0 is provided, the exact minimum number of images needed to hide the message will be displayed.')

    args = parser.parse_args()
    msg = args.msg
    num = args.num

    if (num <= 0):
        num = (len(msg) + 2) * images_per_char
    if (((len(msg) + 2) * images_per_char) > num):
        print('Error: the message cannot be bigger than the number of images')
    else:
        generate_HTML(num)
        generate_PHP(msg)
