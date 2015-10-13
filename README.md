# quiz-show
mobile quiz game


Setup steps for mac or raspi.
1) Download the repo.
1b) if on a raspi edit client/index.js with your raspi IP.
2) create a folder called 'music' inside the 'quiz-show' folder
3) put a bunch of music files into the folder.
4) open the command line and inside the 'quiz-show' folder type 'python main.py'
5) open chrome and visit http://localhost:8000
6) Play.

To join from a phone on the same wifi find your mac's ip address:
> ifconfig |grep inet
and look for a line like inet 192.xxx.xxx.xxx.xx where the x's are numbers, then on your phone go to:
192.xxx.xxx.xxx.xx:8000/client/index.html
