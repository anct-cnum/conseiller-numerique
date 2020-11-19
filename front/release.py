import subprocess
import sys
import os
from ftpretty import ftpretty
import configparser


env = sys.argv[1]

config = configparser.ConfigParser()
config.read(['release.cfg'])
config = config[env]

ftp_host = config['ftp_host']
ftp_user = config['ftp_user']
ftp_password = config['ftp_password']


def call(cmd):
    print('exec:', cmd)
    subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)

#call('ng build --source-map --configuration %s' % env)
call('ng build --configuration %s' % env)

with open('dist/angular-app/index.html', 'a') as f:
    git_hash = subprocess.check_output('git rev-parse HEAD', shell=True).decode('utf8').strip()
    f.write('<!-- version: {} -->'.format(git_hash))

with open('deploy/htaccess', 'r') as fr, open('dist/angular-app/.htaccess', 'w') as fw:
    content = fr.read()
    prefix = '' if env == 'prd' else (env + '-')
    host = '{prefix}app.{host}'.format(prefix=prefix, host=config['host'])
    host_escaped = host.replace('.', '\\.')
    content = content.replace('{{HOST}}', host)
    content = content.replace('{{HOST_ESCAPED}}', host_escaped)
    fw.write(content)

print('FTP config:', ftp_host, ftp_user)
ftp = ftpretty(ftp_host, user=ftp_user, password=ftp_password)

print('Upload dist/ ...')
ftp.upload_tree('dist/angular-app/', '/')
print('Ok.')
