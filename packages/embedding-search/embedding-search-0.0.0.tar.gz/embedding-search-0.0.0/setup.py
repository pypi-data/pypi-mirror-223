from setuptools import setup, find_packages

setup(
    name='embedding-search',
    version='0.0.0',
    description='embedding search',
    author='sangyeop',
    author_email='pdg01117@gmail.com',
    url='https://github.com/sangyeop-kim/embedding-search',
    install_requires=['numpy'],
    packages=find_packages(exclude=[]),
    keywords=['coxwave', 'pdg01117', 'embedding', 'search', 'semantic', 'vector'],
    python_requires='>=3.7',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)