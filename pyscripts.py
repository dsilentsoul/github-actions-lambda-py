import sys
import subprocess
import re
import os

#aws-access-key-id= sys.argv[1]
#aws-secret-access-key= sys.argv[2]
#aws-region= sys.argv[3]

git_diff='git diff --name-status HEAD^'
diff=subprocess.run(git_diff.split(),capture_output=True,text=True)
#diff1= diff.split('\n')
#diff2=[x.split('\t') for x in diff1]
l = [x.split('\t') for x in diff.stdout.split('\n')]
pwd= subprocess.run(['pwd'],capture_output=True,text=True)
print(l)
print(pwd)
for i in l:
    if i[0]=='A' and re.search("^src/.*.py$", i[1]):
        #print(os.path.basename(i[1])[:-3])
        full_path=os.path.basename(i[1])
        zip_file= f'zip deploy.zip {i[1]}'
        subprocess.run(zip_file.split())
        function_name=os.path.splitext(full_path)[0]
        create_command= f'aws lambda create-function --function-name {function_name} --role arn:aws:iam::892244660070:role/github-actions-lambda-py --runtime python3.7 --handler {function_name}.{function_name} --zip-file fileb://deploy.zip'
        subprocess.run(create_command.split())
