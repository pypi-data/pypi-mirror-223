#!/usr/bin/env python3
import os, sys, ghclone, requests, datetime, time, queue, threading, asyncio, mystring, pause
from copy import deepcopy as dc
from threading import Lock
from fileinput import FileInput as finput
from github import Github, Repository
from contextlib import suppress
"""
.git/
- zip and split the history

./
- zip and split the history

./**/*.x
- compress x
""" 

GRepo_Saving_Progress_Lock = threading.Lock()
GRepo_FileLogging_Lock = threading.Lock()

"""
def zip_url(self, url,commit,tag):
	url_builder = self.furl + "/archive"
	if self.commit:
		url_builder += f"/{self.commit}.zip"
	elif self.tag:
		url_builder += f"/{self.tag}.zip"

	self.zip_url_base = url_builder
	return self.zip_url_base
"""

class GRepo_Pod(object):
	def __init__(self, token:str=None,num_processes:int = 10, delete_paths:bool=False):
		self.token = token
		if "GH_TOKEN" not in os.environ:
			self.login()

		self.g = Github(self.token)
		self.processor = mystring.MyThreads(num_processes)
		self.processed_paths = queue.Queue()
		setattr(self.processed_paths, 'lock', threading.Lock())

		self.current_repo_itr = None
		self.total_repo_len = None

		def appr(name:str,encodedName:str):
			with GRepo_FileLogging_Lock:
				fileName = "mapping.csv"
				if not os.path.exists(fileName):
					with open(fileName, "w+") as writer:
						writer.write("RepoITR,RepoURL,RepoSTR,RepoEncodedName\n")

				with open(fileName, "a+") as writer:
					writer.write("{0},{1}\n".format(name,encodedName))

		self.appr = appr
		self.delete_paths = delete_paths
		self.search_string = None
		self.tracking_repos = None
		asyncio.run(self.handle_history())

	@property
	def localfilename(self):
		if self.tracking_name is None:
			self.tracking_name = mystring.string("query_progress_{0}.csv".format(
				mystring.string("{query_string}".format(query_string=self.query_string)).tobase64())
			)
		return self.tracking_name

	@property
	def repos(self):
		if self.tracking_repos is None:
			self.tracking_repos = []
			if os.path.exists(self.localfilename):
				with open(self.localfilename, "r") as reader:
					for line in reader:
						ProjectItr, ProjectURL, ProjectScanned = line.split(",")
						if ProjectScanned == "false":
							self.tracking_repos.append(ProjectURL)
			else:
				self.tracking_repos = [x.clone_url for x in self.g.search_repositories(query=self.search_string)]
		self.total_repo_len = len(self.tracking_repos)
		return self.tracking_repos

	def save(self, current_project_url:str=None):
		with GRepo_Saving_Progress_Lock:
			if not os.path.exists(self.localfilename):
				with open(self.localfilename, "w+") as writer:
					writer.write("ProjectItr,ProjectURL,ProjectScanned\n")
					for proj_itr, proj in enumerate(self.repos):
						writer.write("{0},{1},false\n".format(proj_itr, proj))

			if current_project_url is not None:
				found = False
				with finput(self.localfilename, inplace=True) as reader:
					for line in reader:
						if not found and current_project_url in line:
							line = line.replace("false", "true")
						print(line, end='')
		return

	@property
	def timing(self):
		extra_rate_limiting = self.g.get_rate_limit()
		if hasattr(extra_rate_limiting, "search"):
			search_limits = getattr(extra_rate_limiting, "search")
			if search_limits.remaining < 2:
				print("Waiting until: {0}".format(search_limits.reset))
				pause.until(search_limits.reset)
	
	def repair(self,path,create:bool=True):
		if self.delete_paths and os.path.exists(path):
			os.system("yes|rm -r "+str(path))
		if create:
			os.makedirs(path, exist_ok=True)

	def __call__(self, search_string:str):
		self.timing
		self.search_string = mystring.string(search_string)

		def process_prep(repo_itr:int, repo_clone_url:str, search_string:str, appr:Callable, fin_queue:queue.Queue):
			self.query_string = search_string
			def process():
				name = mystring.string("ITR>{0}_URL>{1}_STR>{2}\n".format(
					repo_itr, repo_clone_url, search_string
				))
				name64 = str(name.tobase64())
				repo_dir = "repo_" + name64
				fileLogging = "log_" + name64 + ".csv"

				self.repair(repo_dir, create=False)
				self.repair(repo_dir)

				ghclone.clone(repo_clone_url, repo_dir)
                ##CRITICAL SECTION TO MINIMIZE/UPLOAD REPO
				util = hugg.localdrive(
					repo_dir,
					wraplambda=lambda foil:
						mystring.foil.isJava(foil)
						or mystring.foil.isScala(foil)
						or mystring.foil.isRust(foil)
						or mystring.foil.isJs(foil)
						or mystring.foil.isPython(foil)
				) #Creating this simply for utility functions, not ^/v
				for file in util.files():
					if util.dowraplambda(file):
						util.wrap(file,file)
						os.remove(file)
				util.logFiles(fileLogging)

				appr(name, name64) #mystring.string(name.replace(',',';').replace('_',',').strip()))
				fin_queue.put(repo_clone_url)

			return process

		if len(self.repos) > 0:
			for repo_itr, repo_url in enumerate(self.repos):
				self.processor += process_prep(repo_itr, repo_url, search_string, self.appr, self.processed_paths)
				self.current_repo_itr = repo_itr
		else:
			print("No Repos Found")

	def login(self):
		os.environ['GH_TOKEN'] = self.token
		with suppress(Exception):
			with open("~/.bashrc", "a+") as writer:
				writer.write("GH_TOKEN={0}".format(self.token))

	@property
	def complete(self):
		return self.total_repo_len == self.current_repo_itr and self.processor.complete

	async def handle_history(self):
		"""
		Have to run this within its own git directory
		"""
		while not self.complete:
			# Get up to 5 strings from the queue
			paths,num_waiting = [], 5
			while len(paths) < num_waiting:
				try:
					path = self.processed_paths.get()
					paths.append(path)
				except queue.Empty:
					time.sleep(10)
					num_waiting -= 1

			# Process the strings
			for path in paths:
				mystring.string("git add {0}".format(path)).exec()
			mystring.string("git commit -m \"Added multiple paths\"").exec()
			mystring.string("git push").exec()
			for path in paths:
				mystring.string("yes|rm -r {0}".format(path)).exec()

			for path in paths:
				self.save(path)
