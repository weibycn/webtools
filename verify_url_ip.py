# -*- coding:utf-8 -*-

# �����վ��Ӧ����ʵIP
# �������ܶ���վͨ��CDN���з���������֪����ʵIP��
# 	ͨ������;���õ����IP�󣬼���Ƿ�Ϊ��ʵIP
# ����1�������http��ֱ��IP��port������get�������ڴ���https
# ����2��ʹ��urllib2��ͨ���鿴urllib2��Դ���룬���ֿ���ʵ�֡�
# 	urlͨ��ip���죬����ͷ������Host��http��https������ʵ�֡�
# 	��https://res.fawan.com/20/ynetLogo.png����ӦIPΪ42.81.28.122
# 	urllib2�򿪵�urlΪhttps://42.81.28.122/20/ynetLogo.png
# 
# Ԥ���˶��̲߳��Ժ���������ʵ�ֲ��м�⡣���amazon�Ƶ�IP�ν��м�⡣
# amazon�Ƶ�IP���ڹ����������ص�


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
		# ���幦����
		print "START " + str + '\n'
		time.sleep(2)
	finally:
		# ִ����� ��С����
		print "END " + str + '\n'
		SEMAPHORE.release()
    


def multi_thread():
	# �����߳�������
	global SEMAPHORE
	num_threads = 3
	SEMAPHORE = threading.Semaphore(num_threads)
	
	for i in range(10):
		# �����߳�ǰ������߳����Ƿ��Ѵ����ޣ����Ӽ���
		# ���Լ����жϺ��������磺����ҵ���ʵIP���˳�ѭ��
		SEMAPHORE.acquire()
		t = threading.Thread(target=test_thread, args=(str(i)))
		t.start()


# ͨ��urllib2 �����վ��ʵIP
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
	#����ͷ����Host��
	headers = { 'User-Agent' : user_agent, 'Host' : host }
	#print headers
	
	try:
		req = urllib2.Request(url, headers = headers )
		response = urllib2.urlopen(req)
		res_code = response.getcode()
		if res_code == 200:
			#�ҵ���ʵIP
			print url + '\t' + host + '\t200 OK'
		elif res_code == 404:
			print url + '\t' + host + '\t404 not found'
		else:
			print url + '\t' + host + '\t' + str(res_code)
	except urllib2.HTTPError, e:
		print e.code
		print url + '\t' + host + '\tnot found'
		sys.exit(1)
		    
	

# ͨ��tcpֱ��IP���ж���ʵIP
# https://res.fawan.com/20/ynetLogo.png		42.81.28.122
#             host        url                 ip   
def test_tcp(ip, port = 80, host = '', url = '/'):
	
	# get��������
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
		# ����socket����
		s=socket(AF_INET,SOCK_STREAM,0)
		#��������
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
			#�ҵ���ʵIP
			print '%s %s 200 OK'%(ip, url)
		elif res_code[0] == '404':
			print '%s %s 404 not found'%(ip, url)
		else:
			print res_code[0]
		
		#�ر�Socket
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

	