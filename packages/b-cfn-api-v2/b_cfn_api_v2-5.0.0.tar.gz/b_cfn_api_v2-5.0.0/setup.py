from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('VERSION') as file:
    VERSION = file.read()
    VERSION = ''.join(VERSION.split())

setup(
    name='b_cfn_api_v2',
    version=VERSION,
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        # Exclude test source files.
        'b_cfn_api_v2_test'
    ]),
    description=(
        'Convenient wrapper around CfnApi.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'b-cfn-custom-userpool-authorizer>=2.0.0,<3.0.0',
        'b_cfn_custom_api_key_authorizer>=3.0.0,<4.0.0',

        # AWS CDK.
        'aws-cdk-lib>=2.0.0,<3.0.0',
        'aws-cdk-constructs>=2.0.0,<3.0.0',
    ],
    keywords='AWS API Gateway',
    url='https://github.com/biomapas/B.CfnApiV2.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
