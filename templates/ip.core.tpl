CAPI=2:
# Copyright AccurateRTL contributors.
# Licensed under the MIT License, see LICENSE for details.
# SPDX-License-Identifier: MIT

name: '::${ip_cfg['name']}:'

filesets:
  files_rtl:
    file_type: systemVerilogSource
    files:
    - hw/rtl/${ip_cfg['name']}.sv

  files_cocotb:
    files:
      - dv/cocotb/test_${ip_cfg['name']}.py
    file_type: user

scripts:
  set_python_path: 
    cmd: [$(eval export PYTHONPATH = $(shell pwd)/../../../dv/cocotb:$PYTHONPATH)]
 
  create_dump_file: 
    cmd: ['printf "module iverilog_dump();\n initial begin \n \$$dumpfile(\"dump.fst\");\n    \$$dumpvars(0 , lio_axil_regs_if);\n end\n endmodule" > iverilog_dump.v']

  copy_tb: 
    cmd: ['cp ../../../dv/cocotb/test_${ip_cfg['name']}.py ./test_${ip_cfg['name']}.py']
    
  create_coverage_data: 
    cmd: ['verilator_coverage --annotate coverage_reports ./coverage.dat']


targets:
  default: &default_target
    filesets:
    - files_rtl
    toplevel: ${ip_cfg['name']}

  simulation:
    filesets:
    - files_rtl

  sim_iverilog:
    toplevel: ${ip_cfg['name']}
    hooks:
      pre_build: [copy_tb, create_dump_file]
    filesets: [files_rtl, files_cocotb]
    flow: sim
    flow_options:
        tool: icarus
        cocotb_module: test_${ip_cfg['name']}
        iverilog_options:
          - -g2012 -siverilog_dump iverilog_dump.v
        timescale: 1ns/1ns    
        
  sim_verilator:
    toplevel: ${ip_cfg['name']}
    hooks:
      pre_build: [copy_tb]
      post_run:  [create_coverage_data]
    filesets: [files_rtl, files_cocotb]
    flow: sim
    flow_options:
        tool: verilator
        cocotb_module: test_${ip_cfg['name']}      
        verilator_options: ['--coverage', "--trace", "--trace-fst", "--trace-structs"]  
        run_options: ["--trace"]

  lint:
    <<: *default_target
    default_tool: verilator
    tools:
      verilator:
        mode: lint-only
        verilator_options:
          - "-Wall"
      veriblelint:
        rules:
          - "-no-trailing-spaces"
