import subprocess
import sys
import os


def call(cmd):
  print('exec:', cmd)
  subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)


ftp_host = os.environ['FTP_HOST']
ftp_user = os.environ['FTP_USER']
ftp_password = os.environ['FTP_PASSWORD']
env = os.environ['DJAPP_DJAPP_ENV']

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

print('build.py: Ok.')
