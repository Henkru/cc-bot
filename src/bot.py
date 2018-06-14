import logging

import irc.bot
import irc.client
import irc.client_aio

import command

class CCClient(irc.client.SimpleIRCClient):
    def __init__(self, name, server, port, nickname, password):
        irc.client.SimpleIRCClient.__init__(self)
        self.name = name
        self._whois_handler = None
        self.connected = False

        self.connect(server, port, nickname, password=password)

    def on_welcome(self, connection, event):
        logging.info('[%s] Connected', self.name)
        self.connected = True

    def on_nicknameinuse(self, connection, event):
        self.connection.nickname = event.arguments[0] + '_'
        connection.nick(self.connection.nickname)
        logging.info('[%s] Nickname is already in use. Trying: %s', self.name, self.connection.nickname)

    def on_nosuchnick(self, connection, event):
        if self._whois_handler:
            self._whois_handler(None)

    def on_whoisuser(self, connection, event):
        if self._whois_handler:
            self._whois_handler(event)

    def whois(self, target, handler):
        try:
            self.connection.whois(target)
            self._whois_handler = handler
        except irc.client.ServerNotConnectedError:
            pass

class CCBot(irc.bot.SingleServerIRCBot):
    def __init__(self, server, port, password, nickname, channel, channel_password, delimiter):
        srv = irc.bot.ServerSpec(server, port ,password)
        irc.bot.SingleServerIRCBot.__init__(self, [srv], nickname, nickname)
        
        self.channel = channel
        self.channel_password = channel_password
        self.command_delimiter = delimiter
        self.clients = {}

    def start(self):
        self._connect()

    def on_welcome(self, connection, event):
        connection.join(self.channel, self.channel_password)
        logging.info('[bot] Join to %s', self.channel)

    def on_nicknameinuse(self, connection, event):
        self.connection.nickname = event.arguments[0] + '_'
        connection.nick(self.connection.nickname)
        logging.info('[bot] Nickname is already in use. Trying: %s', self.connection.nickname)

    def on_pubmsg(self, connection, event):
        msg = event.arguments[0]
        if msg.startswith(self.command_delimiter):
            parts = msg[1:].split(' ', 1)
            cmd = parts[0]
            arg = parts[1] if len(parts) == 2 else None

            command.call(cmd, arg, self)

    def new_client(self, network_name, server, port, nick, password):
        try:
            logging.info('Connecting %s %s:%i', network_name, server, port)
            client = CCClient(network_name, server, port, nick, password)
            self.clients[network_name] = client
        except irc.client.ServerConnectionError as e:
            logging.error('Error: %s', str(e))

    def send(self, msg):
        self.connection.privmsg(self.channel, msg)

    def stop(self):
        logging.info('[bot] Stopping')
        for client in self.clients.values():
            client.connection.disconnect()
        self.connection.disconnect()

    def loop(self):
        self.reactor.process_once()
        for client in self.clients.values():
            client.reactor.process_once()