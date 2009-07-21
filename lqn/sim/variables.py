'''
Created on 18-lug-2009

@author: fabio
'''
#global variables for the simulation   
random_seed = 42424242
#number of LQN members which are not employees of the council
num_of_members              = 5#500
#number of council employees
num_of_employees            = 10#1000
 #initial quids amount per member account            
initial_quids_per_account   = 100
#initial quids for businesses
initial_quids_per_business  = 1000
#quid injection for businesses period, in months:
#for this amount of months, business accounts will get
#quid injections in the amount of increase_step_businesses per month
quid_injection_business_period = 10
#increase_step_for_businesses, in quids
increase_step_for_businesses = 1000
#
#increase step, in quids
#increase_step               = 20
#number of businesses in the scheme
num_of_businesses           = 300
#final total quids amount, not used for now            
final_total_quids           = 100000
#sponsorship factor         
sponsorship_factor          = 10000
#monthly expenditures of members(citizens) for the council
#includes water, refuse, and car. 
#Monthly "flat rate assumed per member, in quids
monthly_expenditures        = 70
#every transaction gets randomly a value between
#lower_range_transaction and upper_range_transaction                
lower_range_transaction     = 10            
upper_range_transaction     = 100
               