from setuptools import setup

setup(
    name='meggie_difference',
    version='0.1.1',
    license='BSD',
    packages=['meggie_difference'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'meggie>=1.3.0',
    ]
)
