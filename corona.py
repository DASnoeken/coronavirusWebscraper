from selenium import webdriver
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import csv

path = r'/home/dsnoeken/geck/geckodriver'   		#put your own path here, to the geckodriver
browser = webdriver.Firefox(executable_path=path)	#Make sure you have firefox
url = 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6'
browser.get(url)

time.sleep(5)
numbers = browser.find_elements_by_xpath("//div[@class='widget flex-vertical full-height indicator-widget ember-view']")  	#//div[@id='ember25']" id's kept changing daily so I try it via class name
#NO_Dead = browser.find_elements_by_xpath("//div[@class='widget flex-vertical full-height indicator-widget ember-view']")		#//div[@id='ember63']
#NO_Recovered = browser.find_elements_by_xpath("//div[@class='widget flex-vertical full-height indicator-widget ember-view']")	#//div[@id='ember77']
no_inf = str(numbers[0].text).split('\n')
no_dead = str(numbers[2].text).split('\n')
no_recov = str(numbers[3].text).split('\n')
print(no_inf)
print(no_dead)
print(no_recov)
print(str(datetime.datetime.now()))
if ',' in no_inf[1]:
	no_inf[1] = no_inf[1].replace(',','')
if ',' in no_dead[1]:
	no_dead[1] = no_dead[1].replace(',','')
if ',' in no_recov[1]:
	no_recov[1] = no_recov[1].replace(',','')
print(no_inf[0]+" = "+no_inf[1]+'\n')
print(no_dead[0]+" = "+no_dead[1]+'\n')
print(no_recov[0] + " = " + no_recov[1]+'\n')

try:
    el = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,'esri.Map_0_gc')))
except TimeoutException:
    print("loading took too much time")
time.sleep(1)
screenshot = browser.save_screenshot("Corona_"+str(datetime.datetime.now())+".png")

browser.quit()

with open('infected.csv','a',newline='') as csvfile:
	writer_inf = csv.writer(csvfile,delimiter=',')
	writer_inf.writerow([str(datetime.datetime.now()),str(no_inf[1])])
with open('dead.csv','a',newline='') as csvfile:
	writer_inf = csv.writer(csvfile,delimiter=',')
	writer_inf.writerow([str(datetime.datetime.now()),str(no_dead[1])])
with open('recovered.csv','a',newline='') as csvfile:
	writer_inf = csv.writer(csvfile,delimiter=',')
	writer_inf.writerow([str(datetime.datetime.now()),str(no_recov[1])])
	
cfr = int(no_dead[1])/(int(no_dead[1])+int(no_recov[1]))
print('CFR = '+str(cfr))
with open('cfr.csv','a',newline='') as csvfile:
    writer_cfr = csv.writer(csvfile,delimiter=',')
    writer_cfr.writerow([str(datetime.datetime.now()),str(cfr)])
