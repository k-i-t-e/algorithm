'''
Created on Mar 15, 2013

@author: kite
'''
import algorithm
import vm_instance

#test = algorithm.ScheduldingAlgorithm()
#test.show()
#print '\n**********************\n'
#test.first_fit_descending()
#print '\n**********************\n'
#test.show()
#print '\n**********************\n'
#test.add_vm(vm_instance.VMInstance('web-server', 'vm4'))
#test.add_vm(vm_instance.VMInstance('computing', 'vm5'))
#print '\n**********************\n'
#test.show()
#print '\n**********************\n'
print 'Now testing simulated annealing'

test2 = algorithm.ScheduldingAlgorithm()
test2.hosts[0].run_vm(test2.VMs[0])
test2.hosts[1].run_vm(test2.VMs[1])
test2.hosts[2].run_vm(test2.VMs[2])
test2.show()
print '\n**********************\n'
i = test2.simulated_annealing()
print '\n**********************\n'
test2.show_hosts()
print 'made '+str(i)+' iterations'
test2.add_vm(vm_instance.VMInstance('web-server', 'vm4'))
test2.add_vm(vm_instance.VMInstance('computing', 'vm5'))

i = test2.simulated_annealing()

test2.show_hosts()
print 'made '+str(i)+' iterations'