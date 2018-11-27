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

If you want to execute some commands inside your docker container, use:
```bash
$ (sudo) docker-compose exec import [command]
```

# More about the project
For more info, visit the main repository of the project: [Games BI](https://github.com/fga-eps-mds/2018.2-GamesBI)
