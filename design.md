# Design

## Architecture
This is a web app with a few different components:
* Frontend - Simple UI built with lit-element and lit-html
* API - Flask application
* Database - SQLite3

## Design
### API
This is the backend API.

<!-- vim-markdown-toc GFM -->

        * [GET /comics](#get-comics)
        * [GET /strips/\<name>](#get-stripsname)
        * [POST /strips/\<id>](#post-stripsid)
* [Data Model](#data-model)
    * [Comics](#comics)
    * [Strips](#strips)
    * [Reads](#reads)

<!-- vim-markdown-toc -->

#### GET /comics
Returns a list of all comics (and associated metadata).
Example:
```javascript
[
    {
        "name": "Nedroid",
        "author": "Anthony Clark",
        "link": "http://nedroid.com/"
    },
    ...
]
```

#### GET /strips/\<name>
Returns a list of all strips for the comic `<name>`.

Example:
```javascript
[
    {
        "id": 12345,
        "title": "Brand New Day",
        "link": "http://nedroid.com/2019/09/brand-new-day/",
        "datePublished": "Fri, 06 Sep 2019 17:32:23 +0000",
        "description": "This is what is known in the business world as a ‘hard sell.’",
        "imgUrl": "http://nedroid.com/comics/2019-09-06-BeartatoComics_Fruitley05_039.png",
        "wasRead": false
    }
    ...
]
```

#### POST /strips/\<id>
Used to change the `wasRead` state of a comic strip.

The body of the message must be JSON with the following fields:
```javascript
{ "wasRead": true }
```

## Data Model
All data is stored in a SQLite database. There are three tables:

### Comics
Each row represents a different comic (e.g. Nedroid, webcomic, xkcd).

* name (string, PRIMARY KEY) - Name of the comic (e.g. "Nedroid")
* author (string) - Name of author.
* link (string) - URL to comic homepage.

### Strips
Each row is a strip, belonging to exactly one comic.

* id (int, PRIMARY KEY) - ID used to reference the strip.
* title (str)
* link (str) - Link to the strip.
* datePublished (date) - Date the strip was published.
* description (str)
* imgUrl (str) - URL to the strip's image.

### Reads
Each row represents a strip the user has read.

* stripId (int, FOREIGN KEY) - ID of strip that has been read
