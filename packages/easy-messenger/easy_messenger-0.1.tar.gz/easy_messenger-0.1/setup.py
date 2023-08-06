from distutils.core import setup
setup(
  name = 'easy_messenger',        
  packages = ['easy_messenger'],   
  version = '0.1',     
  license='MIT',        
  description = 'The simplest Messenger (Facebook, Instagram) API wrapper out there',   
  author = 'Tomas Santana',               
  author_email = 'tommysantana5@gmail.com',    
  url = 'https://github.com/Tomas-Santana/',   
  download_url = 'https://github.com/Tomas-Santana/easy_messenger/archive/refs/tags/v0.1.tar.gz',    
  keywords = ['Instagram', 'Facebook', 'API', 'Wrapper'],  
  install_requires=[            
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
  ],)