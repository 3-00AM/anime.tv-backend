# Anime.tv - Backend Service

![img.png](https://i.imgur.com/3bWcdel.png)

## Team Members

| Name                 | GitHub ID                                       |
| :------------------- | :---------------------------------------------- |
| Vichisorn Wejsupakul | [james31366](https://github.com/james31366)     |
| Bheem Suttipong      | [Bheem6005](https://github.com/Bheem6005)       |
| Sahatsawat Kanpai    | [keyboard2543](https://github.com/keyboard2543) |

## Project Overview and Features

Our project is for get the data from one [MAL API](https://myanimelist.net/apiconfig/references/api/v2), [Kitsu API](https://kitsu.docs.apiary.io/#), and [Aruppi API](https://aruppi-api.herokuapp.com/api/v3) and then we have to store all the get request data into our database.

<div align="right"> <b><a href="#top">↥ back to top</a></b> </div>

### Features



## Requried libraries

- [Python](https://python.org/)

## Instruction for running

First, after clone the project you have to install the dependencies

```shell
pip -r install requirements.txt
```

Next you have to set the environment

```env
DEBUG=True
SQLALCHEMY_DATABASE_URI=Your Database URI
MAL_ACCESS_TOKEN=The Access Token for My Anime List Website
```

Then if you have your new databases you have to run the

```shell
python insert_to_db.py
```

and you have to run the `app.py` by

```shell
python app.py
```

Last, you can use the Our provided front-end by open the `.\templates\index.html`

<div align="right"> <b><a href="#top">↥ back to top</a></b> </div>
