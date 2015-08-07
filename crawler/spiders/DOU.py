
# Author: Ricardo Dahis

# Goal: Scrape all DOU pdf files since 2007.

# Sample url: http://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?jornal=1&pagina=1&data=12/03/2007&captchafield=firistAccess

# Target Directory
dir_target = '/Users/ricardodahis/Documents/Projects/DOU/'
# delete this commentary!

# Modules
import os
import urllib2
from datetime import datetime, timedelta


def main():

	# Tolerance for errors and small
	tolerance = 2
	# Target file size limit to delete, in bytes
	target_size = 500
	
	# Dates configuration
	start = datetime(2007, 1, 1)
	end = datetime(2015, 2, 1)
	delta = timedelta(days=1)
	day = start
	weekend = set([5, 6])
	
	while day <= end:
		if day.weekday() in weekend:
			pass
		else:
			dir = dir_target+str(day.year)+"/"+str(day.month)+"/"+str(day.day)
			if not os.path.exists(dir):
				os.makedirs(dir)
			for section in range(1,4):

				counter_missing = 0
				counter_small = 0

				for page in range(1,1001): # letting it very slack
					
					# Months in url with a zero: 01, 02, etc.
					if day.month <= 9:
						month_with_zero = '0' + str(day.month)
					else:
						month_with_zero = str(day.month)

					url = 'http://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?jornal='+str(section)+'&pagina='+str(page)+'&data='+str(day.day)+'/'+month_with_zero+'/'+str(day.year)+'&captchafield=firistAccess'

					try:
						print('Downloading '+str(day.year)+'_'+str(day.month)+'_'+str(day.day)+'_'+str(section)+'_'+str(page))
						f = urllib2.urlopen(url)
						file = f.read()
						with open("/Users/ricardodahis/Documents/Project/DOU/"+str(day.year)+"/"+str(day.month)+"/"+str(day.day)+"/DOU_"+str(day.year)+'_'+str(day.month)+'_'+str(day.day)+'_'+str(section)+'_'+str(page)+'.pdf', 'wb') as code:
							code.write(file)
			
						# Pass to function
						for dirpath, dirs, files in os.walk('/Users/ricardodahis/Documents/Project/DOU/'+str(day.year)+'/'+str(day.month)+'/'+str(day.day)):
							for file in files:
								path = os.path.join(dirpath, file)
								if os.stat(path).st_size <= target_size:
									os.remove(path)
									if counter_small <= 2: #tolerance
										couter_small += 1
									else:
										break
					except Exception:
						if counter_missing <= tolerance: # tolerance
							counter_missing += 1
							print('Not available. Pass.')
							pass
						else:
							print('After '+str(tolerance+1)+' trys, quit section.')
							break
		day += delta


if __name__ == '__main__':
	main()



# TO DO
# - make it into functions
# - paralellize jobs for not wait web requests
#   - at lest each one getting one year
# - download all files without me having to specify how many there are
# - be intelligent for if internet fails, if it gets stuck for some reason# - be sure I'm not passing to new loops because a certain page doesn't exist in a section that would continue afterwards.

# Automate one download per day, or per hour (disguise robot)
#   Make dates adapt to actual date, including new ones everyday.
# How not to overload website's server? Strategies.
