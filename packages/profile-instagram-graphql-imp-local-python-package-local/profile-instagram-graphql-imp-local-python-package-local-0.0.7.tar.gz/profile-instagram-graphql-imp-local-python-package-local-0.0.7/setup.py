import setuptools
# Each Python project should have pyproject.toml or setup.py
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including current pre-release) as we have moved away from needing to generate a setup.py file to enable editable installs - We might able to delete this file in the near future
setuptools.setup(
     name='profile-instagram-graphql-imp-local-python-package-local',  
     version='0.0.7', #https://pypi.org/project/profile-instagram-graphql-imp-local-python-package-local/
     author="Circles",
     author_email="info@circles.life",
     description="PyPI Package for Circles profile-instagram-graphql-imp-local-python-package Local Python",
     long_description="This is a package for importing data from Instagram business accounts.",
     long_description_content_type="text/markdown",
     url="https://github.com/circles",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
     ],
 )
