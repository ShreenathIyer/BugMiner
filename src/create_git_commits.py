import subprocess
import os


class CreateGitCommitHistory(object):
    def create_commit_history(self, project_name):
        curl_command_1 = 'curl -H "Accept: application/vnd.github.cloak-preview" ' \
                         '"https://api.github.com/search/commits?q=repo:apache/'
        curl_command_2 = '&sort=committer-date&page='
        curl_command_3 = '" -o ../resources/'
        curl_command_4 = '/commits_'
        curl_command_5 = '.json -i -D headers.json'

        output_dir = os.path.abspath('../resources/' + str(project_name.upper()))
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        for i in range(1, 21):
            curl_command = curl_command_1 + str(project_name.lower()) + "+" + str(project_name.upper()) \
                           + curl_command_2 + str(i) + curl_command_3 + str(project_name.upper()) + curl_command_4 \
                           + str(project_name.upper()) + "_" + str(i) + curl_command_5
            curl_this = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = curl_this.communicate()
        # print(err)


if __name__ == "__main__":
    obj = CreateGitCommitHistory()
    obj.create_commit_history('SHIRO')
    # pass
    # curl_command_1 = 'curl -H "Accept: application/vnd.github.cloak-preview" "https://api.github.com/search/commits?q=repo:apache/shiro+SHIRO&sort=committer-date" -o commits.json -D headers.json'
