import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fadeaway",
    version="1.0.1",
    author="rain",
    author_email="948628463@qq.com",
    description="fadeaway is a lightweight WSGI web application framework which depends on the Werkzeug WSGI toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cgynb/fadeaway",
    packages=setuptools.find_packages(),
    install_requires=['werkzeug>=2.3.6'],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
)
