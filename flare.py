#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Cloudflare Cli tool
Flare talks to Cloudflare API directly so you don't have to.
"""
import json
import os
import sys
import click
import yaml
import requests


def get_api_cred():
    """Retrieve API Key from local YAML file."""
    home_dir = os.path.expanduser('~')
    file_suffix = '.yaml'
    yaml_path = os.path.join(home_dir, '.flare' + file_suffix)
    try:
        with open(yaml_path, 'r', encoding='utf8') as stream:
            cred_loaded = yaml.safe_load(stream)
    except FileNotFoundError as e:
        print('[ ERROR ] ' + str(e))
        sys.exit(1)
    else:
        return cred_loaded


def get_paged_info(uri, additional_params=None):
    """Retreive data from API through pagination."""
    first_page = get_info(uri)
    yield first_page['result']
    num_pages = first_page['result_info']['total_pages']

    for page in range(2, num_pages + 1):
        # Check for additional parameters
        if additional_params is None:
            params_value = {'page': page}
        else:
            params_value = {'page': page}
            params_value.update(additional_params)
        next_page = get_info(uri, params_value)
        yield next_page['result']


def get_info(uri, additional_params=None):
    """Retrieve single page data from API."""
    if additional_params is None:
        result = requests.request("GET", uri, headers=HEADERS)
    else:
        result = requests.request("GET", uri, headers=HEADERS, params=additional_params)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('[ HTTP ERROR ] ' + str(e))
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print('[ Connection ERROR ] ' + str(e))
        sys.exit(1)
    except requests.exceptions.Timeout as e:
        print('[ Timeout ERROR ] ' + str(e))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('[ ERROR ] ' + str(e))
        sys.exit(1)
    result_json = json.loads(result.text)
    return result_json

def patch_request(uri, additional_params=None):
    """Patch request through API"""
    if additional_params is None:
        result = requests.request("PATCH", uri, headers=HEADERS)
    else:
        result = requests.request("PATCH", uri, headers=HEADERS, data=additional_params)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('[ HTTP ERROR ] ' + str(e))
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print('[ Connection ERROR ] ' + str(e))
        sys.exit(1)
    except requests.exceptions.Timeout as e:
        print('[ Timeout ERROR ] ' + str(e))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('[ ERROR ] ' + str(e))
        sys.exit(1)
    result_json = json.loads(result.text)
    return result_json

@click.group()
def cli():
    """Initialize Click command."""
    global API_TOKEN, API_KEY, API_EMAIL, HEADERS, URL
    URL = "https://api.cloudflare.com/client/v4/"
    api_cred = get_api_cred()
    if api_cred['API_EMAIL'] is None:
        API_TOKEN = api_cred['API_TOKEN']
        HEADERS = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + API_TOKEN,
        }
    else:
        API_EMAIL = api_cred['API_EMAIL']
        API_KEY = api_cred['API_KEY']
        HEADERS = {
            'Content-Type': 'application/json',
            'X-Auth-Email': API_EMAIL,
            'X-Auth-Key': API_KEY,
        }


@cli.command('list-accounts')
def list_accounts():
    """List all accounts."""
    uri = URL + 'accounts'
    results = []
    # get paginated results
    for page in get_paged_info(uri):
        results += page

    print(json.dumps(results, indent=4))


@cli.command('list-dns-records')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
def list_dns_records(zoneid):
    """List all DNS records for a site."""
    uri = URL + 'zones/' + zoneid + '/dns_records'
    results = []

    for page in get_paged_info(uri):
        results += page

    print(json.dumps(results, indent=4))


@cli.command('list-fw-rules')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
def list_fw_rules(zoneid):
    """List all firewall rules under a site."""
    uri = URL + 'zones/' + zoneid + '/firewall/rules'
    results = []
    # get paginated results
    for page in get_paged_info(uri):
        results += page

    print(json.dumps(results, indent=4))


@cli.command('list-logpush-jobs')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
def list_logpush_jobs(zoneid):
    """List logpush jobs for a site."""
    uri = URL + 'zones/' + zoneid + '/logpush/jobs'
    response = get_info(uri)
    print(json.dumps(response['result'], indent=4))


@cli.command('list-page-rules')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
def list_page_rules(zoneid):
    """List Page Rules for a site."""
    uri = URL + 'zones/' + zoneid + '/pagerules'
    response = get_info(uri)
    print(json.dumps(response['result'], indent=4))


@cli.command('list-ssl-packs')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
def list_ssl_packs(zoneid):
    """List all SSL certificate packs for a site."""
    uri = URL + 'zones/' + zoneid + '/ssl/certificate_packs'
    response = get_info(uri)
    print(json.dumps(response['result'], indent=4))


@cli.command('list-ssl-verification')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
def list_ssl_verification(zoneid):
    """List all SSL verifications for a site."""
    uri = URL + 'zones/' + zoneid + '/ssl/verification'
    response = get_info(uri)
    print(json.dumps(response['result'], indent=4))


@cli.command('list-waf-groups')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
@click.option('--packageid', '-p', required=True, help="Cloudflare WAF Package Id.")
def list_waf_groups(zoneid, packageid):
    """List groups of a WAF package under a site."""
    uri = URL + 'zones/' + zoneid + '/firewall/waf/packages/' + packageid + '/groups'
    results = []

    for page in get_paged_info(uri):
        results += page

    print(json.dumps(results, indent=4))


@cli.command('list-waf-packages')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
def list_waf_packages(zoneid):
    """List WAF available packages for a site."""
    uri = URL + 'zones/' + zoneid + '/firewall/waf/packages'
    response = get_info(uri)
    print(json.dumps(response['result'], indent=4))


@cli.command('list-waf-rules')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
@click.option('--packageid', '-p', required=True, help="Cloudflare WAF Package Id.")
@click.option('--groupid', '-g', required=True, help="Cloudflare WAF Package Group Id.")
def list_waf_rules(zoneid, packageid, groupid):
    """List all waf rules for a site."""
    uri = URL + 'zones/' + zoneid + '/firewall/waf/packages/' + packageid + '/rules'
    groupid_param={'group_id': groupid}
    results = []

    for page in get_paged_info(uri,groupid_param):
        results += page

    print(json.dumps(results, indent=4))


@cli.command('list-workers')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
def list_workers(zoneid):
    """List all Workers for a site."""
    uri = URL + 'zones/' + zoneid + '/workers/scripts'
    response = get_info(uri)
    print(json.dumps(response['result'], indent=4))


@cli.command('list-zones')
def list_zones():
    """List all zones available in the accounts."""
    uri = URL + 'zones'
    results = []
    # get paginated results
    for page in get_paged_info(uri):
        results += page

    print(json.dumps(results, indent=4))


@cli.command('validate-certificate')
@click.option('--zoneid', '-z', required=True, help="Cloudflare Zone Id.")
@click.option('--packuuid', '-p', required=True, help="Certificate Pack UUID.")
def validate_certificate(zoneid, packuuid):
    """Validate Certificate use Certificate Pack UUID."""
    uri = URL + 'zones/' + zoneid + '/ssl/verification/' + packuuid
    payload=json.dumps({
        "validation_method":"txt"
    })
    response = patch_request(uri,payload)
    print(json.dumps(response, indent=4))


if __name__ == '__main__':
    cli()
