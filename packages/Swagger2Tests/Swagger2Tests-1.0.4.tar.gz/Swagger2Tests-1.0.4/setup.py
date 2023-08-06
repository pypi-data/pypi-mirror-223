from setuptools import setup, find_packages

readmepath = 'README.md'
setup(
    name='Swagger2Tests',
    version='1.0.4',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Swagger2Tests = src.loadswagger:main'
        ]
    },
    install_requires=[
        'argparse','jinja2','pytest','requests','coloredlogs','Faker'
    ],
    author='visonforcoding',
    author_email='visonforcoding@gmail.com',
    description='swagger',
    long_description=open(readmepath, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://gitee.com/visonforcoding/code-template-tools',
    package_data={
        "": ["helpers", "templates","constants"],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)