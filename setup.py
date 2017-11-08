from distutils.core import setup
setup(
    name='open-notify-api',
    packages=[],
    version='1.0.1',
    description='Open Notify API server',
    author='Nathan Bergey',
    license='GNU General Public License v3.0',
    author_email='nathan@open-notify.org',
    url='https://api.open-notify.org/',
    keywords=['api', 'nasa', 'space', 'iss'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    scripts=['server.py', 'update_astros.py', 'update_iss_position.py', 'update_tle.py']
)
