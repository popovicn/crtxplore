import argparse

import requests


def fail(msg, exit_code=1):
    print('Error:', msg)
    exit(exit_code)


def get_subdomains(domain, exclude_wildcard, exclude_expired, timeout):
    url = 'https://crt.sh/?q={}&deduplicate=Y&output=json'.format(domain)
    if exclude_expired:
        url += '&exclude=expired'
    try:
        response = requests.get('https://crt.sh/?q={}&deduplicate=Y&output=json'.format(domain),
                                timeout=timeout,
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0aaa'
                                })
    except requests.Timeout:
        fail('Response timed out.')
    except requests.RequestException as e:
        fail(str(e))

    if response.status_code != 200:
        fail('response status {}'.format(response.status_code))

    subdomain_set = set()
    for cert in response.json():
        name_value = cert.get('name_value')
        if not name_value:
            continue
        if '\n' in name_value:
            for subdomain in name_value.split('\n'):
                if exclude_wildcard:
                    if '*' not in subdomain:
                        subdomain_set.add(subdomain)
                else:
                    subdomain_set.add(subdomain)
        else:
            if exclude_wildcard:
                if '*' not in name_value:
                    subdomain_set.add(name_value)
            else:
                subdomain_set.add(name_value)

    return subdomain_set


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required_args = parser.add_argument_group('required arguments')
    optional_args = parser.add_argument_group('optional arguments')
    required_args.add_argument('-d', dest='domain', help='Target domain', required=True)
    optional_args.add_argument('-ew', dest='exclude_wildcard', action='store_true', help='Exclude wildcard(*) subdomains')
    optional_args.add_argument('-ee', dest='exclude_expired', action='store_true', help='Exclude expired certificates')
    optional_args.add_argument('-t', dest='timeout', help='Timeout', type=float)
    optional_args.add_argument('-o', dest='output_file_path', help='Output file')
    args = parser.parse_args()

    subdomains = get_subdomains(args.domain, args.exclude_wildcard, args.exclude_expired, args.timeout)
    for subdomain in subdomains:
        print(subdomain)
    if args.output_file_path:
        with open(args.output_file_path, 'w+') as output_file:
            output_file.write('\n'.join(subdomains))
