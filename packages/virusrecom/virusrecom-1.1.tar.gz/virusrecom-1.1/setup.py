import setuptools

with open("README.rst", "r",encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="virusrecom",
  install_requires=["matplotlib","pandas","numpy", "scipy"],
  version="1.1",
  author="Zhi-Jian Zhou",
  author_email="zjzhou@hnu.edu.cn",
  description="An information-theory-based method for recombination detection of viral lineages.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ZhijianZhou01/virusrecom",
  packages=setuptools.find_packages(),
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
)
