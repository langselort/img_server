# -*- coding: UTF-8 -*-
import os
import ConfigParser
import time

from qiniu import Auth,put_file, etag


class ImgCls(object):
# TODO 日志处理
	def __init__(self):
		"""
		读取配置文件初始化
		"""
		top_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + '..')
		self.conf = ConfigParser.ConfigParser()
		self.conf.read(top_path + '/conf.ini')
		# key
		self.access_key = self.conf.get('img_bed','Access_Key')
		self.secret_key = self.conf.get('img_bed','Secret_Key')
		self.bucket_name = self.conf.get('img_bed','Bucket_Name')
		self.outside_chain = self.conf.get('img_bed','Outside_Chain')
		self.qny_auth = Auth(self.access_key, self.secret_key)
		
		# TODO session 登录
		
	
	def upload_img(self,img_file):
		
		img_url = None
		# 获取当前时间
		time_now = int(time.time())
		# 转换成localtime
		time_local = time.localtime(time_now)
		# 转换成新的时间格式(2016-05-09 18:59:20)
		ts = time.strftime("%Y%m%d%H%M%S", time_local)
		#要上传的空间
		bucket_name = self.bucket_name
		#上传到七牛后保存的文件名
		key = ts + '.png'
		#生成上传 Token，可以指定过期时间等
		token = self.qny_auth.upload_token(bucket_name, key, 3600)
		#要上传文件的本地路径
		local_file = img_file
		try:
			ret, info = put_file(token, key, local_file)
			# print(info)
			assert ret['key'] == key
			assert ret['hash'] == etag(local_file)
			img_url = self.outside_chain + '/' + key
		except Exception as e:
			print e
		return img_url

if __name__ == '__main__':
	img_cls = ImgCls()
	img_url = img_cls.upload_img('1.jpg')
	print(img_url)