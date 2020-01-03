#!/usr/bin/env python

import boto3
import click


class ec2Instances(object):
    def __init__(self):
        self.ec2_resource = boto3.resource('ec2')
        self.ec2_client = boto3.client('ec2')
        self.no_instances = 0

    def list_instances(self, list=None):
        if list is not None:
            if list == 'running' or list == 'RUNNING':
                ec2_instances = self.ec2_resource.instances.filter(
                    Filters=[{'Name': 'instance-state-name',
                              'Values': ['running']}
                             ])
            elif list == 'stopped' or list == 'STOPPED':
                ec2_instances = self.ec2_resource.instances.filter(
                    Filters=[{'Name': 'instance-state-name',
                              'Values': ['stopped']}
                             ])
            else:
                pass

            for instance in ec2_instances:
                self.no_instances += 1
                for tag in instance.tags:
                    click.echo(click.style(tag["Value"], 'green'))
                click.echo(instance.id +
                           " | " +
                           instance.instance_type +
                           " | " +
                           instance.key_name +
                           " | " +
                           instance.private_ip_address +
                           " | " +
                           instance.public_dns_name)
            click.echo("==============\n{} instance(s)".format(
                self.no_instances))

    def destroy_instances(self, instances):
        list_instances = instances

        if len(list_instances) >= 1:
            self.ec2_client.terminate_instances(InstanceIds=list_instances)
        else:
            click.echo("Nothing to destroy.")


class Buckets(object):
    def __init__(self):
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')
        self.no_buckets = 0

    def list_buckets(self):
        for bucket in self.s3_resource.buckets.all():
            self.no_buckets += 1
            click.echo(click.style(bucket.name, 'green'))
        click.echo("============\n{} bucket(s)".format(
            self.no_buckets))

    def list_objects(self, bucket):
        paginator = self.s3_client.get_paginator("list_objects")
        page_iterator = paginator.paginate(Bucket=bucket, Prefix='')
        count = 0

        for page in page_iterator:
            if "Contents" in page:
                for key in page["Contents"]:
                    count += 1
                    click.echo(click.style(key['Key'], 'green'))
        click.echo("==========\n{} file(s)".format(count))


class Iam(object):

    def __init__(self):
        self.iam_resource = boto3.client('iam')

    def list_users(self):
        users = self.iam_resource.list_users()
        count_users = 0
        for user in users['Users']:
            if user:
                count_users += 1
                date = user['CreateDate']
                click.echo(user['UserId'] +
                           ' | ' +
                           click.style(user['UserName'], 'green') +
                           ' | ' +
                           date.strftime('%m/%d/%Y-%X'))
            else:
                click.echo("No user")
        click.echo("==========\n{} user(s)".format(count_users))


class Dynamodb(object):

    def __init__(self):
        self.dydb = boto3.client('dynamodb')

    def list_tables(self):
        tables = self.dydb.list_tables()
        count = 0
        if tables:
            for table in tables['TableNames']:
                count += 1
                click.echo(click.style(table, 'green'))
        click.echo("==========\n{} table(s)".format(count))

    def records(self, table):
        items = self.dydb.scan(TableName=table)
        count = 0

        for item in items['Items']:
            count += 1
            click.echo(click.style(str(item), 'green'))
        click.echo("============\n{} record(s)".format(count))


@click.group()
@click.version_option()
def cli():
    """Manage different cloud resources"""
    pass


@cli.command()
@click.option('--list', '-l', help='Show EC2 instances list')
@click.option('--destroy', '-d', help='Destroy EC2 instances')
def ec2(list, destroy):
    """
    Manage AWS EC2 resources.

    Usage:

    mcloud ec2 --help
    """
    ec2_instances = ec2Instances()

    if list:
        if list == 'running' or list == 'RUNNING':
            ec2_instances.list_instances(list)
        elif list == 'stopped' or list == 'STOPPED':
            ec2_instances.list_instances(list)
        else:
            click.echo(
                "Please sepcify LIST parameter. E.g. --list [running/stopped]")

    if destroy:
        if click.confirm('Are you sure you want to destry instance(s)?'):
            destroy_list = destroy.split(",")
            ec2_instances.destroy_instances(destroy_list)


@cli.command()
@click.option('--buckets', '-b', is_flag=True, help='List all s3 buckets')
@click.option('--bucket', help='Give bucket name for list all files')
def s3(buckets, bucket):
    """
    Manage AWS S3 resources.

    Usage:

    mcloud s3 --help
    """
    s3_buckets = Buckets()

    if buckets:
        s3_buckets.list_buckets()
    if bucket:
        s3_buckets.list_objects(bucket)


@cli.command()
@click.option('--users', '-u', is_flag=True, help='List all users')
def iam(users):
    """
    Manage AWS IAM resources.

    Usage:

    mcloud iam --help
    """
    iam_resource = Iam()

    if users:
        iam_resource.list_users()


@cli.command()
@click.option('--tables', '-t', is_flag=True, help='List all tables')
@click.option('--records', '-r', help='List records of specific table')
def dynamodb(tables, records):
    """
    Manage AWS DynamoDB resources.

    Usage:

    mcloud dynamodb --help
    """
    dyndb_resource = Dynamodb()

    if tables:
        dyndb_resource.list_tables()
    if records:
        dyndb_resource.records(records)
