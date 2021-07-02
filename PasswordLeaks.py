import requests
import hashlib
# import sys


def request_api_data(query_char):  # query_char is first 5 digits of hashed password
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check API')
    return res


def get_password_leaks_count(hashes, hash_to_check):  # hashes is response that contains password and number
    hashes = (line.split(':') for line in hashes.text.splitlines())  # splitting hashes in a tuple
    for h, count in hashes:  # hashes is a generator object that can be looped through
        if h == hash_to_check:  # if tail hash == our tail, return count/how many times it has been leaked
            return count
    return 0


def pwned_api_check(password):  # password is actual password in text
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()   # running our password through SHA1
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)  # response is tail of hashed passwords that match first5_char of password
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times, change your password')
        else:
            print(f'{password} was NOT found')


if __name__ == '__main__':
    # reading from command line
    # sys.exit(main(sys.argv[1:]))

    # reading from text file is more secure
    with open('../password.txt', 'r') as file:
        data = file.readlines()
        main(data)