# time-based-web-steganography
 A steganography method for hiding messages in image delivery latency

## Introduction
Steganography consists of the use of techniques that make it possible to hide a message so that its mere existence is not perceived. This data is embedded into normal-looking information (called cover) so the secret is only revealed if using suitable mechanisms.

In classical steganography, the security of the message was achieved by obscure methods, so that the channel was not discovered; whereas modern steganography makes use of existing channels, especially digital media such as video, audio or image files. However, there are many channels outside of digital media that are exploited to hide these messages, such as text files, executable files or communication protocols.

For this document, a steganography method based on web pages and the HTTP protocol will be developed. There are several ways to exploit this protocol, but in particular it will be focused on the loading time established for the different elements that contain the web page itself.

## Motivation
Today, modern steganography is focused almost entirely on digital channels, used mainly for intellectual property protection, intelligence agencies, activists and criminals. The latter can include all those who misuse cyberspace through the use of malware, be they individuals or entire organizations. An example of this type of organisation are those that make use of an APT, which will be the focus of this document.

An APT (Advanced Persistent Threat) is a set of processes that use multiple attack vectors to achieve a goal that is usually persistent over time. These objectives could be exfiltrating information, undermining or impeding critical aspects of the organization or positioning itself to carry out these objectives in the future. These threats often use the Command and Control (C&C) structure, which consists of using an external server to install malware on previously compromised machines in order to control them remotely over a long period of time. It is therefore important that the communication between the machines and the server be stealthy so that it is undetectable to the victim.
In this work, a modern steganography method is developed in order to be able to maintain this communication between machine and server avoiding suspicion. It is based on a web page that will be accessed by the compromised machines to receive the information transmitted by the remote server. Thus, it is important that this page appears normal within the network traffic of the organization that actually owns the devices.

The message will be transmitted using the elements of the web page itself and its loading times. Since multimedia files tend to show more delay when loading, these will be the ones used. In order to have a large number of images without arousing suspicion, the website will have an icon storage aesthetic. This type of page is used for making PowerPoint presentations and similar tools, being suitable for both work and education scope.

## Proposed mechanism
The final goal of this project is to hide a message in a cover media. Following this goal, the team decided to develop a web front to hide commands sent from a C&C server to infected bots. There have already been many different approaches to this idea, but the team decided to devise a new and hopefully more effective take on this problem.

In order to achieve this, there are several milestones that must be met. Firstly, the commands must be somewhat hidden, as it would not be beneficial for it to be identified as a server used to send commands, since it would be taken down or blocked. For this reason, the team decided to develop a technique not easily identifiable. After some thought, it was agreed that tailor-made delays could be used in the delivery of elements, as it is something normal at first glance, especially when loading images.

Thus, the methodology proposed in this document is a website hosting multiple images (which will be icons), where the delay of serving those images to a client encodes the message itself.

Any user accessing this website, will see several icons untimely loading, which should not be unusual behaviour. But the time which takes to load these icons encodes the message.

![index](/assets/0.png)

To hide a message using specific delays, the first step was to convert the characters of the message to be hidden into numbers; this was achieved using the ASCII table, as every character is assigned a numerical value.

![ASCII table](/assets/1.png)

The first approach that was considered was to use the base decimal value, where character ‘A’ would be equivalent to 65 and ‘B’ to 66. In this sense, each image would be a single character, so a delay of 65 milliseconds would correspond to character ‘A’ and a delay of 66 milliseconds to ‘B’.

![delays](/assets/2.png)

There is an intrinsic problem with this character to number translation: there is only 1 millisecond difference between two consecutive characters in the ASCII table, as it so happens with characters ‘A’ and ‘B’. The problem of this fact is that there is always a delay when transmitting data over any medium. In this sense, if the user connects to the webpage, there will be several additional milliseconds of delay for carrying the image from the server to the client. This usually means that the delay calculated by the client is not exactly the delay caused by the server that encodes the specific letter.

A valid countermeasure would then be to increase the milliseconds difference between two consecutive characters in the ASCII table. This gave rise to the concept of inter-delay. Instead of delaying n milliseconds, where n is the decimal representation of an ASCII character, the server would delay n*inter-delay milliseconds. Now, having an inter-delay of 10 milliseconds, ‘A’ would be equivalent to 650 and ‘B’ to 660. This allows the data transmission delay to have an error range of 10 milliseconds, considerably improving robustness. But typically, 10 milliseconds is not enough, as the transmission delay can sometimes be several hundred milliseconds, even a few seconds. This, of course, could be mitigated by having a high enough inter-delay. For example, 300 milliseconds is enough most times.

![inter-delay](/assets/3.png)

But increasing the inter-delay poses a new challenge: if the inter-delay is set to 300 milliseconds, an image could be delayed more than 37 seconds if it encodes the ‘~’ character, as it is translated into 126 (126 * 300 = 37800 ms). This is not only impractical, but also raises the suspicions of any user accessing the website.

The problem can be partially reduced by considering only the useful ASCII characters. Characters before the 32nd character can be omitted; the end line character may be useful, but as we are going to use the page to encode commands, it will not be strictly necessary.

![useful ASCII chars](/assets/4.png)

Then, any character can have a delay equal to its decimal value minus the number of non-important-characters. After this, ‘A’ would be equivalent to 33 and ‘B’ to 34. Considering the inter-delay of 300 ms, the maximum possible delay would be over 28 seconds ([126 - 32] * 300 = 28200 ms), which is an improvement, but not enough.

![non-important-chars](/assets/5.png)

The underlying problem lies in the fact that a single image must now encode 94 different numbers. To overcome this, a character can be encoded by more than one image. If, for example, two images were used per character, the first image could encode the decimals and the second image the units. Now, an image would only need to represent 10 different numbers, from 0 to 9. Following this change, ‘A’ would be 3 + 3 and ‘B’ would be 3 + 4. The maximum possible delay would now be almost 3 seconds (9 * 300 = 2700 ms), which is an extreme improvement.

![images-per-char](/assets/6.png)

This idea can actually be further expanded: if the number of images increases, the number of symbols that an image needs to encode reduces, allowing for greater inter-delays, which in turn implies better robustness. As already stated, the maximum number is 94 (126 - 32); to represent this in 3 images, the base can be changed, from decimal to base 5, translating 94 (base 10) into 334 (base 5). The maximum delay per image can be expressed as (base-1)*inter-delay; with 3 images and 300 ms of inter-delay, the maximum delay per image is 1200 ms.

![base](/assets/7.png)

If 7 images are used per character, the delay could even be represented as binary: 94 (base 10) into 1011110 (base 2). With 7 images and 300 ms of inter-delay, the maximum delay per image is 300 ms.

To summarise, more images per character implies a lower base, which corresponds to the number of symbols represented by a single image. A lower base entails a higher possible inter-delay, which leads to better robustness. But, if the inter-delay is too large, it can be more easily discovered and extracting the hidden message takes more time. And even if the inter-delay is a large number, sometimes the network may be saturated, so it could lead to misinterpretations.

In order to solve this problem, a checksum was added at the end of the message. This checksum is calculated by adding all the symbols of each image by both the server and the client. If they do not match, there has been an error when extracting or sending the message. If they match, there is a low possibility of a false positive match, but in most cases the message will be the correct one. To separate the message from the checksum, the server adds a separator between the both of them before sending it to the client. This separator will be encoded with the lowest possible delay, 0 milliseconds. Since the 0 ms delay is already taken by the first useful character of the ASCII table (the 32nd element in our case), the number of non-important characters will be reduced by 1, so the first useful character of the ASCII table will now be associated with a 1 ms delay and the maximum number will become 95.

![checksum](/assets/8.png)

For an added layer of security, more images with random delay will be added after the checksum, so that, even if the message and its length changes, the number of images will always be the same. To identify the end of the useful information, another separator will be added after the checksum.

A last problem arises from adding a checksum for the whole message: if the message is too large, the probability of an error taking place during the transmission highly increases. If an error occurs, the whole message must be received again and the checksum calculated once more. For this reason, decoding the message can take hours, since only one failure implies repeating everything once more. To solve this, the message can be divided into blocks of a specific number of characters, and instead of a checksum for the whole message, there is a checksum for each block. This implies that, if an error is encountered, only a single block has to be calculated once again instead of the whole message.

![blocks](/assets/9.png)

## Technical implementation
A working Proof of Concept (PoC) has been developed to show the feasibility of the aforementioned idea. The code of the PoC has been implemented following this folder structure:
- img: This folder contains all the icon PNG images which are going to be displayed.
- index.html: This file is the front-end of the web page. It basically contains several image HTML elements to place the respective icons. The source of these icons will point to the back-end, which will be responsible for loading and delaying the icon delivery.
image.php: This file is the back-end of the web page. HTML image elements request this file to load the image by giving the ID of the image. Depending on the ID, the specific delay will be performed and then the image will be delivered.
- globals.py: This file contains several global variables and functions used by the create_page.py and unhide.py.
- create_page-py: This python script can receive two parameters, the message that will be hidden and the number of images to be displayed. Then, it will dynamically create both index.html and image.php based on those parameters, as well as the values from globals.py.
unhide.py: This python script connects to the web page and extracts the message by calculating the time it took to load the images.

## Setup & Usage
To test the PoC, the first step is to set up a web server. This can be achieved through a web server solution. One possibility is XAMPP, which is open source and cross-platform; it can be downloaded from [this site](https://www.apachefriends.org/download.html).

After the installation, the code of the PoC must be copied into the htdocs folder, located inside XAMPP’s directory. A new folder must be created inside of the htdocs folder, and the code must be copied inside. The PoC code can be obtained from [this public repository](https://github.com/Rymond3/time-based-web-steganography).

Now, the webpage must be created. Python is needed to execute the PoC, so it must be installed; it can be downloaded from [this site](https://www.python.org/downloads/). Firstly, the globals.py file can be edited to set global variables like inter-delay, number of images used to encode a single character, etc. Then, a terminal must be opened inside of the directory containing the code and the create_page.py must be executed. The arguments of this script are:

```
usage: create_page.py [-h] -msg MSG [-num NUM]

Generate the Stego page

optional arguments:
  -h, --help  show this help message and exit
  -msg MSG    the message to hide
  -num NUM    the number of images displayed in the page (consider that space is needed for
              the checksum and separators); Default: 100; If a number less than or equal to
              0 is provided, the exact minimum number of images needed to hide the message
              will be displayed.
```

Some checks are performed over the arguments passed and the global variable to make sure that no errors are encountered during the execution. It may be the case that there are required python libraries that are not installed on the system. To install them, execute the command:
```
pip install <library>
```

If pip is not installed on the system, first execute 
```
python3 -m pip install
```

After executing the create_page.py script, the web server must be started. This is done by executing the XAMPP application and starting the Apache Web Server functionality. If everything worked properly, the web page should be visible by opening a web browser and typing the following URL: http://localhost/name_of_the_code_folder/.

Now the script unhide.py must be edited. The webpage value must be changed to the URL inputted into the browser. Lastly, this script can be executed.

This has been executed locally. In order to execute over a network first download the unhide.py and globals.py files onto another device and change the web page to http://internal_ip_of_the_server/name_of_the_code_folder/. Both devices must be connected to the same network.

In order to use it over the network, the configuration of the router must be changed in order to forward incoming traffic to the server. Open a web browser and type http://192.168.1.1. Under the Ports menu add a new rule with the server’s IP address, TCP protocol, set the external port to 5555, for example, and internal port to 80. Now, an external system can access the website by setting the web page value to http://external_ip_of_the_server:external_port_set_in_the_router_rule/name_of_the_code_folder/.

## Comprehensive tests

The code has been implemented to ensure a high degree of scalability and flexibility. For this reason, any user can specify values such as images-per-char, inter-delay and block-size and execute the scripts, which will shape to the specified attributes automatically.

In order to test the most optimal combination of attributes, as well as the robustness of the methodology over the internet, it was decided that a high number of tests would be carried out, each one with a different set of attributes. A [spreadsheet](/tests/tests.csv) was created to record the result of each test.

Five initial attributes have been taken into account: message length, images-per-char, base, inter-delay and block-size. Each row of the spreadsheet has a unique variation of these attributes. Per each row, three tests have been carried out to ensure more accurate results. Each test has three result columns assigned: failed checksums (number of times the checksum did not match), seconds (number of seconds needed to decode the message) and wrong message (if the checksum matched but the message is incorrect, i. e. a false positive). Lastly, two columns show the average failed checksums and average seconds calculated from each three tests.

It is performed 516 tests, having 172 different combinations of attributes. These tests have shown that the most consistently optimal attribute combination is: images-per-char = 4, base = 4, inter-delay = 100, block-size = 5. The following charts show the reasoning behind these values: Figure 12.a shows that 4 images-per-char is the most efficient in terms of average seconds. Figure 12.b displays the average number of seconds per inter-delay, where 75 ms obtains the worst score. On the other hand, Figure 12.c indicates the average number of fails per inter-delay, where starting at 100 ms the number of fails is extremely reduced. Lastly, Figure 12.d shows the average seconds per block-size, where 5 is the most efficient one.

![ASCII table](/assets/10.png)
![ASCII table](/assets/11.png)
![ASCII table](/assets/12.png)
![ASCII table](/assets/13.png)

More information discovered through these tests is discussed in each quality metric.

## Quality Metrics

In terms of capacity, the webpage could technically have an infinite number of images and, thus, the length of the message could be infinite. But there is a practical limit. Since this steganography method leverages delays, having a longer message could imply an extremely long time to extract the message of the web page. After all, the main focus of this project was the security aspect of the steganography, as commands are not exceedingly lengthy. Even so, thanks to dividing the message into blocks, longer messages can be more easily calculated than having only a single checksum. After several tests, we were able to set the practical capability of this method to a message of about 40 characters, as it takes about 50 seconds to decode, which is arguably too long.

In terms of security, it is the main focus of this project, as the final goal was to create a C&C as undetectable as possible. Unless the inter-delay is set to an extremely high number, the delays do not stand out, and it is common to see images that take time to load. It should be noted that the delay is only specified in the server side, so a client would not be able to see the logic behind the delays, which would be possible if the delay logic had been developed using javascript, for example. Also, an icon web page is a website that can be typically accessed in working environments, as they can be copied to be used in powerpoints and presentations, so it would not raise alarms.

At the process level, if the device has been previously compromised, it is possible to hide the trace of the script by using a rootkit. Otherwise, if a rootkit is not used, functions can be implemented to check that processes are not being monitored. This should be enough to remain undetected.

In terms of network traffic it could be a noisy process. Although this cannot be changed, methods of making it less suspicious can be developed. An example of this would be to verify that there is already traffic on the network over http(s) or that a search has been performed on engines such as Google.

The script is launched from a terminal, so it might attract attention if the fingerprint is different from a browser. A solution to this would be to launch the script from the browser itself, or else copy its fingerprint. Since security is one of the most important issues, this could be one of the main future steps of the project.

In terms of robustness, setting up a large inter-delay should avoid most of the possible errors of the transport latency. Also the checksums ensure that, if an error has occurred, the message blocks are requested until all the checksums are satisfied. There is a possibility that the checksum fails and there is a false positive, but these cases would be extremely few.

After the tests were performed, several false positive checksums were detected, but only when the inter-delay was equal to or lower than 50 milliseconds. Out of 411 tests performed with an inter-delay over 50 ms, none of them presented a false positive checksum (in essence, the message was correctly decoded). Out of 75 tests performed with an inter-delay equal to 50 ms, only 3 presented a false positive checksum (4%). Out of 30 tests performed with an inter-delay equal to 40 ms, 5 presented a false positive checksum (16.66%). After such tests, it is safe to state that robustness is guaranteed if the inter-delay is greater than or equal to 60 ms.

Another reason why we decided to use the cover of an icon hub is because the icons typically have a very similar byte size, so the loading time difference between two different images is highly reduced.

On the other hand, since the script is developed in Python, it is necessary that the compromised device can execute it. This is not a problem if the necessary software has been previously installed. However, if this is not the case, the device must contain a Python installation, which is not common on non-development oriented Windows systems. For this purpose, the script could be exported as an executable (being in Windows simply an .exe) so no installation is required. On Linux this should not be necessary since most distributions already have Python installed.
