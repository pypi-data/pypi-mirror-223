from setuptools import setup, find_packages

# Зчитуємо вміст файлу README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="PythonPackageUpdateChecker",
    version="1.0.15",
    description="A utility to automatically check for updates of installed Python packages and update them to the latest versions.",
    long_description=long_description,
    # Вказуємо тип контенту для README.md
    long_description_content_type="text/markdown",
    author="Andrii Bohachev",
    author_email="andriybogachev@gmail.com",
    packages=find_packages(),
    install_requires=["setuptools", "aiohttp", "tqdm", "asyncio"],
    entry_points={
        "console_scripts": [
            "PythonPackageUpdateChecker = PythonPackageUpdateChecker:__main__"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    # exclude_package_data={"": ["subprocess", "winsound", "pkg_resources"]},
    python_requires=">=3.6",
    keywords="python package update checker utility async aiohttp",
    project_urls={
        "Source": "https://github.com/andriybogachev/PythonPackageUpdateChecker",
        "Bug Reports": "https://github.com/andriybogachev/PythonPackageUpdateChecker/issues",
    },
    license="MIT",
)
