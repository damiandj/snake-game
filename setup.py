from setuptools import setup, find_packages

with open("requirements.txt") as fp:
    install_requires = fp.read()

setup(
    name="snake_game",
    description="Snake game ",
    url="https://github.com/damiandj/snake-game/",
    author="Damian Jabłczyk",
    author_email="damianjablczyk@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=[],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={
        "console_scripts": [
            "snake=snake_game.run_game_with_gui:main",
        ],
    },
)
