# pytokens

## Version

0.1.0

## Build Test

- Branch
  * master ![master](https://travis-ci.org/GnomeZworc/pytokens.svg?branch=master)
  * develop ![develop](https://travis-ci.org/GnomeZworc/pytokens.svg?branch=develop)
  * feature/check-token ![check-token](https://travis-ci.org/GnomeZworc/pytokens.svg?branch=feature/check-token)

- Version
  * 0.1.0 ![0.1.0](https://travis-ci.org/GnomeZworc/pytokens.svg?branch=0.1.0)

## Routes

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
