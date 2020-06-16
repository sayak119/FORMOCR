from setuptools import setup

setup(
   name='pythonForm',
   version='1.0',
   description='A module to extrat key value from form',
   author='Sayak Kundu',
   author_email='sk.sayakkundu1997@gmail.com',
   packages=['pythonForm'],  #same as name
   package_dir={'pythonForm': 'pythonForm'},  
   install_requires=['google-cloud-vision==1.0.0','numpy==1.18.4','opencv-python==4.2.0.34', 'google-api-core==1.17.0', 'grpcio==1.29.0'], #external packages as dependencies
)
