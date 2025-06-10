#!/bin/python3
import hjson  
from mako.template import Template
import subprocess
import os.path
from pathlib import Path
import shutil

cfg_file = open("ip.cfg", 'r', encoding='utf-8')
ip_cfg   = hjson.loads(cfg_file.read())

# Создаем обязательные директории
core_path = os.getcwd() + '/../' + ip_cfg['name']

if not os.path.exists(core_path): 
  os.mkdir(core_path)

for cur_dir in ["hw", "hw/rtl", "dv", "dv/cocotb", "doc", "data"]: 
  cur_path = core_path + '/' + cur_dir
  if not os.path.exists(cur_path):
    os.mkdir(cur_path)

# Копируем файл конфигурации ядра
shutil.copy(os.getcwd() + '/ip.cfg', core_path + '/data/ip.cfg')
  
# Создаем файлы документации
cur_path = core_path + "/doc/user_guide_en.md"
if not os.path.exists(cur_path):
  file = Path(cur_path)  
  file.touch()

# Создаем user_guide_ru файл с пользовательской документацией 
cur_path = core_path + '/doc/user_guide_ru.md'

if not os.path.exists(cur_path):
  doc_file  = open(cur_path, 'w', encoding='utf-8')
  doc_tmpl  = Template(filename='./templates/user_guide_ru.md.tpl', input_encoding='utf-8')
  doc_file.write(doc_tmpl.render(ip_cfg=ip_cfg))

# Создаем sv файл с rtl кодом ядра
cur_path = core_path + '/hw/rtl/' + ip_cfg['name'] + ".sv"

if not os.path.exists(cur_path):
  ip_sv_file  = open(cur_path, 'w', encoding='utf-8')
  ip_sv_tmpl  = Template(filename='./templates/ip.sv.tpl', input_encoding='utf-8')
  ip_sv_file.write(ip_sv_tmpl.render(ip_cfg=ip_cfg))

# Создаем fusesoc core файл 
cur_path = core_path + '/' + ip_cfg['name'] + ".core"

if not os.path.exists(cur_path):
  ip_core_file  = open(cur_path, 'w', encoding='utf-8')
  ip_core_tmpl  = Template(filename='./templates/ip.core.tpl', input_encoding='utf-8')
  ip_core_file.write(ip_core_tmpl.render(ip_cfg=ip_cfg))

   
# Создаем тестбенчи в соответствии с конфигурацией
cur_path = core_path + '/dv/cocotb/test_' + ip_cfg['name'] + ".py"

if not os.path.exists(cur_path):
  cocotb_test  = open(cur_path, 'w', encoding='utf-8')
  cocotb_test_tmpl  = Template(filename='./templates/test_ip.py.tpl', input_encoding='utf-8')
  cocotb_test.write(cocotb_test_tmpl.render(ip_cfg=ip_cfg))

# Создаем Makefile
cur_path = core_path + '/Makefile'

if not os.path.exists(cur_path):
  makefile_file  = open(cur_path, 'w', encoding='utf-8')
  makefile_tmpl  = Template(filename='./templates/Makefile.tpl', input_encoding='utf-8')
  makefile_file.write(makefile_tmpl.render(ip_cfg=ip_cfg))

# Создаем Readme
cur_path = core_path + '/README.md'

if not os.path.exists(cur_path):
  readme_file  = open(cur_path, 'w', encoding='utf-8')
  readme_tmpl  = Template(filename='./templates/Readme.md.tpl', input_encoding='utf-8')
  readme_file.write(readme_tmpl.render(ip_cfg=ip_cfg))

