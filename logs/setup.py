from distutils.core import setup
setup(
    name='open-notify-api-logs',
    packages=['nginx_parse'],
    version='1.0.0',
    description='Open Notify API server logfile parser',
    author='Nathan Bergey',
    license='GNU General Public License v3.0',
    author_email='nathan@open-notify.org',
    url='https://api.open-notify.org/',
    keywords=['api', 'nasa', 'space', 'iss', 'logs', 'nginx', 'datadog', 'statsd'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    scripts=['datadog-monitor.py']
)
