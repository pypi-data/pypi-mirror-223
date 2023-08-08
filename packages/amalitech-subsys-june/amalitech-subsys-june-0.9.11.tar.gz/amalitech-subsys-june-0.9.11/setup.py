from setuptools import find_packages, setup

setup(
    name="amalitech-subsys-june",
    version="0.9.11",
    packages=find_packages(),
    entry_points={"console_scripts": ["subsys = app.subsys:cli"]},
    install_requires=["click", "requests", "tqdm", "python-slugify"],
    author="Charles Biney, Eric Kodzi, Donal-Miles Gyasi",
    author_email="charles.biney@amalitech.org, eric.kodzi@amalitech.org, donal-miles.gyasi@amalitech.org",
    description="A git inspired assignment submission system.",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
