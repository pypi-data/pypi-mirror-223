from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()
    
setup(
    name='discord_api_info',
    version='2.5',
    packages=find_packages(),
    description="Library to retrieve the latest chrome user agent, version and latest discord client build number.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests>=2.0',
        'beautifulsoup4'
    ],
)
