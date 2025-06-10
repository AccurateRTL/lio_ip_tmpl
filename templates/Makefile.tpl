# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

	
sim_veril: ./build/${ip_cfg['name']}_0/sim_verilator/coverage.dat
	cd ./build/${ip_cfg['name']}_0/sim_verilator; verilator_coverage --annotate coverage_reports ./coverage.dat; cd ../../..

./build/${ip_cfg['name']}_0/sim_verilator/coverage.dat:
	fusesoc --cores-root=.. run --target sim_verilator --no-export ${ip_cfg['name']} 

sim_icar:
	fusesoc --cores-root=.. run --target sim_iverilog  --no-export ${ip_cfg['name']} 

lint_veril: 
	fusesoc --cores-root=.. run --target lint --tool verilator --no-export ${ip_cfg['name']} 

lint_verib: 
	fusesoc --cores-root=.. run --target lint --tool veriblelint --no-export ${ip_cfg['name']} 
 
clean:
	rm -Rf ./build
	

