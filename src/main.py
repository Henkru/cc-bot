#!/usr/bin/env python3
import toml
import argparse
import time
import logging
import sys

from bot import CCBot

def load_config(filepath):
    try:
        return toml.load(filepath)
    except Exception as e:
        logging.error('Error: %s', str(e))
        sys.exit(1)

def get_or_die(d, key, msg):
    try:
        return d[key]
    except:
        logging.error('Error: %s', msg)
        sys.exit(1)

def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='No script kiddies were harmed in the making of this awesome IRC C&C bot.')
    parser.add_argument('config', metavar='CONFIG', type=str, help='a config file')
    args = parser.parse_args()
    config = load_config(args.config)

    bot_config = get_or_die(config, 'cc', 'I need some bot configures!')
    server = get_or_die(bot_config, 'server', 'Give me a server!')
    bot_nick = get_or_die(bot_config, 'nick', 'Give me a nick!')
    channel = get_or_die(bot_config, 'channel', 'Give me a channel!')
    networks = bot_config = get_or_die(config, 'networks', 'I need some networks!')
    
    port = bot_config.get('port', 6667)
    server_password = bot_config.get('server_password', None)
    channel_password = bot_config.get('channel_password', '')
    delimiter = bot_config.get('command_delimiter', '!')

    bot = CCBot(server, port, server_password, bot_nick, channel, channel_password, delimiter)
    bot.start()

    for network_name, network in networks.items():
        try:
            server = network['server']
            port = network.get('port', 6667)
            nick = network.get('nick', bot_nick)
            password = network.get('password', None)
            bot.new_client(network_name, server, port, nick, password)
        except KeyError as e:
            logging.error('Error: %s', str(e))

    try:
        while(True):
            bot.loop()
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    #except Exception as e:
    #    logging.error('Error: %s', str(e))
    finally:
        bot.stop()

if __name__ == '__main__':
    main()