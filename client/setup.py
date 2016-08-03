#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sz yongle'
import os,glob
from distutils.core import setup  
import py2exe  
import sys
from PyQt4 import QtCore, QtGui
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

sys.path.append(r'G:\Python27\Lib')
INCLUDES = ['sip','VideoCapture','PIL','ImageFont','win32com','win32gui','PyQt4.Qt','PyQt4.QtWebKit',"xml"]

MANIFEST_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="1.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="requireAdministrator"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.21022.8"
            processorArchitecture="x86"
            publicKeyToken="1fc8b3b9a1e18e3b">
      </assemblyIdentity>
    </dependentAssembly>
  </dependency>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
  </dependency>
</assembly>
"""
RT_MANIFEST = 24



options = {"py2exe" :
    {"compressed" : 1,
     "optimize" : 2,
     "bundle_files" : 3,
     "ascii":1,
     "includes" : INCLUDES,
     "packages":["encodings"],
     "dll_excludes": [ "MSVCP90.dll", "mswsock.dll", "powrprof.dll",'win32ui','pywin','pywin.debugger'],
     "typelibs": [('{D95CB779-00CB-4B49-97B9-9F0B61CAB3C1}', 0, 4, 0), ]  
      }}

windows = [{"script": "Main.py",
      "icon_resources": [(1, "logo.ico")],
      "other_resources" : [(RT_MANIFEST, 1,
                        MANIFEST_TEMPLATE % dict(prog="yonglefinger"))],
      }]

data_files = [('image', glob.glob('image/*.*')),
('img', glob.glob('img/*.*')),
('img/kt', glob.glob('img/kt/*.*')),
('img/newIcos', glob.glob('img/newIcos/*.*')),
('dll', glob.glob('dll/*.*')),
('.', glob.glob('config.ini')),
('print', glob.glob('print/*.*')),
('log', glob.glob('log/*.*')),
('.', glob.glob('log.conf')),
('.',glob.glob('*.ico')),
('.',glob.glob(os.path.dirname(os.__file__)+'\\*.pil')),
('.',glob.glob(os.path.dirname(os.__file__)+'\\*.png'))
#('.', [os.path.join(os.environ['SystemRoot'], 'system32', 'msvcp71.dll')])
]


setup(name = "sz yongyle",
      version = "1.0",
      description = "vip card system",
      author = "yl",
      author_email ="42320756@qq.com",
      maintainer = "huboqiao",
      maintainer_email = "42320756@qq.com",
      license = "yl",
      url = "http://www.3uni.com",
      zipfile='VIPcore.dll',
      data_files = data_files,
      options = options,
      windows = windows,
      
      )