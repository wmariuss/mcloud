# mcloud

Simple cloud resources management tool.

## Requirements

* `Python >= 3.6`
* AWS credentials file with credentials (you can setup using awscli)

## Install

* `pip install requirements.txt`

## Usage

* `mcloud --help`

Commands available:

* `ec2 --list/-l running/stopped`
* `ec2 --destroy/-d [list_IDs_instances]`
* `s3 --buckets/-b`
* `s3 --bucket bucket_name`
* `iam --users/-u`
* `dynamodb --tables/-t`
* `dynamodb --records/-r [table_name]`

## Contribute

Contributions are always welcome.

* Fork the repo
* Create a pull request against master
* Be sure tests pass (if exists)

Check [Git Flow](https://guides.github.com/introduction/flow/) for details.

## Authors

* [Marius Stanca](mailto:me@marius.xyz)
