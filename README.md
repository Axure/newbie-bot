# Newbie Bot

QQ bot for the newbiew group.

## Setup

### QQBot

First you need to setup [QQBot](https://github.com/pandolia/qqbot).

After installing it with `pip`, and starting it with

```bash
qqbot
```

, you should migrate this repository to `~/.qqbot-temp/plugins` (the `plugins` directory are the root directory of this repository). In this way you will be able to load the plugins by name.

### Load Plugins

Copy `thesarus.sample.py` to `thesarus.py` and add your own thesarus. Only the `thesarus` variable in the file will be used.

Use

```bash
qq plug first
```

to load the `first` plugin, which is responsible for the miscellaneous functions like Lisp interpreting.

Use

```bash
qq plug justice
```

to load the `justice` plugin, which is responsible for the keyword detection. 


### Unload and Quit

```bash
qq unplug first
qq unplug justice
```

would unload the plugins respectively. And

```bash
qq stop
```

would stop the bot completely.

