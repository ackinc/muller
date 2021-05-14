# muller

Credit card statements are useful as address proof, so this is a little app
that ensures I always have my latest credit card statement handy

## Behaviour

- Trawl through emails (gmail support only; email address must be provided as an env var)
  to find the latest credit card statement
  - The filter used to find credit card statement emails is specified as an env var
- Download the statement (pdf attachment on the email)
- Strip password if any (password must be provided as an env var)
- Extract the first page (usually the one that contains the address)
- Upload the extracted page to google drive (location to be provided as an env var)

## Deployment Notes

- This app will be deployed to a Heroku dyno running Ubuntu
  - Since it requires the `pdftops`, `pdfseparate`, and `ghostscript`
    utilities which are not installed by default on Heroku dynos
    (run `apt install ghostscript poppler-utils` to get them),
    I'll have to work with a custom buildpack to make them available
