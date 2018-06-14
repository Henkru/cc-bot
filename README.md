# cc-bot

This is a simple IRC based C&C.

## Getting started

* Requirements:
    * Python 3
    * Pip
* Install:
    * (Optional) If you are fancy: `virtualenv -p python3 env && source env/bin/active`
    * Install dependencies: `pip install -r requirements.txt`
    * Create the config: `cp config.example config`
* Run:
    * `python src/main.py config` - Start the bot and load config from `config` file.

## Config

The bot is using [TOML](https://github.com/toml-lang/toml) based configure file and the structure of that looks like

```toml
# The IRC server and the channel where the bot connects
[cc]
server = "irc.foo.bar"
port = 6667                    # Optional, default: 6667
server_password = "foobar"     # Optional
nick = "foobarbot"
channel = "#foobar"
channel_password = "foobar"    # Optional

# The command start character
command_delimiter = "!"        # Optional, default: !

# List of the networks where the bot can query stuff
[networks]
  [networks.ircnet]
  server = "irc.inet.fi"
  port = 6667                  # Optional, default: 6667
  nick = "bbott55677"          # Optional, default: cc.nick
  password = "salainen"        # Optional
  
  [networks.efnet]
  server = "efnet.portlane.se"

  ...
```

## Commands

* `whois <nick>` - query information about a nickname
* `networks` - get the status of networks

### Example usage

```
< Henkru> !networks
< ccbot0231> Networks: efnet [connecting], quakenet [connecting], ircnet [connected]
< Henkru> !whois henkru
< ccbot0231> [ircnet] Henkru henkru@kapsi.fi Henri Nurmi
< Henkru> !networks
< ccbot0231> Networks: ircnet [connected], efnet [connected], quakenet [connected]
< Henkru> !whois henkru
< ccbot0231> [ircnet] Henkru henkru@kapsi.fi Henri Nurmi
< ccbot0231> [efnet] No such nick
< ccbot0231> [quakenet] Henkru henkru@kapsi.fi Henri Nurmi
```