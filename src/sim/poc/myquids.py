###################################################
# Liquidity Network Simulation
#
# This code provides a crude simulation for
# the liquidity network as proposed on
# www.feasta.org
# It is just a starting point to get a feeling
# of the dynamics. Later, a proper
# Agent Based Modeling approach should be adopted
#
# Please get details for the network at
# www.feasta.org
#
# Basically, the network issues free money, "quids", 
# to individuals. They spend it. Businesses get
# no quids initially, they have to earn them.
# The more active traders get rewarded by 
# getting more quids assigned. Inactive accounts
# get quids removed. Activity is measured through
# velocity: the amount of debits divided by the
# average balance over a specific period
###################################################
import random
from RingList import RingList


DEBUGLEVEL = 3

#Group some variables for the simulation
class Variables(object):
	initialquids=1000                  #initial quids allocated to individuals
	initialaccounts=3000               #how many individuals participate
	duration=30                        #duration of simulation; 1unit = 1 day
	percentSuccessfulTransactions=5    #simulates acceptance and other hindrances:
	lowerRangeTransaction=10           #every transaction gets randomly a value between
	upperRangeTransaction=100          #lowerRangeTransaction and upperRangeTransaction
	lowTransactionPerDay=0             #every individual does randomly between
	highTransactionPerDay=10           #lowTransactionPerDay and highTransactionPerDay
	percentQuidAdjustment=5            #how much Quids get added/removed when adjustments take place (end of week)
	transactionFee=0.0125              #transaction fee on every transaction (ta)
	percentNewBusiness=8               #initially, a % of ta's happen with new businesses participating
	percentNewBusinessAdjustment=2     #later, the amount of new businesses will get lower and ta's happen with already participating ones
	newBizThreshold=initialaccounts/10 #threshold when this new business % gets adjusted
	newBizThresholdStep=newBizThreshold #by how much
	higherAcceptanceThreshold=initialaccounts*10 #initially, more ta's will fail - simulating lower acceptance
	higherAcceptanceIncreaseStep=higherAcceptanceThreshold #later, more ta's will succeed - simulating better acceptance
	lowVelocityLimit=10                #the velocity limit at which accounts get quids removed
	highVelocityLimit=75               #the limit when they get added
	velocityRollingDays=90             #the interval velocity gets measured (or less if recently joined)
	percentQuidAdjustment=5            #how much gets adjusted
	maxSuccessfulTransactions=90       
		
#the first agents are the individuals
class Person(object):

	def __init__(self, name, quids):
		self.name=name
		self.quids=quids
		self.balanceHistory=RingList(90) #history of daily balances over last 90 days
		self.debitsHistory=RingList(90)  #history of daily debits over last 90 days
		self.dailyDebits=[]              #daily debits list
		self.velocity=0.0
		
	def startDayTrading(self):
		self.dailyDebits=[]             #on day trading start, the daily debits list gets reset
			
	def appendDailyDebits(self):
		self.debitsHistory.append(self.dailyDebits) #individual bought something
		
	def closeDayTrading(self):         #day ends
		self.appendDailyDebits()
		self.balanceHistory.append(self.quids)
			
	def checkLimits(self):             #not needed yet
		print "Check Limits"

	def removeQuids(self):             #velocity below limits --> quids removed
		print "removeQuids"
		toremove = self.quids*(5.0/100)
		self.quids=self.quids -toremove
		self.newBalance()
		return toremove

	def newBalance(self):              #just print balance
		if DEBUGLEVEL >= 7:
		  print "Member %s new balance: %s " %(self.name, self.quids)

	def addQuids(self):                #velocity above higher limit --> quids added
		print "addQuids"
		toadd = self.quids*(5.0/100)
		self.quids=self.quids + toadd
		self.newBalance()
		return toadd

	def check(self, buy):              #does individual have funds to buy the good?
		if DEBUGLEVEL >= 8:
			print "%s would like to buy %s for %s" %(self.name, buy.good, buy.quid)
		if (self.quids < buy.quid):
			if DEBUGLEVEL >= 8:
				print "%s does not have sufficient funds to buy %s" %(self.name,buy.good)
			return 0
		else:
			return 1
	
	def buy(self, buy):                #Yes, so do buying
		if DEBUGLEVEL >= 8:
			print "Transaction %s: %s buying %s for %s" %(buy.getID(), self.name, buy.good, buy.quid)
		self.quids=self.quids - buy.quid
		buy.setSuccessful(1)
		self.dailyDebits.append(buy.quid)
		self.newBalance()

	def sell(self,sell):               #actually crediting an account (a business)
		if DEBUGLEVEL  >= 8:
			print "Selling %s for %s" %(sell.good, sell.quid)
		self.quids=self.quids + sell.quid
		self.newBalance()
		
	def computeDailyVelocity(self):    #
		dailyvelocity = 0.0
		sum = 0.0 
		dailytransactions = len(self.dailyDebits)
		if dailytransactions == 0:
			if DEBUGLEVEL >= 7:
				print "No activity on account %s yet" %self.name
		else:
			for i in self.dailyDebits:
				sum = sum + i
			dailyvelocity = sum / dailytransactions
			if DEBUGLEVEL >= 5:
				print "%s's daily velocity: %s" %dailyvelocity
	
	def computeVelocity(self):         #at week termination, the velocity gets calculated
		balances = self.balanceHistory.get()
		days = len(balances)
		if days == 0:
			if DEBUGLEVEL >= 7:
				print "No activity on account %s yet" %self.name
				return
		velocity = 0.0
		totaldebits = self.calcTotalDebitsInPeriod()
		totaltransactionsinperiod = self.__getTotalTransactionsInPeriod__()
		if (totaltransactionsinperiod > 0):
			velocity = totaldebits / totaltransactionsinperiod
		#divide by average balance or total number of transactions?
		#averagebalance = self.calcAverageBalance()
		#if averagebalance >0:
		#	velocity = totaldebits / averagebalance
			if DEBUGLEVEL >= 3:
				print "%s's velocity over the last %s days: %s" %(self.name, days, velocity)
		return velocity
	
	def __getTotalTransactionsInPeriod__(self):
		debits = self.debitsHistory.get()
		totalTransactions = 0
		for dailyDebits in debits:
			transactions = len(dailyDebits)
			totalTransactions = totalTransactions + transactions
		return totalTransactions
					
	def getVelocity(self):
		return self.velocity
		
	def calcAverageBalance(self):
		totalbalance = 0.0
		averagebalance = 0.0
		balances = self.balanceHistory.get()
		days = len(balances)
		for i in balances:
			totalbalance = totalbalance + i	
		if days > 0:	
			averagebalance = totalbalance / days
		return averagebalance
		
	def calcTotalDebitsInPeriod(self):
		totaldebits = 0.0
		debits = self.debitsHistory.get()
			
		for day in debits:
			for transaction in day:
				totaldebits = totaldebits + transaction
		if DEBUGLEVEL >= 6:
			print "%s's total debits over the last 90 days: %s" %(self.name,totaldebits)
		return totaldebits

#the entity running the network collects the fees
class NetworkAdministration(Person):
	
	def setFee(self, vars):
		self.fee = vars.transactionFee
		
	def getFee(self):
		return self.fee
	
#govt participates in the network and gets taxes; not yet implemented
class Government(Person):
	pass

#the network itself
class LiquidityNetwork():

	def __init__(self, variables):
		self.people = dict()
		self.business = dict()
		self.variables = variables
		self.netmgr = NetworkManager(variables)
		
	def getNetworkManager(self):
		return self.netmgr
	
	def getVariables(self):
		return self.variables
		
	def startNetwork(self):
		print "Starting Liquidity Network..."
		if DEBUGLEVEL >= 7:
			print "Initial conditions: Every person gets 1000 quids."
		self.initialquids=self.variables.initialquids
		self.initialaccounts=self.variables.initialaccounts
		self.totalQuids=self.initialaccounts*self.initialquids
		if DEBUGLEVEL >= 7:
			print "Initial total Quids amount: %s" %self.totalQuids
		random.seed() # seeds the random number generator
		self.createInitialMembers()
		self.runNetwork()
		
	def runNetwork(self):
		
		sched = Schedule(self.variables);
		sched.runSchedule()
		

	def getAdministration(self):
		return self.admin
	
	def createInitialMembers(self):
		
		for i in range(0,self.initialaccounts):
    			name = "Member %s" % i 
    			person = Person(name, self.initialquids)
			self.addMember(person)
			
		self.admin=NetworkAdministration("Administration",0)
		self.admin.setFee(self.variables)
    					
	def addMember(self, person):
		if DEBUGLEVEL >= 8:
			print "Member %s joined the network." % person.name
		self.people[person.name] = person

	def getMembers(self):
		return self.people.values()
#how many quids are in the system? needed for monitoring and making decisions about limits, adjustment quantities, etc.
	def calcTotalQuids(self):
		quids=0
		members= self.people.values()
		for i in members:
			quids=quids + i.quids
		if DEBUGLEVEL >= 3:
			print "Total amount of Quids in member accounts: %s" %quids
		bizquids=0
		businesses= self.business.values()
		for i in businesses:
			bizquids= bizquids + i.quids
		adminquids = self.getAdministration().quids
		if DEBUGLEVEL >= 3:
			print "Total amount of Quids in business accounts: %s" %bizquids
			print "Total amount of Quids for administrator: %s" %adminquids
			print "Total amount of Quids in the network: %s" %(quids + bizquids + adminquids)

	def addBusiness(self, business):
		if DEBUGLEVEL >= 8:
			print "Business %s joined the network." % business.name
		self.business[business.name] = business

	def getBusinesses(self):
		return self.business.values()
	
#a step in the simulation: a day
class PlayTurn(object):

	def __init__(self,network, id):
		self.network = network
		self.variables = network.getVariables()
		self.id=id
		self.bizcount=1
		
	def startDay(self):
		print "***********************************"
		print "Day %s" %self.id
		print "***********************************"
		
		self.network.getNetworkManager().dayStartedEvent()
		members = self.network.getMembers()
		biz = self.network.getBusinesses()
		self.membersDoTransactions(members) #not very clean agent modelling :-)
		self.membersDoTransactions(biz)
		
	def membersDoTransactions(self, members):
		vars = self.network.variables
		
		for i in members:
			transactionPerDay=random.randrange(vars.lowTransactionPerDay,vars.highTransactionPerDay)
			i.startDayTrading()
			for transNum in range(0,transactionPerDay):
			  self.doTransaction(i)
			i.closeDayTrading()
			  			   	
	def doTransaction(self, member):   #an individual or a business does a transaction
		network=self.network
		vars = network.variables		 
		#assign randomly a price in the range
		price= random.randrange(vars.lowerRangeTransaction,vars.upperRangeTransaction)
		netmgr = network.getNetworkManager()
		transaction = Transaction(price,"bread", netmgr.getTransactionCount())
		#this essentially simulates acceptance and other criterias, making transactions fail or succeed
		ok = netmgr.evalShouldTransactionBeSuccessful()
		if not ok:
			if DEBUGLEVEL >= 8:
				print "Transaction %s has been rejected" %transaction.getID()
		else:		
			ok = member.check(transaction) #sufficient funds?
				
			if ok: #yes --> transaction takes place
				transaction.setSuccessful(1)
				member.buy(transaction)
				biz = self.evalWhichBusiness()
				biz.sell(transaction)
				biz.payFee(transaction,network)
				netmgr.shouldIncreaseNewBusinessRate(len(self.network.getBusinesses()))
			
		netmgr.transactionEvent(transaction)
		
	def evalWhichBusiness(self):       #should the ta take place with a new participating business or an already participating one?
		existing = self.network.getBusinesses()
		vars = self.network.getVariables()
		rate = vars.percentNewBusiness/100.0
		rnd = random.random()
		
		if rnd <= rate or len(existing) == 0: #a new business joins the network
		  name = "Business %s" %len(existing)
		  biz = Business(name, 0)
		  self.bizcount = self.bizcount + 1
		  self.network.addBusiness(biz)
		else:
			index = random.randint(0,len(existing)-1) # ta takes place with existing businesss
			biz = existing[index]
		return biz
	
	def endDay(self):
		members = self.getAllMembers()
		for i in members:
			i.computeDailyVelocity()
		
		self.network.calcTotalQuids()
		self.network.getNetworkManager().dayClosedEvent()
		print "Day %s closed" %self.id
		print "******************************"
		
	def getAllMembers(self):
		members = self.network.getMembers()
		businesses = self.network.getBusinesses()
		for biz in businesses:
			members.append(biz)
		admin = self.network.getAdministration()
		members.append(admin)
		
		return members
	
	def endOfWeek(self): #end of week: maintenance tasks
		self.network.getNetworkManager().getGlobalVelocity() #calculate global velocity for decision support
		members = self.getAllMembers()
		added,removed =0,0
		for i in members:
			velocity = i.computeVelocity() #calculate velocity for each individual
			if velocity < self.variables.lowVelocityLimit: 
				res = i.removeQuids()
				removed = removed + res
			if velocity > self.variables.highVelocityLimit:
				res = i.addQuids()
				added = added + res
		print "Removed %s quids" %removed
		print "Added %s quids" %added
	
	def doStats(self): #just some stats interesting at every day
		netmgr = self.network.getNetworkManager()
		if DEBUGLEVEL >= 3:
			print "Total number of transactions: %s" %netmgr.getTransactionCount()
			print "Total number of failed transactions: %s" %netmgr.getFailedCount()
			print "Total turnover: %s" %netmgr.getTurnover()
			print "Total number of businesses: %s" %len(self.network.getBusinesses())
		
class Transaction(object):
	
	def __init__(self, quid, good, id):
		self.quid=quid
		self.good=good
		self.successful=0
		self.id=id
		
	def setSuccessful(self,success):
		self.successful=success

	def isSuccessful(self):
		return self.successful
	def getID(self):
		return self.id
				 		
#a business is a person but only a business pays fees.
class Business(Person):
	
	def payFee(self,buy, network):
		admin = network.getAdministration()
		fee = admin.getFee()
		feeInQuids = buy.quid*fee
		transaction = Transaction(feeInQuids,"fee",buy.getID())
		self.quids = self.quids - feeInQuids
		admin.sell(transaction)

#some helper functions for the simulation
class NetworkManager(object):
	
	def __init__(self, variables):
		self.variables = variables
		self.transactionCount = 0
		self.failedCount = 0
		self.turnover = 0.0
		self.dailyTurnover = []
		self.balanceHistory = RingList(90)
		
	def getTurnover(self):
		return self.turnover
	#on every transaction
	def transactionEvent(self, transaction):
		self.transactionCount = self.transactionCount + 1
		if (not transaction.isSuccessful()):
			self.failedCount = self.failedCount + 1
		else:
			self.turnover = self.turnover + transaction.quid
			self.dailyTurnover.append(transaction.quid)
	#on every day		
	def dayStartedEvent(self):
		self.dailyTurnover = []
	#end of day	
	def dayClosedEvent(self):
		self.balanceHistory.append(self.dailyTurnover)
	#returns how many transactions in total	
	def getTransactionCount(self):
		return self.transactionCount
	#how many ta's rejected
	def getFailedCount(self):
		return self.failedCount
    #check if the threshold for failing/succeeding ta's should be changed
	def checkPercentage(self):
		tcount = self.getTransactionCount()
		vars = self.variables
		if (tcount == vars.higherAcceptanceThreshold) and (vars.percentSuccessfulTransactions <= vars.maxSuccessfulTransactions):
			vars.percentSuccessfulTransactions = vars.percentSuccessfulTransactions + 10
			vars.higherAcceptanceThreshold = vars.higherAcceptanceThreshold + vars.higherAcceptanceIncreaseStep
			print "New successful transactions percentage: %s" %vars.percentSuccessfulTransactions 
    #global velocity of the system
	def getGlobalVelocity(self):
		balances = self.balanceHistory.get()
		days = len(balances)
		balance = 0.0
		globalvelocity = 0.0
		transactions = 0
		for dailyBalance in balances:
			for transaction in dailyBalance:
				balance = balance + transaction
				transactions = transactions + 1
		if (transactions >0 ):
			if DEBUGLEVEL >= 3:
				print "Global balance: %s - Global transactions: %s" %(balance,transactions)
			globalvelocity = balance / transactions
		if DEBUGLEVEL >= 3:
			print "Global velocity over the last %s days: %s" %(days,globalvelocity)
		return globalvelocity
	#determines if a transaction will be successful or will fail (simulating acceptance, etc.)
	def evalShouldTransactionBeSuccessful(self):
		self.checkPercentage()		
		rate = self.variables.percentSuccessfulTransactions/100.0
		rnd = random.random()
		if rnd <= rate:
			successful = 1 #above success rate --> succeeds
		else:
			successful = 0 #below --> fails
			
		return successful
	#checks if the amount of ta's happening with existing businesses rather new ones should be adjusted
	def shouldIncreaseNewBusinessRate(self,existingBiz):
		if existingBiz == 0:
			return 
		
		tmp = existingBiz % vars.newBizThreshold	
		if tmp <= vars.newBizThreshold:
			if tmp==0 and vars.percentNewBusiness != 0:
				vars.percentNewBusiness = vars.percentNewBusiness - vars.percentNewBusinessAdjustment
				vars.newBizThreshold = vars.newBizThreshold + vars.newBizThresholdStep
		return
	#the scedule of the simulation
class Schedule(object):
	
	def __init__(self,vars):
		self.variables = vars
		
	def runSchedule(self):
		run = self.variables.duration
		for i in range(0,run):
			day = i+1
			turn = PlayTurn(ln, day) #play a day
			turn.startDay()
			turn.endDay()
			turn.doStats()
			
			if day%7 == 0 : #this is also end of week
				turn.endOfWeek()
    

vars = Variables()
ln = LiquidityNetwork(vars)
ln.startNetwork()



