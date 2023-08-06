from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='env_minion',
    version='0.0.4',
    description='Enforces environmental variable conformance with template shared across team',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NikaEco/env-minion',
    author='Nisemono',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'gru = env_minion.hook_factory:create_all_hooks',
        ]
    }
)