""" 

Makes app installable through pip and play nicely with flask features 

    Flask documentation pros of setting up your app as a package:

        - Currently, Python and Flask understand how to use the package
        only because you’re running from your project’s directory.
        Installing means you can import it no matter where you run from.

        - Manage your project’s dependencies just like other packages do,
        so pip install yourproject.whl installs them.

        - Test tools can isolate your test environment from your development environment. '

"""

from setuptools import find_packages, setup

setup(
    name='ailerons-tracker-backend',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
