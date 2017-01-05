import sys
import pytsk3
import datetime
import pyewf
import argparse
import hashlib
import csv
import os
import sqlite3
import re
import pandas.io.sql as sql

conn = sqlite3.connect("file.db")
cur = conn.cursor()
makequery = "CREATE TABLE FILE_INFO(FILENAME char(50),C_TIME char(50),M_TIME char(50),E_TIME char(50),EXTENSION char(50),FILESIZE char(50),LOCATION char(50)"
cur.execute("makequery")

class ewf_Img_Info(pytsk3.Img_Info):
	def __init__(self, ewf_handle):
		self._ewf_handle = ewf_handle
		super(ewf_Img_Info, self).__init__(
		url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

	def close(self):
		self._ewf_handle.close()

	def read(self, offset, size):
		self._ewf_handle.seek(offset)
		return self._ewf_handle.read(size)

	def get_size(self):
		return self._ewf_handle.get_media_size()


def directoryRecurse(directoryObject, ParentPath):
	for entryObject in directoryObject:
		if entryObject.info.name.name in [".", ".."]:
		continue
		try:
			f_type = entryObject.info.meta_type
		except:
			print "entryobject.info.name.name.",entryObject.info.name.name
			continue
		try:
			filepath = '/%s/%s' % ('/'.join(parentPath),entryObject.info.name.name)
			outputPath ='./%s/%s/' % (str(partition.addr),'/'.join(parentPath))

			if f_type == pytsk3.TSK_FS_META_TYPE_DIR:
				sub_directory = entryObject.as_directory()
				parentPath.append(entryObject.info.name.name)
				directoryRecurse(sub_directory,parentPath)
				parentPath.pop(-1)
				print "Directory: %s" % filepath
			elif f_type == pytsk3.TSK_FS_META_TYPE_REG and entryObject.info.meta.size != 0:
				searchResult = re.match(args.search,entryObject.info.name.name)
				if not searchResult:
					continue
				filedata = entryObject.read_random(0,entryObject.info.meta.size)
				print "match ",entryObject.info.name.name
				createtime = get_create_time()
				modifitime = get_modification_time()
				entrytime = get_entry_modification_time()
				eext = os.path.splittext(filename)
				exten = eext[1]
				size = get_size()
				locat = parentPath


				filequery = ""INSERT INTO FILE_INFO (FILENAME,C_TIME,M_TIME,E_TIME,EXTENSION,FILESIZE,LOCATION),values(createtime,modifitime,entrytime,exten,size,locat)"
				cur.excute(filequery)

				if args.extract == True:
					if not os.path.exists(outputPath):
						os.makedirs(outputPath)
					extractFile = open(outputPath+entryObject.info.name.name,'w')
					extractFile.write(filedata)
					extractFile.close
			elif f_type == pytsk3.TSK_FS_META_TYPE_REG and entryObject.info.meta.size == 0:


		except IOError as e:
			print e
			continue
def makequery(line)
	expression = line.split(' ')
	creation_time = expression[0]
	op1 = expression[1]
	modified_time = expression[2]
	op2 = expression[3]
	entry_time = expression[4]
	op3 = expression[5]
	extension = expression[6]
	op4 = expression[7]
	filesize = expression[8]
	op5 = expression[9]
	location = expression[10]
	selectquery = "select * from FILE_INFO WHERE C_TIME = ‘creation_time’ ‘op1’ M_time =‘modified_time’  ‘op2’ E_TIME=‘entry_time’ ‘op3’ EXTENSION = ‘extension’ ‘op4’ FILESIZE =‘filesize’ ’op5’ LOCATION = ‘location’ into outfile '~/out.csv' fields terminated by ',' enclosed by "'"'
	cur.execute("selectquery")



filenames = pyewf.glob(args.imagefile)
dirPath = args.path
if not args.search == '.*':
	print "Search Term Provided",args.search
outfile = open(args.output,'w')
outfile.write('"Inode","Full Path","Creation Time","Size","MD5 Hash","SHA1 Hash"\n')
wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
ewf_handle = pyewf.handle()
ewf_handle.open(filenames)
imagehandle = ewf_Img_Info(ewf_handle)


partitionTable = pytsk3.Volume_Info(imagehandle)
for partition in partitionTable:
	print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len
	if 'NTFS' in partition.desc:
		filesystemObject = pytsk3.FS_Info(imagehandle, offset=(partition.start*512))
		directoryObject = filesystemObject.open_dir(path=dirPath)
		print "Directory:",dirPath
		directoryRecurse(directoryObject,[])