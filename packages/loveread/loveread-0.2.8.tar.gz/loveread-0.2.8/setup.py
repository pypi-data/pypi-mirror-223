from setuptools import setup

setup(
    name="loveread",
    version="0.2.8",
    author="Vlad Havrylov",
    author_email="wladgavrilov@gmail.com",
    description="A brief description of your package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://gitlab.com/wladgavrilov/loveread",
    packages=['loveread'],
    install_requires=["bs4"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)