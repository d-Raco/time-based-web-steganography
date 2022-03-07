import os, os.path, sys, argparse, math
import globals

def generate_HTML(num):
    ''' Generates the HTML file; frontend of the web-page, hosting the images'''

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


def generate_PHP(msg):
    ''' Generates the PHP file; back-end of the web-page, specifies the delays per image'''

    # Open the file image.php (backend of the webpage, in charge of serving the images with a specific delay)
    f = open("image.php", "w")

    # Write the header of image.php and get the value of "image_id" from the URL
    f.write('<?php\n  header("Content-Type:image/png");\n\n  $image_id = $_GET["image_id"];\n\n')

    checksum_length = 0
    # Divide the message into blocks
    for block in range (0, block_number):
        index = (block * globals.block_size + 2*block) * globals.images_per_char + checksum_length
        # For each character of the message, specify the delay of the corresponding images using the ascii value of the character itslef converted into the specified base
        for i in range (0, globals.block_size):
            msg_index = i + block*globals.block_size
            # Check if the index does not exceed the message
            if (msg_index < len(msg)):
                # Divide each character into the number of images needed per char
                for j in range (0, globals.images_per_char):
                    if (block == 0 and i == 0 and j == 0):
                        f.write('  if($image_id == ' + str(index) + ')\n    $ms = ' + str(int(globals.dec_to_base((ord(msg[msg_index])-globals.non_important_characters), globals.base).rjust(globals.images_per_char, '0')[j], globals.base)) + ';\n')
                    else:
                        f.write('  elseif($image_id == ' + str(index) + ')\n    $ms = ' + str(int(globals.dec_to_base((ord(msg[msg_index])-globals.non_important_characters), globals.base).rjust(globals.images_per_char, '0')[j], globals.base)) + ';\n')
                    index += 1

        # Add a separator between the message itself and the checksum; it will be identified by having the minimum delay
        for j in range (index, index + globals.images_per_char):
            f.write('  elseif($image_id == ' + str(j) + ')\n    $ms = ' + str(0) + ';\n')

        index = index + globals.images_per_char
        checksum = checksum_list.pop()
        checksum_length += len(checksum)
        # Specify the delay of the corresponding images using a checksum, which is calculated by adding all the message's delays
        for j in range (index, (index + len(checksum))):
            f.write('  elseif($image_id == ' + str(j) + ')\n    $ms = ' + str(int(checksum[j-index], globals.base)) + ';\n')

        index = index + len(checksum)
        # Add a separator between the checksum and the rest of the message; it will be identified by having the minimum delay
        for j in range (index, index + globals.images_per_char):
            f.write('  elseif($image_id == ' + str(j) + ')\n    $ms = ' + str(0) + ';\n')

    index = index + globals.images_per_char
    # Add a separator between the checksum and the rest of coverup additional images; it will be identified by having the minimum delay
    for j in range (index, index + globals.images_per_char):
        f.write('  elseif($image_id == ' + str(j) + ')\n    $ms = ' + str(0) + ';\n')

    # If it is any coverup additional image, have a random delay
    f.write('  else\n    $ms = rand(0,' + str(globals.base-1) + ');\n\n')

    # Sleep as many milliseconds as specified; usleep is specified by microseconds, so multiply by 1000; also multiply by inter_delay to have more delay, making it more robust
    f.write('  usleep( $ms * ' + str(globals.inter_delay) + ' * 1000 );\n\n')

    # Check how many images there are under the "img" directory
    img_dir = './img'
    img_num = len([name for name in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, name))])

    # If "image_id" is negative, change it to 0
    f.write('  if($image_id < 0)\n    $image_id = 0;\n\n')

    # Serve an image from the "img" directory following this logic: $image_id % img_num + ".png"; note that the name of the images is a number starting from 0 and going up
    f.write('  $theImage = "./img/". ($image_id % ' + str(img_num) + ') .".png";\n  if(is_file($theImage))\n    echo file_get_contents($theImage);\n?>')
    f.close()


def main():
    # Define global variables
    globals.init_globals()

    # Check if the base is in a valid range
    if (globals.base < 2 or globals.base > 36):
        print('Error: the base must be >= 2 or <= 36')
        return

    # Check if the globals.block_size is a valid number
    if (globals.block_size < 1):
        print('Error: the block_size must be >= 1')
        return

    # Parse the arguments passed to the program
    parser = argparse.ArgumentParser(description='Generate the Stego page')
    parser.add_argument('-msg', type=str, required=True, help='the message to hide')
    parser.add_argument('-num', type=int, default=300, help='the number of images displayed in the page (consider that space is needed for the checksum and separators); Default: 100; If a number less than or equal to 0 is provided, the exact minimum number of images needed to hide the message will be displayed.')

    args = parser.parse_args()
    msg = args.msg
    num = args.num

    global block_number
    block_number = math.ceil(len(msg) / globals.block_size)

    global checksum_list
    checksum_list = []
    checksum_size = 0
    # Calculate the checksum of the different delays by block, adding the corresponding numbers and transforming the result into the specified base
    for block in range (0, block_number):
        checksum = 0
        index = block * globals.block_size
        for i in range (index, (index+globals.block_size)):
            # Check if the index does not exceed the message
            if (i < len(msg)):
                for j in range (0, globals.images_per_char):
                    checksum += int(globals.dec_to_base((ord(msg[i])-globals.non_important_characters), globals.base).rjust(globals.images_per_char, '0')[j], globals.base)
        checksum = globals.dec_to_base(checksum, globals.base)
        checksum_size += len(checksum)
        checksum_list.insert(0, checksum)

    # Minimum number of images required to hide the message (taking into consideration the checksums and separators)
    minimum = ((len(msg) + 2*block_number + 1) * globals.images_per_char + checksum_size)

    # If number lower or equal to 0, specify the number of images as the minimum required to hide the message
    if (num <= 0):
        num = minimum

    # Check if the number of images is not enough to hide the message
    if (minimum > num):
        print('Error: the message cannot be bigger than the number of images')
        return

    # Check if the base/images_per_char ratio is enough to encode the globals.relevant_characters ascii characters we are interested in (from char globals.non_important_characters to globals.maximum_ascii_char_num). If this is not the case, print some recommendations
    if (pow(globals.base, globals.images_per_char)-1 < globals.relevant_characters):
        print('Error: the base/images_per_char ratio is not enough to encode at least the globals.relevant_characters')
        print('Recommendations:')

        i = 0
        while (pow(globals.base, globals.images_per_char+i)-1 < globals.relevant_characters):
            i += 1
        print('     - set globals.images_per_char to ' + str(globals.images_per_char + i) + '. Using the same globals.inter_delay, the maximum delay of an image would be: ' + str((globals.base - 1)*globals.inter_delay) + 'ms.')

        i = 0
        while (pow(globals.base+i, globals.images_per_char)-1 < globals.relevant_characters):
            i += 1
        if (globals.base+i <= 36):
            print('     - set globals.base to ' + str(globals.base + i) + '. Using the same globals.inter_delay, the maximum delay of an image would be: ' + str((globals.base + i - 1)*globals.inter_delay) + 'ms.')

        print('     - fine tune both the globals.base and globals.image_per_char.')
        return

    # Generate the server files
    generate_HTML(num)
    generate_PHP(msg)


if __name__ == '__main__':
    main()
