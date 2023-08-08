import setuptools
import time

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 版本
today = time.strftime("%Y%m%d", time.localtime(time.time()))

version_filename = "src/lightning_trainer/__init__.py"
with open(version_filename, "r") as fr:
    text = ""
    for line in fr.readlines():
        if "__version__" in line:
            text += f"__version__ = \"{today}\"\n"
        else:
            text += line
with open(version_filename, "w") as fw:
    fw.write(text)


setuptools.setup(
    name="lightning_trainer",
    version=today,
    author="Wenkai Liu",
    author_email="wenkai_liu@hust.edu.cn",
    description="Makes training models easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wkailiu/lightning_trainer",
    project_urls={
        "Bug Tracker": "https://github.com/wkailiu/lightning_trainer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.yaml", "*.npy"],
        # And include any *.msg files found in the 'hello' package, too:
        # "hello": ["*.msg"],
    },
    python_requires=">=3.6",
    install_requires=[
        "rich>=11.0",
        "logzero",
        "omegaconf",
        "psutil",
    ],
    entry_points={
        'console_scripts': [
            'lightning_trainer=lightning_trainer:run_train',
        ]
    }
)