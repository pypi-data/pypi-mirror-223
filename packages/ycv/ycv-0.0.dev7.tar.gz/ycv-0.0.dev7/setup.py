from setuptools import setup

setup(
    name='ycv',
    version='0.0.dev7',
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'ycv=ycv:build_materials_cli'
        ]
    },
)
