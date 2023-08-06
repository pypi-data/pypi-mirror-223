from setuptools import setup, find_packages

setup(
    name='bardclient',
    version='1.0',
    license='MIT License',
    author='yangdage',
    author_email = '314474977@qq.com',
    description="A simple reverse engineering of google's bard implements by python3",
    package_dir=find_packages('src'),
    url="https://github.com/ydg119/bardclient",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    py_modules=["bardclient"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],

)
