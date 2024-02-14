project('tessbind', 'cpp',
  version : '0.1',
  default_options : ['warning_level=3', 'cpp_std=c++14'])

pymod = import('python')
py = pymod.find_installation('python3')
py.extension_module('example', sources : 'example.cpp', dependencies : dependency('python3'))
