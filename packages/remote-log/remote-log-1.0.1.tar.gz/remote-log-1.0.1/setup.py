from setuptools import setup, find_packages
setup(
    name='remote-log',
    version='1.0.1',
    packages=find_packages(),
    description = 'A simple function to send logging data to a remote server.',
    long_description='''
    It sends a POST request to the server with the data you passed. If the system is offline, it stored the logs offline and sends all the data on the next call of remote_log.\n
    This way you are always assured you will receive the data to be logged.\n
    It also sends basic system information. Any uniquely identifiable information is not sent as plain text. It is hashed on the system using SHA256 before being sent. This way the logging server can still uniquely identify a log request but have no traceability back to the system that sent it thus allowing you to take a privacy first approach to logging.
    \n\n
    The function remote_log is non blocking and doesn't return anything. It's only purpose is to send logging data.
    ''',
    author = 'Shubham Gupta',
    author_email = 'shubhastro2@gmail.com',
    install_requires=[
            'psutil',
            'py-cpuinfo',
            'requests',
        ],
)