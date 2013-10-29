Skypecraft
==========

Skypecraft is a small Python script that connects an in-game chat on your Minecraft server with a group conversation in Skype keeping them in sync. It should be useful on small private servers.

![skype screenshot](https://raw.github.com/wiki/kirov/skypecraft/screenshots/skype.png)

![minecraft screenshot](https://raw.github.com/wiki/kirov/skypecraft/screenshots/minecraft.jpg)

How to install
--------------

1. Enable Rcon in your `server.properties`. Specify Rcon password. Restart the Minecraft server.
2. [Register](http://www.skype.com/go/join) dedicated Skype account for your server.
3. Download and install [Skype](http://www.skype.com/intl/en/get-skype/on-your-computer/). Log in. Remember that Skypecraft works only if you install Skype and Minecraft server on the same machine.
4. Invite the newly created Skype user to your group chat.
5. Download and install [Python 2.x](http://python.org/download/). If you are OS X or Linux user, you may not need this. 32-bit version is preferable.
6. Did you [download Skypecraft](https://github.com/kirov/skypecraft/releases) already? Unzip it somewhere.
7. Now you need to install a few more dependencies. If you are familiar with Python, you may prefer using `pip` or `easy_install`. Otherwise you should locate the file called `dependencies.zip` and unpack its contents into the same directory which contains `skypecraft.py`.
8. Rename `settings.py.example` to `settings.py`.
9. Open it with any text editor such as Notepad. Make sure that your settings are correct.
10. Okay, it's time to run the script.

How to use
----------

Run Minecraft server and Skype as usual. Then open the command line and try to execute `skypecraft.py` (Windows) or `python skypecraft.py` (OS X, Linux). Skype may request your permission for the script to access API: allow it.


Commands
--------

Users can use the following commands in the chat. Simply type them without slashes or something.

* `players` (available only in Skype chat) — displays a list of players that are currently playing on server.
* `call` (available both in Skype and in-game chats) — starts Skype conference call.


Known issues
------------

* Skypecraft hasn't been deeply tested on operating systems other than Windows.
* Latest Skypecraft release works only with Minecraft 1.7 and newer versions. If you're looking for 1.6 compatibility, check out Skypecraft version 0.1.2. 
* If you're running OS X and getting a segmentation fault, then you need to run Skypecraft with this command: `VERSIONER_PYTHON_PREFER_32_BIT=yes python skypecraft.py`.
* Microsoft will shutdown Skype Desktop API by the end of 2013. Hopefully older versions of Skype will continue work.
* My English isn't perfect, so I'm sure that this README contains some grammar errors.

License & support
-----------------

This project is hosted on GitHub https://github.com/kirov/skypecraft and is licensed under MIT license.

If you have any questions, you can ask them in the [official thread on Minecraft forums](http://www.minecraftforum.net/topic/1493588-software-skypecraft-01/).