import requests
import backoff
import logging


log = logging.getLogger(__name__)


@backoff.on_exception(backoff.constant, (requests.exceptions.RequestException),
                      jitter=backoff.random_jitter, max_tries=5, interval=30)
def get_users(num_users):
    response = requests.get(url='https://randomuser.me/api',
                            params={'format': 'csv',
                                    'inc': 'name,location,email,dob,registered,phone,nat',
                                    'nat': 'us,dk,fr,gb',
                                    'results': num_users}
                            )
    response.raise_for_status()
    return response


def main():
    response = get_users(50)
    with open('users.csv', 'w') as f:
        f.write(response.text)
        f.write('\n')


if __name__ == '__main__':
    main()
