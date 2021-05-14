# muller

Credit card statements are useful as address proof, so this is a little app
that ensures I always have my latest credit card statement handy

## Intended Behaviour

- Trawl through emails (gmail support only; email address must be provided as an env var)
  to find the latest credit card statement
  - It's assumed that the most recently received email with "Credit Card Statement" in the subject
    and a pdf attachment is our target
- Download the statement pdf
- Strip password if any (password must be provided as the env var)
- Extract the first page (usually the one that contains the address)
- Upload the extracted page to google drive (location to be provided as an env var)

## Deployment Notes

- This app will be deployed to a Heroku dyno running Ubuntu
  - Since it requires the `pdftops`, `pdfseparate`, and `ghostscript`
    utilities which are not installed by default on Heroku dynos
    (run `apt install ghostscript poppler-utils` to get them),
    I'll have to work with a custom buildpack to make them available
