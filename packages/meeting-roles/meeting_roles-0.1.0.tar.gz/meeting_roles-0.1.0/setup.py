from setuptools import setup, find_packages

setup(
    name="meeting_roles",
    version="0.1.0",
    description="A FastAPI web app to manage meeting roles",
    author="Coopdevs",
    author_email="pelayo.garcia@coopdevs.org",
    url="https://git.coopdevs.org/coopdevs/tooling/meeting-roles-manager",
    packages=find_packages(),
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "fastapi",
        "sqlite3",
        "aiofiles",
        "python-multipart",        
    ],
    entry_points={
        "console_scripts": [
            "meeting_roles=meeting_roles.run:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
