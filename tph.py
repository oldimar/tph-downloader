#!/usr/bin/python3

#This script needs the tool 'wget' to run

import http.client as web
import re
import subprocess as sp

def get_issues_by_year(year):
  re_issue = re.compile("data-cover-issue-url=\"/content/(\d+-?\d*)/(\d+-?\d*)\"")
  site="tph.ucpress.edu"
  url="/content/by/year/{}".format(year)
  conn = web.HTTPConnection(site)
  conn.request("GET",url)
  r = conn.getresponse()
  body = r.read().decode("utf8")
  return re_issue.findall(body)

def get_chapters_by_issue(a,b):
  #re_chapter = re.compile("href=\"(/content/{}/{}/\d+-?\d*)\"".format(a,b))
  re_chapter = re.compile("data-apath=\"/ucptph/{}/{}/(\d+\.?\d*)\.atom\"".format(a,b))
  site="tph.ucpress.edu"
  url="/content/{}/{}".format(a,b)
  conn = web.HTTPConnection(site)
  conn.request("GET",url)
  r = conn.getresponse()
  body = r.read().decode("utf8")
  return list(set([ "http://tph.ucpress.edu/content/{}/{}/{}.full.pdf".format(a,b,x) for x in re_chapter.findall(body)]))

def authenticate(user,passwd):
  re_form_id=re.compile("name=\"form_build_id\" +value=\"([^\"]+)\" />\n<input type=\"hidden\" name=\"form_id\" value=\"highwire_user_login\" />",re.S)
  site="tph.ucpress.edu"
  url="/user/login"
  conn = web.HTTPConnection(site)
  conn.request("GET",url)
  r = conn.getresponse()
  body = r.read().decode("utf8")
  form_id = re_form_id.findall(body)[0]
  sp.run(["wget","--save-cookies", "/tmp/tph.cookies.txt",
          "--keep-session-cookies", "--post-data",
          "name={}&pass={}&form_build_id={}&form_id=highwire_user_login".format(user,passwd,form_id),
          "--delete-after", "http://tph.ucpress.edu/user/login"])

def get_chapters(chapters):
  with open("/tmp/tph.log","a") as outfile:
      cmd = ["wget", "-nc", "-x", "--load-cookies", "/tmp/tph.cookies.txt" ]
      cmd.extend(chapters)
      sp.run(cmd,stdout=outfile, stderr=outfile)

user=input("Entre o nome do usuario: ")
passwd=input("Entre o password: ")
authenticate(user,passwd)
for year in range(1978,2018):
    issues = get_issues_by_year(year)
    for a,b in issues:
        print("Getting issue {},{},{}".format(year,a,b))
        get_chapters(get_chapters_by_issue(a,b))
