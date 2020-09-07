import os
import traceback
import time

CGRP_CPU_LIMIT = 'RES_CPU_LIMIT'

class cpuutilisation:
    def __init__(self, cpu_limit=None):
        '''
        Initate the object for calculating cpu utilisation.
        If it fails to calculate, in any case it will return value pass
        while initiating the class or it will try to get value from env variable
        RES_CPU_LIMIT. One of them is mandatory.
        '''    
        self.cgrp_init_cycles, self.cgrp_end_cycles = 0, 0
        self.sys_init_cycles, self.sys_end_cycles = 0, 0
        self.no_of_host_cores = 0
        self.errors = []
        if cpu_limit is not None:
            self.cgrp_cpu_limit = cpu_limit
        else:
            try:
                self.cgrp_cpu_limit = os.environ[CGRP_CPU_LIMIT]
            except Exception as e:
                raise Exception('No cpu limit specified while initiating class or set in env variable {}'.format(e))
    def get_no_of_cores_host(self):
        '''
        Get total number of cores on host machine
        '''
        cpu_info = '/proc/cpuinfo'
        try:
            with open(cpu_info, 'r') as cpus:
                lscpu = cpus.readlines()
                cores = 0
                for cpu in lscpu:
                    if 'processor' in cpu: #count as  core if processor exists in line
                        cores += 1
                return int(cores)    
        except Exception as e:
            err = 'Unable to read number of Cores from System :- {}'.format(e)
            self.errors.append(err)
            # print(err)
            # traceback.print_exc()
    def get_cpu_usage_cgrp(self):
        '''
        Read the cpu cycles of cgroup, 
        '''
        file = '/sys/fs/cgroup/cpu,cpuacct/cpuacct.usage_percpu'
        try:
            with open(file, 'r') as usage_percpu:
                all_cores = usage_percpu.readlines()[0].split()
                total_cgrpcpu_cycles = 0
                for core in all_cores: total_cgrpcpu_cycles += int(core)            
                return total_cgrpcpu_cycles           
        except Exception as e:
            err = 'Exception occured while get per cpu cgrp usage :- {}'.format(e)
            self.errors.append(err)
            #print(err)
            # traceback.print_exc()
            
    def get_cpu_usage_host(self):
        '''
        Read the cpu cycles from of host.
        '''
        try:
            sys_stat = '/proc/stat'
            with open(sys_stat, 'r') as sys:
                stat = sys.readlines()[0].split() #system wide cpu usage all cores
                system_stat = 0
                for x in stat[1:]:
                    system_stat += int(x)
                return int(system_stat)
        except Exception as e:
            err = 'Exception occured duing getting system usage cycle :- {}'.format(e)
            self.errors.append(err)
            # print(err)
            # traceback.print_exc()
    def get_core_utilisation(self):
        '''
            > If it fails to calculate the usage, it return the default value defined in
              passed while initiating the class, core_utilisation else value from env variable 'RES_CPU_LIMIT'.
        Calculates the delta of cpu usage between start time & end time.
        returns the Float value. If total cores in system are 10 and it returns
        2.3 that means, function have used 2.3 cores on an average, which translates
        to around 2300m in terms, if one checks in docker stats. 
        '''
        try:
            self.no_of_host_cores = self.get_no_of_cores_host()
            cores_used = float((self.cgrp_end_cycles - self.cgrp_init_cycles)/(self.sys_end_cycles - self.sys_init_cycles) * self.no_of_host_cores * 100)/1000000000
            return None, float('{:.2f}'.format(cores_used))
        except Exception as e:
            err = 'Issue occured in cpu utilisation calculation, due to previous errors returning default maximum value set:- {}'.format(self.cgrp_cpu_limit)
            self.errors.append(err)
            # print(err)
            # print('Core utilisation Calculation error, values passed :- {}'.format(vars(cpuutilisation(self.cgrp_cpu_limit))))
            # traceback.print_exc()
            return self.errors, float(self.cgrp_cpu_limit)

    def start_time(self):
        '''
        Get the start of cgroup cycles and system cycles at point, when this function is called.
        Example Usage:
        Initate the core class, with default limit if it fails to calculate. Ex. 3
        core = cpuutilisation(3)
        Call this function before the start of function, you want to calculate cpu usage for
        core.start_time()
        actual_function_call_here_for_which_cpu_util_need_to_be_calculated()
        '''           
        self.cgrp_init_cycles = self.get_cpu_usage_cgrp()
        self.sys_init_cycles = self.get_cpu_usage_host() 

    def end_time(self):
        '''
        Get the end of cgroup cycles and system cycles at point, when this function is called.
        Example Usage:
        Call this at the end of 
        actual_function_call_here_for_which_cpu_util_need_to_be_calculated()
        core.end_time()
        Initate the core class, with default limit if it fails to calculate. Ex. 3
        core = cpuutilisation(3)
        Call this function before the start of function, you want to calculate cpu usage for
        core.start_time()
        actual_function_call_here_for_which_cpu_util_need_to_be_calculated()
        core.end_time()
        '''  

        self.cgrp_end_cycles = self.get_cpu_usage_cgrp()
        self.sys_end_cycles = self.get_cpu_usage_host() 

def main():
    core = cpuutilisation(3)
    core.start_time()
    time.sleep(3)
    #execute function here 
    core.end_time()
    errs, cores = core.get_core_utilisation()
    if errs is not None:
        for err in errs:
            print(err)
        print('\n Utilisation : ', cores)        
    else:
        print('Utilisation : ', cores)        
if __name__ == "__main__":
    main()
