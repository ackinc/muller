# muller

Credit card statements are useful as address proof, so this is a little app
that ensures I always have my latest credit card statement handy

## Intended Behaviour

- Trawl through emails (gmail support only; email address must be provided as an env var)
  to find the latest credit card statement
- Download the statement (script assumes it's a pdf attachment)
- Strip password if any (password must be provided as the env var)
- Extract the first page (usually the one that contains the address)
- Upload the extracted page to google drive (location to be provided as an env var)

## Deployment Notes

- This app will be deployed to Heroku
- Since it requires the `pdfseparate` utility which is not installed by default on
  Heroku dynos, I'll have to work with a custom buildpack to make it available
