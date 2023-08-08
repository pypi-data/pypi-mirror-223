from setuptools import setup

setup(
    name='edx-analytics-logger',
    version='1.2.1',
    packages=['edx_analytics_logger'],
    url='https://github.com/javi-aranda/edx-analytics-logger',
    license='MIT',
    author='javisenberg',
    description='edx powered ApiBackend',
    long_description=open('README.rst').read(),
    install_requires=[
        'celery',
        'requests',
    ]
)
