# -*- coding:utf-8 -*-

# 检测网站对应的真实IP
# 背景：很多网站通过CDN进行防护，难以知道真实IP，
# 	通过其他途径拿到多个IP后，检测是否为真实IP
# 方法1：如果是http，直连IP和port，发送get请求。难于处理https
# 方法2：使用urllib2，通过查看urllib2的源代码，发现可以实现。
# 	url通过ip构造，请求头中增加Host域。http和https都可以实现。
# 	如https://res.fawan.com/20/ynetLogo.png，对应IP为42.81.28.122
# 	urllib2打开的url为https://42.81.28.122/20/ynetLogo.png
# 
# 预留了多线程测试函数，可以实现并行检测。如对amazon云的IP段进行检测。
# amazon云的IP段在官网可以下载到


import urllib2
import sys
import re
from socket import *
import threading
import time


# Max Thread Num
#SEMAPHORE = threading.Semaphore(3)
SEMAPHORE = None

def test_thread(str):
	global SEMAPHORE
	
	try:
		# 具体功能区
		print "START " + str + '\n'
		time.sleep(2)
	finally:
		# 执行完毕 减小计数
		print "END " + str + '\n'
		SEMAPHORE.release()
    


def multi_thread():
	# 设置线程数上限
	global SEMAPHORE
	num_threads = 3
	SEMAPHORE = threading.Semaphore(num_threads)
	
	for i in range(10):
		# 创建线程前，检测线程数是否已达上限，增加计数
		# 可以加入判断函数，例如：如果找到真实IP，退出循环
		SEMAPHORE.acquire()
		t = threading.Thread(target=test_thread, args=(str(i)))
		t.start()


# 通过urllib2 检测网站真实IP
# https://res.fawan.com/20/ynetLogo.png		42.81.28.122
# schema      Host        url                 ip     

def test_ip_url(schema='http', ip='', port=80, host='', url=''):
	# url = schema://ip:port/url
	if port == 80 or port == 443:
		url = '%s://%s/%s' %(schema, ip, url)
	else:
		url = '%s://%s:%d/%s' %(schema, ip, port, url)
	print url
	
	
	user_agent ='Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'  
	#请求头增加Host域
	headers = { 'User-Agent' : user_agent, 'Host' : host }
	#print headers
	
	try:
		req = urllib2.Request(url, headers = headers )
		response = urllib2.urlopen(req)
		res_code = response.getcode()
		if res_code == 200:
			#找到真实IP
			print url + '\t' + host + '\t200 OK'
		elif res_code == 404:
			print url + '\t' + host + '\t404 not found'
		else:
			print url + '\t' + host + '\t' + str(res_code)
	except urllib2.HTTPError, e:
		print e.code
		print url + '\t' + host + '\tnot found'
		sys.exit(1)
		    
	

# 通过tcp直连IP，判断真实IP
# https://res.fawan.com/20/ynetLogo.png		42.81.28.122
#             host        url                 ip   
def test_tcp(ip, port = 80, host = '', url = '/'):
	
	# get请求内容
	get_data = '''GET %s HTTP/1.1
Host: %s
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
Accept-Encoding: gzip, deflate, sdch
Accept-Language: zh-CN,zh;q=0.8
Connection: close

'''%(url, host)

	# print get_data

	try:
		# 建立socket对象
		s=socket(AF_INET,SOCK_STREAM,0)
		#建立连接
		s.connect((ip, port))
		#print "Request:\r\n%s\r\n"%get_data
		s.send(get_data)
		sresult=s.recv(1024)
		
		#print "Response:\r\n%s\r\n" %sresult
		
		re_code = re.compile(r'HTTP/1.1 (.*?) ')
		res_code = re_code.findall(sresult)
	
		if len(res_code) < 1:
			print '%s %s error to get url'%(ip, url)
		elif res_code[0] == '200':
			#找到真实IP
			print '%s %s 200 OK'%(ip, url)
		elif res_code[0] == '404':
			print '%s %s 404 not found'%(ip, url)
		else:
			print res_code[0]
		
		#关闭Socket
		s.close()
	except Exception,ex:
		print 'exception:error to connect' 
		print ex

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	
	# https://res.fawan.com/20/ynetLogo.png
	# https://42.81.28.122/20/ynetLogo.png
	#test_tcp(ip = '42.81.28.122', port = 80, url = '/20/ynetLogo.png')
	test_ip_url('https', ip = '42.81.28.122', port = 443, host = 'res.fawan.com', url = '20/ynetLogo.png')

	