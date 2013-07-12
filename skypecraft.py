#!/usr/bin/env python
#
# Skypecraft
# https://github.com/kirov/skypecraft
#
# Copyright (c) 2012-2013 Evgeniy Kirov
# See the file LICENSE for copying permission.

from datetime import datetime
import rconite
import re
import Skype4Py
import sys
import tailer
import textwrap

import settings

reload(sys)
sys.setdefaultencoding('utf-8')


class Daemon(object):

    skype_commands = ['players', 'call']
    minecraft_commands = ['call']

    def __init__(self):
        self.log('Hello!')
        self.setup_skype()
        self.setup_rcon()
        self.setup_server_log()

    def run(self):
        for line in tailer.follow(self.server_log):
            self.on_server_log(line)

    def stop(self):
        self.log('Stopping...')
        self.server_log.close()

    def log(self, message, level=0):
        log_levels = {
            0: 'INFO',
            1: 'WARNING',
            2: 'ERROR'
        }
        print '%s [%s] %s' % (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            log_levels[level],
            message
        )
        sys.stdout.flush()

    def setup_skype(self):
        self.skype = Skype4Py.Skype()
        self.skype.Attach()
        self.skype.OnMessageStatus = lambda *a, **kw: self.on_skype_message(*a, **kw)
        self.skype.OnCallStatus = lambda *a, **kw: self.on_skype_call(*a, **kw)
        self.skype_chat = self.skype.Chat(settings.SKYPE_CHAT_NAME)
        self.log('Attached to Skype')

    def setup_rcon(self):
        self.rcon = rconite.connect(
            settings.MINECRAFT_RCON_HOST,
            settings.MINECRAFT_RCON_PORT,
            settings.MINECRAFT_RCON_PASSWORD
        )
        self.log('Connected to RCon')

    def setup_server_log(self):
        self.server_log = open(settings.MINECRAFT_SERVER_LOG)
        self.log('Opened server.log')

    def send_skype(self, msg):
        msg = str(msg.decode('utf-8', errors='ignore'))
        self.skype_chat.SendMessage(msg)
        self.log('Sent to Skype: %s' % msg)

    def send_rcon(self, msg):
        for part in textwrap.wrap(msg, 60):
            part = part.encode('utf-8')
            self.rcon.command('say %s' % part)
        self.log('Sent to Minecraft: %s' % msg)

    def on_skype_message(self, msg, status):
        if status != 'RECEIVED':
            return
        if msg.ChatName != settings.SKYPE_CHAT_NAME:
            return
        msg.MarkAsSeen()
        if msg.Body in self.skype_commands:
            self.log('Someone has sent a command "%s"' % msg.Body)
            getattr(self, 'command_%s' % msg.Body)()
            return
        self.send_rcon(u'[Skype] <%s> %s' % (msg.Sender.FullName, msg.Body))

    def on_skype_call(self, *args, **kwargs):
        self.skype.Mute = True

    def on_server_log(self, line):
        # checking if user command
        line = line.decode(settings.MINECRAFT_SERVER_LOG_ENCODING)
        match = re.compile('^[0-9\-\s:]{20}\[INFO\]\s\<.+\>\s(.+)$').match(line)
        if match and match.groups()[0] in self.minecraft_commands:
            self.log('Someone has sent a command "%s"' % match.groups()[0])
            getattr(self, 'command_%s' % match.groups()[0])()
            return
        # checking if this is a message from user
        match = re.compile('^[0-9\-\s:]{20}\[INFO\]\s(\<.+\>\s.+)$').match(line)
        if match:
            self.send_skype(match.groups()[0])

    def command_players(self):
        self.send_skype(self.rcon.command('list').replace('online:', 'online: '))

    def command_call(self):
        try:
            self.skype.PlaceCall(settings.SKYPE_CHAT_NAME)
        except ValueError:
            pass

if __name__ == '__main__':
    d = Daemon()
    try:
        d.run()
    except KeyboardInterrupt, e:
        d.stop()
