#!/usr/bin/python
##
# Various attempts to make boto work
# and a couple of examples.
# blakegolliher
##

import boto
import boto.s3
import boto.s3.connection
from boto.s3.key import Key
import sys

def percent_cb(complete, total):
	sys.stdout.write('.')
	sys.stdout.flush()

AWS_ACCESS_KEY_ID = 'notarealkeyid'
AWS_SECRET_ACCESS_KEY = 'youshouldprovidearealaccesskey'

bucket_name = 'chewbacca'

conn = boto.connect_s3(
	aws_access_key_id = AWS_ACCESS_KEY_ID,
	aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
	host = 'chewbacca.bitstore.io',
	calling_format = boto.s3.connection.OrdinaryCallingFormat(),
	)

# to CREATE a bucket
# bucket = conn.create_bucket(bucket_name,location=boto.s3.connection.Location.DEFAULT)
bucket = conn.get_bucket(bucket_name)

testfile = 'lolfile'
print 'Uploading %s to Amazon S3 bucket %s.' % (testfile, bucket_name)

k = Key(bucket)
k.key = testfile
k.set_contents_from_filename('./lolfile', cb=percent_cb, num_cb=10)

print "\nHey that looks like it worked!  How about we list 'dem keys?"

bucket = conn.get_bucket(bucket_name)
alist = bucket.list()
for key in alist:
	print key.name

print '\nHey that looks like it worked!  How about we read back %s.' % testfile
# contents = bucket.get_key(testfile, validate=False)
contents = k.get_contents_as_string()
print "The key '%s/%s' contains the following. " % (k.bucket.name,k.name)
print contents
print "The key '%s/%s' contained the above. " % (k.bucket.name,k.name)

localfilename = 'bgolliher_testfile'
print '\nCool!  I\'ll shove that into a file called %s now.' % localfilename
k.get_contents_to_filename(localfilename)
