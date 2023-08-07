import os
from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

REQUIRES = ['requests']

about = {}
here = os.path.abspath(os.path.dirname(__file__))
print(here)
with open(os.path.join(here, "techo", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=["techo"],
    package_data={"": ["LICENSE", "NOTICE"]},
    package_dir={"techo": "techo"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=REQUIRES,
    license=about["__license__"],
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Environment :: Console',
        'Natural Language :: English',
    ],
    project_urls={
        "Source": "https://github.com/nanason01/techoFrontend",
    },
)
