
# Author: Ricardo Dahis

# Goal: Scrape all DOU pdf files since 2007.

# Sample url: http://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?jornal=1&pagina=1&data=12/03/2007&captchafield=firistAccess

# Target Directory
dir_target = '/Users/ricardodahis/Documents/Projects/DOU/'


# Modules
import os
import urllib2




def main():

	# Tolerance for errors and small
	tolerance = 2

	# Target file size limit to delete, in bytes
	target_size = 500



	for year in range(2012, 2016):
		for month in range(1,13):
			for day in range(1,32):
				
				dir = dir_target+str(year)+"/"+str(month)+"/"+str(day)
				if not os.path.exists(dir):
					os.makedirs(dir)
				
				for section in range(1,4):

					counter_missing = 0
					counter_small = 0

					for page in range(1,1001): # letting it very slack
						
						# Months in url with a zero: 01, 02, etc.
						if month <= 9:
							month_with_zero = '0' + str(month)
						else:
							month_with_zero = str(month)

						url = 'http://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?jornal='+str(section)+'&pagina='+str(page)+'&data='+str(day)+'/'+month_with_zero+'/'+str(year)+'&captchafield=firistAccess'

						try:
							print('Downloading '+str(year)+'_'+str(month)+'_'+str(day)+'_'+str(section)+'_'+str(page))
							f = urllib2.urlopen(url)
							file = f.read()
							with open("/Users/ricardodahis/Documents/Project/DOU/"+str(year)+"/"+str(month)+"/"+str(day)+"/DOU_"+str(year)+'_'+str(month)+'_'+str(day)+'_'+str(section)+'_'+str(page)+'.pdf', 'wb') as code:
							    code.write(file)
				
							# Pass to function
							for dirpath, dirs, files in os.walk('/Users/ricardodahis/Documents/Project/DOU/'+str(year)+'/'+str(month)+'/'+str(day)):
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


if __name__ == '__main__':
	main()



# TO DO
# - adjust for different number of days in months
# - make it into functions
# - paralellize jobs for not wait web requests
#   - at lest each one getting one year
# - download all files without me having to specify how many there are
# - be intelligent for if internet fails, if it gets stuck for some reason# - be sure I'm not passing to new loops because a certain page doesn't exist in a section that would continue afterwards.

# Automate one download per day, or per hour (disguise robot)
#   Make dates adapt to actual date, including new ones everyday.
# How not to overload website's server? Strategies.

# How much of functions' parameters to pass as inputs? It will quickly have lots of inputs. Examples: tolerance, file size limit to delete.
