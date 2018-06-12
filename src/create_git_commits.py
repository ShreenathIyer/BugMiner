"""
This module returns the git commit history for a given project
"""
import subprocess
import os
import re


class CreateGitCommitHistory(object):
    # Parsing the main header file to fetch the number of pages
    def parse_header(self, file_name):
        header_file = open("./"+file_name, 'r', encoding='utf-8')
        str_page = 0
        for line in header_file:
            if line.split(" ")[0] == "Link:":
                # str_page = re.search(r'.*?page=\.(.*?)>; rel="last"', line)
                str_page = re.findall(r'.*?page=(.*?)>; rel="last"', line.split(',')[1])
                return int(str_page[0])
        return str_page

    # Create the main header file returns the number of pages
    def get_page_count(self, project_name):
        curl_command_1 = 'curl -H "Accept: application/vnd.github.cloak-preview" ' \
                         '"https://api.github.com/search/commits?q=repo:apache/'
        curl_command_2 = '&sort=committer-date" -o commits.json -D headers.json'

        curl_command = curl_command_1 + str(project_name).lower() + "+" + str(project_name).upper() + curl_command_2
        curl_this = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = curl_this.communicate()
        return self.parse_header("headers.json")

    # Paginate the commit history based on the returned page number
    def create_commit_history(self, project_name):
        pages = self.get_page_count(project_name)

        curl_command_1 = 'curl -H "Accept: application/vnd.github.cloak-preview" ' \
                         '"https://api.github.com/search/commits?q=repo:apache/'
        curl_command_2 = '&sort=committer-date&page='
        curl_command_3 = '" -o ../resources/'
        curl_command_4 = '/commits_'
        curl_command_5 = '.json -D headers.json'

        output_dir = os.path.abspath('../resources/' + str(project_name.upper()))
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        for i in range(1, pages+1):
            print("[%s]: Generating git commit history file #%d... \n" % (project_name.upper(), i))
            curl_command = curl_command_1 + str(project_name.lower()) + "+" + str(project_name.upper()) \
                           + curl_command_2 + str(i) + curl_command_3 + str(project_name.upper()) + curl_command_4 \
                           + str(project_name.upper()) + "_" + str(i) + curl_command_5
            curl_this = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = curl_this.communicate()
        print("[%s]: Generated git commit history files" % project_name.upper())


if __name__ == "__main__":
    pass
    # obj = CreateGitCommitHistory()
    # obj.create_commit_history('SHIRO')
