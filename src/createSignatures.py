'''
Created on 15-Dec-2015

@author: Hemanth Kumar Tirupati
@ID    : cs13b027
'''

import time

from selenium import webdriver
import subprocess
import threading


ans = ""
browserDriver = "../lib/chromedriver"
threadLock = threading.Lock();
startLoad = 0

class browserThread (threading.Thread):
    def __init__(self, webpage):
        threading.Thread.__init__(self);
        self.webpage = webpage
        
    def run(self):
        global startLoad
        while 1:
            threadLock.acquire()
            if startLoad == 1:
                print "startLoad", startLoad
                threadLock.release()
                time.sleep(0.1)
                break;
            else:
                print "startLoad", startLoad
                threadLock.release()
                time.sleep(0.5)
        driver.get(self.webpage)
        driver.quit()
        threadLock.acquire()
        startLoad=0
        threadLock.release()
    
class signatureThread (threading.Thread):
    def __init__(self, website, counter, bthread):
        threading.Thread.__init__(self);
        self.website = website
        self.counter = counter
        self.bthread = bthread
        
    def run(self):
        fo = open("../data/" + self.website + str(self.counter), "w")
        pids = ""

        global startLoad
        
        threadLock.acquire()
        startLoad=1
        threadLock.release()
        
        while pids == "" or len(pids.splitlines())!=2:
            if (not self.bthread.is_alive()) and startLoad==0:
                return;
            pids = subprocess.check_output("./scanChromeProcess.sh").rstrip()
        pid = pids.splitlines()[1]
        time = 1
        anon = ""

        print pid
        global ans
        ans=""
        while 1:
            anon = subprocess.check_output(["./anonMemory.sh", pid])
            if anon == "" or anon == "0":
                break;
            ans+=str(time) + " " + anon[:len(anon) - 2] + "\n";
            #fo.write(str(time) + " " + anon[:len(anon) - 2] + "\n")
            time = time+1;
        fo.write(ans)
        fo.close()
        
with open("../data/filtered.txt", "r") as f:
    for website in f:
        webpage = "http://" + website.rstrip()
        print webpage
        for counter in range(1, 6):
            print "counter:", counter
            driver = webdriver.Chrome(browserDriver);
            bthread = browserThread(webpage)
            sthread = signatureThread(website.rstrip(), counter, bthread)
            sthread.start()
            bthread.start()
            bthread.join()
            sthread.join()
