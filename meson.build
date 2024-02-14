project('tessbind', 'cpp',
  version : '0.0.2',
  default_options : ['warning_level=3', 'cpp_std=c++14'])

pymod = import('python')
py = pymod.find_installation('python3')
py.extension_module('tessbind', sources : 'src/main.cpp', dependencies : [
  dependency('python3'),
  dependency('lept'),
  dependency('tesseract'),
  ])
