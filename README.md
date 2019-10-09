
# SERVERLESS URL SHORTENER


A URL Shortener is a service that creates short **aliases for URLs**. It generates a short code for a URL and then redirects the user to the URL when that code is accessed. One example of such service is [bitly](https://bitly.com/).


# Solution

## System requirements

 - Functional:
   
   - Given a URL, the system will generete a unique short alias(short URL)
   - If we enter to the short URL, we will be redirected to the original URL
   - A simple user interface
   - The UI will show the generated URL
   - Basic auth

 - Non functional:
   - Highly availiability
   - URLs most not be predictable
   - Python 3 with any framework
   - Good coverage
   - Use GIT
   - Clean and reliable code
 
## About this app
This app is a flask based project. It implements flask as a factory and make use of blueprints. SqlAlchemy ORM, dotenv, JWT for auth, argon2 for password hashing,  and pytest for test suite. It implements a simple logger and a custom error validator and schema validator Marshmallow for schema validation. 

## Project structure

For this project i choose a multi-module project structure. This app implements four four modules: health, short_url, users and utils. Tests folder is separated and outside of main app.  

```
url_shortener/
├── app
│   ├── short_urls
│   │   ├── model.py # (M)
│   │   ├── routes.py # (VC)
│   │   ├── schema.py
│   │   ├── constants.py
├── users
│   │   ├── model.py 
│   │   ├── routes.py 
│   │   ├── schema.py
│   │   ├── constants.py
├── utils
│   │   ├── short_url.py # bijective function for encoding short_ids
│   │   ├── error_handler.py
│   │   ├── helpers.py
│   │   ├── validators.py
│   │   ├── swagger.py
│   ├── __init__py # main app
└── tests
    └── integration
    └── unit
```

## Database design

I choose to use PostgreSQL, it is suitable for our purposes. I will use two tables.
- One table will contain the user's data who created the short link
- One table will store URL mapping information


## Built with
- Python 3.7
- Flask

## Code style
PEP8

## API Reference

The project will serve swagger-ui @ /swagger (not working on lambda deployment :(), but you can review the api specification here: https://app.swaggerhub.com/apis-docs/ernestopalafox/url-shortener/1.0.0
  


## Ramble on about the algorithm

## TLDR: Go directly to Decision section [here](#decision)

### IDEA 1

Ok, we need a unique id for each URL. What if we use a standard algorithm to hash the given URL string? Lets say we choose crc-32. It will generate a 32 bit hash value.
```
>>> import zlib
>>> zlib.crc32(b'http://www.thelongestdomainnameintheworldandthensomeandthensomemoreandmore.com')
239525111
>>> hex(239525111)
'0xe46dcf7'

```
Looks great... right?

The size of the crc32 hash space is 2^32 = 68,719,476,736

But... what about collitions?

As stated here [wiki generalization] "the expected number of N-bit hashes that can be generated before getting a collision is not 2^N, but rather only 2​^N⁄2".

Hence, for our crc32 algorithm we can expect our first collition at: 2^(32/2) = 256
Wait, what???

Hash function approach Drawbacks:

- Early collisions
- Insertion can became costly. We will need to hit db to ensure the id doesn't exist, if it exist, we will generate another random id until id is unique.

Workarounds:

- Append a random id to the hash after encoding, it will also make out urls more 'secure'. But the cost will be a larger url.

Or maybe there is a simple and better way?
Let's start again.

  

### IDEA 2

The most popular shortened urls services use a series of numbers and capital and lower case letters [a-zA-Z0-9], but why? I can guess 2 main reasons. The first one is that you don't have to deal with weird characters [%,/,$,...]. And the second one is exponential growth.

Since we don't have in our requirements a 'strict' length constrain. Lets say we will generate short urls of max_length 6.

If we use base10 it will give us a total of:

10^6 = 1 Million of unique ids

If we use base62 it will give us a total of:

62^6 = 56 billion 800 million 253 thousand 584 unique ids

It's more clear now.

But, how will we generate this id that we will encode to base62?

We can generate a random number then, we will encode it to base62. This way we can map out shortId to the long url and store it on a database. Sound good.

But... thinking a little more, we still have some issues. First, we will need to hit the db to ensure the rand number isn't already used. Let's assume we already have millions of records, at this point, insertion can be costly. We can also (rarely) have concurrency problems that can lead to more than one url mapped to the same short url.

Lets recap
Random int generation approach drawbacks:
- We will need to hit the db to ensure the rand number isn't already used.
- Concurrency issues unless we ensure uniqueness directly on our db.

  

### IDEA 3

What if we don't relay in a random number, but a sort of counter?
Ok, maybe a simpler approach can work better. We can make use of an auto increment id of a SQL DB, and encode it to base62. With this approach we don't need hash algorithms or random generators. We can just use a simple identity field that is incremented each time.

We can ensure uniqueness and insertion shouldn't be costly at scale. Also we don't have single points of failure like concurrency issues. But... wait...

Let's say my next id is 10000, encoded in base 62 will be 2bI, next one will be 10001, encoded 2bJ...

With this approach someone can guess all our urls at first glance... it isn't safe at all.

We can (at the cost of url length) add a random identifier, to make them a little bit more secure.
What if instead of 2bk (10002 in base10) we add 2 more random base 62 characters?

Something like this:
final_url = first_random_char + short_url + second_random_char
'H2bk2'
'a2bL0'

Still look very similar...

What if we insert our random chars in position[1] and position[-2]...
'2Hb2k'
'2ab0L'
Looks better now, it is still guessable, but not at first glance.

Auto-incremental id approach drawbacks:
- We will be doing two DB operations, insert and update, every time we create a new record.

  
  

##  Decision:

Even if it is a common problem nowadays, there are plenty of ways to solve it. IMO, there is no perfect solution. Of course there can be a lot of improvements and workarounds in all of the approaches mentioned.

I am sure it's good to think about scaling issues, and think of a distributed system at the beginning. Maybe using tools like Zookeper, or Redis for manage auto-increments. Thinking about caching for a better performance. Purging the DB data. Randomizing the alphabet on base62 encoding... But for this exercise it seems to me like an overkill.

At this moment I will choose approach #2. IMO, it will perform better than the #3rd approach, i better SELECT + INSERT something on a DB than INSERT + UPDATE.

As we will use base62, and we don't have a strict constrain on url length it will generate more than 56 billion urls of length up to 6. If we hit that limit, we can continue generating larger urls. For urls of length 7 we can have more than 3 trillion (62^7) unique urls.

  

## How to use
```
# Clone this repo
git clone this repo && cd repo

# Create virtualenv (highly recommended)
virtualenv -p python3 .env

# Activate virtualenv
.env/source/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run flask project
FLASK_ENV=development flask run

# API will be running @ http://localhost:5000
```

  

## How to use with docker

```
# build docker image
docker build -t url-shortener:latest .
# run docker image
docker run -d --name shortener -p 5000:5000 url-shortener
# API will be running @ http://localhost:5000
```

## Deploy to aws lambda

This project can be deployed to aws lambda using zappa. You must have awscli and AWS credentials configured. Just edit zappa_settings.example.json and rename it to zappa_settings.json
```
zappa deploy <stage>
```
 
## If you are using OSx:  

If you are using OSx: The project uses argon2-cffi package for password hashing. To deploy successfully to lambda, you need to upload linux binaries, so you need to use lambci/lambda:build-python3.7.


```
# build image
docker run --rm -it -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" -v "$PWD":/var/task lambci/lambda:build-python3.7 bash

# run image with bash support
docker run -ti --expose=5000 -e AWS_PROFILE=default -v "$(pwd):/var/task" -v ~/.aws/:/root/.aws --rm lambci/lambda:build-python3.7 bash

# install requirements
pip install -r requirements

# deploy
zappa deploy dev

```

 
## Tests

Tests are written using pytest. Once installed, you can run tests with this commands

```
FLASK_ENV=TEST pytest --verbose
pytest --cov=app tests
```