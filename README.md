# Lambdo
Lamb*do* is a CLI tool that utilizes the Lambda GPU Cloud Public APIs

![help_output.png](lambdo/static/help_output.png)

## Lambda Labs Cloud API
https://docs.lambdalabs.com/public-cloud/cloud-api/

## Lambda Labs Redoc
https://cloud.lambdalabs.com/api/v1/docs

## How does it work?
Lambdo was built using [Typer](https://typer.tiangolo.com) by tiangolo

All of the features included in this page work out of the box, including command completion. Be sure to install it!

I utilized the `requests` library to handle the API calls and `pydantic` to import environment variables.

## Setup
To get started, you should run the setup script to assign your API Key and SSH path so Lambdo can help manage those files
```bash
lambdo setup
```

## First steps
Once this is done, you can now use any of the commands available by Lambdo.

For example, get your currently running GPU instances
```bash
lambdo instances
```
*TODO Add image here with working instance*
