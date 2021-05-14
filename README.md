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

- This app will be deployed to a Heroku dyno running the [Heroku-20][1] stack
  - Since it requires the `pdftops` and `pdfseparate` utilities which are not installed by
    default on Heroku dynos running cedar-20 (must install the `poppler-utils`
    package to get them), I'm be using the [heroku-community/apt][2] third-party buildpack to
    make them available

[1]: https://devcenter.heroku.com/articles/heroku-20-stack
[2]: https://github.com/heroku/heroku-buildpack-apt
