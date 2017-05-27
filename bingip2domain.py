# -*- coding:utf-8 -*-

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com

进行了修改 只能处理1页 将就用吧


测试：

---------------- 117.25.139.77 ----------------
1	http://www.chinaz.net
2	http://app.chinaz.com
3	http://www.wangmeng.com
4	http://space.chinaz.com


---------------- 1 IP has domains ----------------


"""

import re
import time
import urllib2
import sys

class ip2domain(object):

    @classmethod
    def get_domains(cls, ip):
        domains = set()
        url = ('https://cn.bing.com/search?q='
               'IP:%s&first=999999991&FORM=PERE' % ip)
        user_agent ='Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'  
        headers = { 'User-Agent' : user_agent }
        print url
        try:
            req = urllib2.Request(url, headers = headers )
            response = urllib2.urlopen(req)
            
            html = response.read().encode('utf-8')
            #print '\n\nhtml:\n%s\n' % html
        except Exception,e:
            print Exception,":",e
            html = ''
            #print 'null result'
        else:
            print '\n\nhtml:\n%s\n' % html
        	  #<h2><a href="http://www.wangmeng.com/" h="ID=SERP,5092.1">wangmeng.com 网盟。。。。。</a></h2>
            domain_regx = r'''<h2><a\shref="([^"]*?)"\sh="ID=[^"]*?">'''
            #[^<]*?</a></h2>'''
            # <h2><a\shref="https?://([^"]*?)"\starget="_blank"\sh="ID=[^"]*?">[^<]*?</a></h2>
            domain_list = re.findall(domain_regx, html, re.X)
            print domain_list
            # 去重
            for i in range(0, len(domain_list)):
                index = domain_list[i].find('/', 8)
        
                if -1 != index:
                    domain_list[i] = domain_list[i][0:index]
            
            domains = set(domain_list)
        
        return domains

def main():
    file = open('bing-domains.txt', 'w')
    #has domains IP num
    ipnum = 0
    
    for i in range(77, 78):
        ip = '117.25.139.%d' %i
    
        domains = ip2domain.get_domains(ip)
		    # check numbers
        if 0 == len(domains):
        		continue;
		    
        ipnum += 1
		    # write to file
        line = 1
        file.write('\n\n---------------- %s ----------------\n' %ip)
        print ip
        for domain in domains:
            file.write('%d\t%s\n' %(line, domain))
            line += 1
            print domain
        
        # 暂停1s
        time.sleep(1)

    file.write('\n\n---------------- %d IP has domains ----------------\n' %ipnum)
    file.close()

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    main()
