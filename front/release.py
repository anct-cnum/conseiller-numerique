import subprocess
import sys
import os
from ftpretty import ftpretty
import configparser


env = sys.argv[1]

config = configparser.ConfigParser()
config.read(['ftp.cfg'])
config = config[env]

ftp_host = config['host']
ftp_user = config['user']
ftp_password = config['password']


def call(cmd):
    print('exec:', cmd)
    subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)

#call('ng build --source-map --configuration %s' % env)
call('ng build --configuration %s' % env)

with open('dist/angular-app/index.html', 'a') as f:
  git_hash = subprocess.check_output('git rev-parse HEAD', shell=True).decode('utf8').strip()
  f.write('<!-- version: {} -->'.format(git_hash))

print('FTP config:', ftp_host, ftp_user)
ftp = ftpretty(ftp_host, user=ftp_user, password=ftp_password)

print('Upload dist/ ...')
ftp.upload_tree('dist/angular-app/', '/')
print('Upload htaccess...')
ftp.put('deploy/htaccess', '/.htaccess')
print('Ok.')
