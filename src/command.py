_COMMANDS = {}

def command(name):
    def wrapper(f):
        _COMMANDS[name] = f
        return f
    return wrapper

def call(cmd, arg, bot):
    if cmd in _COMMANDS:
        _COMMANDS[cmd](arg, bot)

@command('whois')
def cmd_whois(arg, bot):
    if not arg:
        bot.send('Usage: whois <nick>')
    for name, client in bot.clients.items():
        if client.connected:
            client.whois(arg, whois_handler(bot, client))

@command('networks')
def cmd_ls_networks(arg, bot):
    status = map(lambda x: '%s [%s]' % (x.name, 'connected' if x.connected else 'connecting'), bot.clients.values())
    bot.send('Networks: %s' % ', '.join(status))

def whois_handler(bot, client):
    def wrapper(event):
        if event:
            nick = event.arguments[0]
            user = event.arguments[1]
            host = event.arguments[2]
            real = event.arguments[4]
            bot.send('[%s] %s %s@%s %s' % (client.name, nick, user, host, real))
        else:
            bot.send('[%s] No such nick' % (client.name))
    return wrapper
