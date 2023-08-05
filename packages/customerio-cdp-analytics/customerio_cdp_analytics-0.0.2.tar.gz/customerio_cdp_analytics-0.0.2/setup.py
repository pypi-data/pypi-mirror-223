import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
# Don't import the module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'customerio','analytics'))
from version import VERSION

long_description = '''
Customer.io Data Pipelines (CDP) is a customer data platform to improve decision-making with real-time updates and deliver personalized experiences.

This is the official python client that wraps the Customer.io Data Pipelines REST API (https://customer.io/docs/cdp/getting-started/cdp-getting-started/).
'''

install_requires = [
    "requests~=2.7",
    "monotonic~=1.5",
    "backoff~=2.1",
    "python-dateutil~=2.2"
]

tests_require = [
    "mock==2.0.0",
    "pylint==2.8.0",
    "flake8==3.7.9",
]

setup(
    name='customerio_cdp_analytics',
    version=VERSION,
    url='https://github.com/customerio/cdp-analytics-python',
    author='Customer.io',
    author_email='cdp@customer.io',
    maintainer='Customer.io',
    maintainer_email='cdp@customer.io',
    test_suite='analytics.test.all',
    packages=['customerio.analytics'],
    python_requires='>=3.6.0',
    license='MIT License',
    install_requires=install_requires,
    extras_require={
        'test': tests_require
    },
    description='Customer.io Data Pipelines (CDP) is a customer data platform to improve decision-making with real-time updates and deliver personalized experiences.',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
