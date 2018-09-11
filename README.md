# pytokens

## Version

1.0.0

## Build Test

- Branch
  * master ![master](https://travis-ci.org/GnomeZworc/pytokens.svg?branch=master)
  * develop ![develop](https://travis-ci.org/GnomeZworc/pytokens.svg?branch=develop)

- Version
  * 1.0.0 ![1.0.0](https://travis-ci.org/GnomeZworc/pytokens.svg?branch=1.0.0)
  * 0.3.0 ![0.3.0](https://travis-ci.org/GnomeZworc/pytokens.svg?branch=0.3.0)
  * 0.2.0 ![0.2.0](https://travis-ci.org/GnomeZworc/pytokens.svg?branch=0.2.0)
  * 0.1.0 ![0.1.0](https://travis-ci.org/GnomeZworc/pytokens.svg?branch=0.1.0)

## Routes

```
- /
  * method : GET
  * header :
    - token : string
- /create
  * method : POST
  * header :
    - token : string
  * data :
    - source : string
    - id : int
    - limit_time : int (0 = unlimited)
  * retour :
    - message : string
    - token : string
- /check
  * method : POST
  * header :
    - token : string
  * data :
    - source : string
    - token : string
  * retour :
    - message : string
    - is_valid : int
    - (if is_valid) id : int
- /delete
  * method : POST
  * header :
    - token : string
  * data :
    - source : string
    - token : string
  * retour :
    - message : string
    - is_valid : int
    - (if is_valid) is_deleted : int
```

## Docker

You can use this api with docker :

```yml
---
version: '3'
services:
  pytokens:
    image: 'gnomezworc/pytokens:1.0.0'
    environment:
     - 'MONGO_HOST=mongo'
     - 'HOST=0.0.0.0'
    ports:
     - '80:8000'
    depends_on:
     - 'mongo'
  mongo:
    image: 'mongo'
    ports:
     - '27017:27017'
...
```
