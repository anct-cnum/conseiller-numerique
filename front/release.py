import subprocess
import sys

env = sys.argv[1]


def call(cmd):
    print('exec:', cmd)
    subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)

call('ng build --configuration %s --output-path=dist/master' % env)

print('Add githash...')
with open('dist/master/index.html', 'a') as f:
    git_hash = subprocess.check_output('git rev-parse HEAD', shell=True).decode('utf8').strip()
    f.write('<!-- version: {} -->'.format(git_hash))

print('Copy files...')
call('cp deploy/buildpacks dist/master/.buildpacks')
call('cp deploy/servers.conf.erb dist/master/servers.conf.erb')

print('Build archive...')
call('tar -C dist -czvf dist/master.tar.gz master')

print('Upload archive ...')
call('scalingo --app {env}-cnum-front deploy dist/master.tar.gz'.format(env=env))
print('Ok.')
