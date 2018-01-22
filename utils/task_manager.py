#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 9/Jan/17 11:05
Description:

Arrange tasks based on the priorities.

Based on its priority, task can be a

"""
from utils import Logger

class TaskManager(object):
	def __init__(self):
		self.name = 'TaskManager'
		self.logger = Logger(self.name)

		self.tasks = []
		self.priorities = []

	def add_task(self, task):
		curr_highest_priority = max(self.priorities) if self.priorities else 0

		if task.priority < curr_highest_priority:
			self.logger.warning((task.name, 'Request refused. Higher priority task is running.'))
			return False

		elif task.priority == curr_highest_priority:
			self.logger.info((task.name,
												'Task is created successfully. Same priority task is running. Adding to the task list'))
			self.tasks.append(task)
			self.priorities.append(task.priority)

		elif task.priority > curr_highest_priority:
			if self.tasks or self.priorities:
				self.logger.warning((task.name, 'is created successfully. Other tasks are discarded.'))
				self.tasks.clear()
				self.priorities.clear()

			self.tasks.append(task)
			self.priorities.append(task.priority)

	def clean_tasks(self):
		"""
		:brief: remove timeout and completed task from task list
		:return:
		"""
		for task in list(self.tasks):
			to_remove = False
			if task.state == task.states['end']:
				self.logger.info((task.name, 'is done.'))
				to_remove = True

			if task.is_current_task_timeout():
				self.logger.error('Task ' + task.name + ' timeout...')
				to_remove = True

			if to_remove:
				self.tasks.remove(task)
				self.priorities.remove(task.priority)

	def run_tasks(self):
		self.clean_tasks()

		for task in self.tasks:
			self.logger.debug(('current task: ', task.name,
												 'current state: ', task.state.name))

			task.run()
