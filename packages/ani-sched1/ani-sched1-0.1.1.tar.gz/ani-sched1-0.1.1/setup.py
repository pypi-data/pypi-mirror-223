import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="ani-sched1",
    version="0.1.1",
    description="A local API for anime schedules and news (livechart.me)",
    license="MIT",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    author="lkaijie",
    author_email="",
    url="https://github.com/lkaijie/ani-sched-api",
    packages=setuptools.find_packages(),
    install_requires=["requests", "beautifulsoup4","selenium","feedparser"],
    keywords=["api", "myanimelist", "anime", "schedule", "news", "livechart"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)