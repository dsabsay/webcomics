from setuptools import find_packages, setup

setup(
    name='webcomics',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask>=1.1.1',
        'daemonize>=2.5.0',
        'psutil>=5.6.3',
        'schedule>=0.6.0'
    ],
)
