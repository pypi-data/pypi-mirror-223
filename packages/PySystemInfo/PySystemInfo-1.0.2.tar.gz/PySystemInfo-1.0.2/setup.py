import setuptools

setuptools.setup(
    name='PySystemInfo',
    version='1.0.2',
    description='It s a package that allows you to easily find out the system information of your computer through Python',
    author='Gaeduck',
    author_email='gms8757@naver.com',
    url='https://github.com/Gaeduck-0908/PySystemInfo',
    install_requires=['psutil ', 'py-cpuinfo', 'GPUtil'],
    packages= setuptools.find_packages(),
    keywords=['Sysinfo', 'system', 'SystemInfo', 'Python system', 'Python System info'],
    python_requires='>=3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)