'''
Created on Mar 12, 2013

@author: kite
'''

# import repr
import operator
# import placement_exeptions
from placement_exeptions import NoHostsLeftExeption
from vm_instance import VMInstance
from physical_host import PhysicalHost
import random
from random import seed, choice
from copy import deepcopy
import math
        

class ScheduldingAlgorithm:

    def __init__(self):
        self.VMs = []
        self.VMs.append(VMInstance('computing', 'vm1'))
        self.VMs.append(VMInstance('computing', 'vm2'))
        self.VMs.append(VMInstance('web-server', 'vm3'))
        
        self.hosts = []
        self.hosts.append(PhysicalHost('host1'))
        self.hosts.append(PhysicalHost('host2'))
        self.hosts.append(PhysicalHost('host3'))
    
    def show(self):
        for vm in self.VMs:
            vm.show_props()
        
        for host in self.hosts:
            host.show_host_props()
    
    def first_fit_descending(self):
        print 'Running FFD placement algorithm'
        # sorted_cpu = sorted(self.VMs, key = lambda vm: vm.cpu_usage)
        sorted_cpu = sorted(self.VMs, key=operator.attrgetter('cpu_usage'), reverse=True)
        sorted_mem = sorted(self.VMs, key=operator.attrgetter('mem_usage'), reverse=True)
        sorted_hdd = sorted(self.VMs, key=operator.attrgetter('hdd_usage'), reverse=True)
        
        sorted_list = [sorted_cpu, sorted_mem, sorted_hdd]
        
        
        for sort in sorted_list:
            print sort
        
        
        vm_cnt = 0  # VM counter
        host_cnt = 0  # host counter
        for sort in sorted_list:
            while vm_cnt < len(sort):
                print 'Using list ' + str(sort)
                if sort[vm_cnt].host == '':
                    while True:
                        if self.hosts[host_cnt].run_vm(sort[vm_cnt]):
                            break
                        else:
                            if host_cnt < len(self.hosts):
                                host_cnt += 1
                            else:
                                raise NoHostsLeftExeption
                                
                    vm_cnt = 0
                    break
                else:
                    vm_cnt += 1
                
    
    def first_fit(self, vm):
        print 'Running a first fit algorithm to place vm ' + vm.vm_name
        host_cnt = 0
        while host_cnt < len(self.hosts):
            if self.hosts[host_cnt].run_vm(vm):
                break
            else:
                if host_cnt < len(self.hosts):
                    host_cnt += 1
                else:
                    raise NoHostsLeftExeption
    
    def add_vm(self, vm):
        self.VMs.append(vm)
        self.first_fit(vm)
        
    def cost_func(self, hosts):
        cost = 0
        for host in hosts:
            if host.running:
                cost += 1
        return cost
    
    def simulated_annealing(self):
        k = 1.3806488 * (10**(-23))
        print 'Running Simulated Annealing algoritm'
        temp = 1000
        no_changes_iterations = 0
        old_delta = 0
        result_iter = 0
        for i in xrange(10000):
            result_iter = i
            temp_hosts = deepcopy(self.hosts)
            seed()
            host1 = choice(temp_hosts)
            seed()
            host2 = choice(temp_hosts)
            seed()
            #host1.show_host_props()
            try:
                vm = choice(host1.assigned_vms)
            except IndexError:
                continue
            host1.migrate(vm, host2)
            delta = self.cost_func(self.hosts) - self.cost_func(temp_hosts)
            if self.cost_func(self.hosts) >= self.cost_func(temp_hosts):
                self.hosts = temp_hosts
                #no_changes_iterations = 0
            else:
                if k*temp>0:
                    if math.exp(self.cost_func(self.hosts) - self.cost_func(temp_hosts)) / (k * temp) > random.random():
                        self.hosts = temp_hosts
            temp *= 0.7
            if delta == old_delta:
                no_changes_iterations += 1
            else:
                no_changes_iterations = 0 
            if no_changes_iterations>20:
                break
        return result_iter   
            

test = ScheduldingAlgorithm()
test.show()
print '\n**********************\n'
test.first_fit_descending()
print '\n**********************\n'
test.show()
print '\n**********************\n'
test.add_vm(VMInstance('web-server', 'vm4'))
test.add_vm(VMInstance('computing', 'vm5'))
print '\n**********************\n'
test.show()
print '\n**********************\n'
print 'Now testing simulated annealing'

test2 = ScheduldingAlgorithm()
test2.hosts[0].run_vm(test2.VMs[0])
test2.hosts[1].run_vm(test2.VMs[1])
test2.hosts[2].run_vm(test2.VMs[2])
test2.show()
print '\n**********************\n'
i = test2.simulated_annealing()
print '\n**********************\n'
test2.show()
print 'made '+str(i)+' iterstions'