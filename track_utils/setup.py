from setuptools import setup, find_packages

setup(
    name='track_utils',
    version='1.0.0',
    packages=['track_utils', 'track_utils.metrics'],
    package_dir={'track_utils': 'track_utils'},
    url='https://github.com/hushchyn-mikhail/track_utils.git',
    license='',
    author='Mikhail Hushchyn',
    author_email='mikahil91@yandex-team.ru',
    description='Utils for track pattern recognition.',
    install_requires=['numpy>=1.11.0'],
)
