import subprocess
import sys

env = sys.argv[1]


def call(cmd):
    print('exec:', cmd)
    subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)

call('ng build --configuration %s' % env)

print('Add githash...')
with open('dist/angular-app/index.html', 'a') as f:
    git_hash = subprocess.check_output('git rev-parse HEAD', shell=True).decode('utf8').strip()
    f.write('<!-- version: {} -->'.format(git_hash))

print('Copy files...')
call('cp deploy/buildpacks dist/angular-app/.buildpacks')
call('cp deploy/servers.conf.erb dist/angular-app/servers.conf.erb')

print('Build archive...')
call('tar --transform "s/^dist\/angular-app/master/" -czvf dist/angular-app.tar.gz dist/angular-app')

print('Upload archive ...')
call('scalingo --app {env}-cnum-front deploy dist/angular-app.tar.gz'.format(env=env))
print('Ok.')
