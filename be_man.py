import sys, os, time

argv = sys.argv
host_name = argv[1]
num = argv[2] if len(argv)>2 else 1
proxy = argv[3] if len(argv)>3 else ''
while True:
    os.system('scrapy crawl be -a host_name=%s -a num=%s -a proxy=%s' % (host_name, num, proxy))
    time.sleep(8)