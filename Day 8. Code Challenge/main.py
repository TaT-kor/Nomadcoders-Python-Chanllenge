import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

def extract_brands():
  result = requests.get(alba_url)
  soup = BeautifulSoup(result.text, "html.parser")
  brandbox = soup.find_all("li", {"class":"impact"})

  try:
    for brand in brandbox:
      info = brand.find("a", {"class":"goodsBox-info"})
      company = info.find("span", {"class":"company"}).text
      link = info["href"]
      print(f"{company} : {link}")
      extract_job(company, link)
      print("csv 저장 완료\n")
  except:
    print("----- 모든 브랜드의 스크래핑을 완료했습니다. -----")

def extract_job(company, link):
  result = requests.get(link)
  soup = BeautifulSoup(result.text, "html.parser")
  normalInfo = soup.find("div", {"id":"NormalInfo"})
  save_to_file(company, normalInfo)

def save_to_file(company, inFoForm):
  jobList = get_jobs(inFoForm)

  file = open(f"{company}.csv", mode="w", encoding = "utf-8")
  writer = csv.writer(file)
  writer.writerow(["place", "title", "time", "pay", "date"])

  for job in jobList:
    writer.writerow(list(job.values()))
  return

def get_jobs(inFoForm):
  place_list = []
  title_list = []
  timedata_list = [] 
  pay_list = []
  regDate_list =[]
  jobList = []

  places = inFoForm.find_all("td",{"class":"local first"})
  titles = inFoForm.find_all("span",{"class":"company"})
  timedatas = inFoForm.find_all("td",{"class":"data"})
  pays = inFoForm.find_all("td",{"class":"pay"})
  regDates = inFoForm.find_all("td",{"class":"regDate last"})

  for place in places:
    place_list.append(place.text)
  for title in titles:
    title_list.append(title.text)
  for timedata in timedatas:
    timedata_list.append(timedata.text)
  for pay in pays:
    pay_list.append(pay.text)
  for regDate in regDates:
    regDate_list.append(regDate.text)

  for no in range(len(place_list)):
    jobList.append({"place" : place_list[no], "title" : title_list[no], "time" : timedata_list[no], "pay" : pay_list[no], "date" : regDate_list[no]})
  return jobList

extract_brands()