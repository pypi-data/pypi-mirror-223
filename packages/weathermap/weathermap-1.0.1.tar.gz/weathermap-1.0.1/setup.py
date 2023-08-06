from setuptools import setup, find_packages

setup(
    name='weathermap',
    version='1.0.1',
    description='Openweathermap api simplified',
    author='Savan Patel',
    author_email='sawanpatel2508@gmail.com',
    url='https://github.com/savan2508/WeatherApp',
    packages=find_packages(exclude=['tests']),
    keywords=['weather', 'forecast', 'openweathermap', 'openweather'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
