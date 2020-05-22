#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# 此脚本基于时间排序，仅保留最新的15个tag

import requests
requests.packages.urllib3.disable_warnings()


class CleanHarbor:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.base_url = "https://registry.youdomain.com/"
        self.login_url = self.base_url + 'login'
        self.project_url = self.base_url + 'api/projects'
        self.repo_url = self.base_url + 'api/repositories'
        self.session = requests.Session()
        self.session.verify = False
        # 此处是个坑,harbor源码auth部分的username是principal,故params参数必须是principal,否则会401
        self.session.post(self.login_url, params={"principal": self.user, "password": self.password})

    def get_project(self):
        project_info = []
        harbor_info = self.session.get(self.project_url).json()
        for project in harbor_info:
            info = {}
            info['project_id'] = project['project_id']
            info['project_name'] = project['name']
            project_info.append(info)
        return project_info

    def get_delete_repo(self):
        project_info = self.get_project()
        delete_reponame = []
        for project_id in project_info:
            repo_info = self.session.get(self.repo_url, params={"project_id": project_id['project_id']}).json()
            for repo in repo_info:
                if repo['tags_count'] > 15:
                    delete_reponame.append(repo['name'])
        return delete_reponame

    def delete_repo_tag(self):
        delete_reponame = self.get_delete_repo()
        for repo_name in delete_reponame:
            tag_url = self.repo_url + "/" + repo_name + "/tags"
            tags = self.session.get(tag_url).json()
            tags_sort = sorted(tags, key=lambda tags: tags["created"])
            del_tags = tags_sort[0:len(tags_sort) - 15]
            for tag in del_tags:
                del_repo_tag_url = tag_url + "/" + tag['name']
                result = self.session.delete(del_repo_tag_url)
                if result.status_code == 200:
                    print('{}:{} tag删除成功..'.format(repo_name, tag['name']))
        print("所有tag删除完成...")


if __name__ == "__main__":
    Harobr = CleanHarbor('admin', 'Harbor12345')
    Harobr.delete_repo_tag()