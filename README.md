<p align="middle"><img src="https://i.imgur.com/M74MjRl.jpg"></p>

[![Build Status](https://travis-ci.org/fga-eps-mds/2018.2-GamesBI_Importadores.svg?branch=master)](https://travis-ci.org/fga-eps-mds/2018.2-GamesBI_Importadores)
[![Maintainability](https://api.codeclimate.com/v1/badges/9fcbd359a63880bdb0b2/maintainability)](https://codeclimate.com/github/fga-eps-mds/2018.2-GamesBI_Importadores/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/fga-eps-mds/2018.2-GamesBI_Importadores/badge.svg?branch=)](https://coveralls.io/github/fga-eps-mds/2018.2-GamesBI_Importadores?branch=)

# Getting started

Before anything, you need to install [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/). After installing those, you'll be able to start contributing to this project.

# Starting the application

It's as easy as:

```bash
$ make up
```

And after you download all the necessary dependencies the application will be running locally.

You can also build your docker container without executing it with:

```bash
$ make build
```

And you can execute without showing any logs with:
```bash
$ (sudo) docker-compose up -d
```

# Other commands

If you want to execute some Flask commands inside your docker container, use:
```bash
$ (sudo) docker-compose exec import [command]
```

These commands can be:
```bash
python manage.py test
python manage.py createapp your-app
```
or any other supported by Flask.

# More about the project
This project aims to offer a competitive BI for games. This includes, game development, content creation for youtube and twitch and whether you should invest in a game if you're a publisher.

A lot of its design ideas came from other sites, for example, [steamspy](steamspy.com). Although we're not only using information from Steam, but also from Youtube and Twitch.

Our belief is that there isn't a cross-platform and helpfull BI tool for games out there. Which is why our main goal is to deliver this very such thing, and also make it acessible for everyone willing to use it.
