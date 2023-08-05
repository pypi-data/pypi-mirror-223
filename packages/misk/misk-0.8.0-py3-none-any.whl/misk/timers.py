#!/usr/bin/env python3
# This file is a part of misk and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/misk/blob/master/LICENSE.txt for the full license text.
# SPDX-License-Identifier: MIT

import time
from datetime import timedelta

from . import functions as fn

__all__ = [r'ScopeTimer']



class ScopeTimer(object):

	'''
	A utility class for scoped timing blocks of code using python's "with" keyword.
	'''

	def __init__(self, description, print_start=False, print_end=print):
		self.__description = str(description)
		self.__print_start = print_start
		self.__print_end = print_end

	def __enter__(self):
		self.__start = time.perf_counter_ns()
		if self.__print_start is not None and (not isinstance(self.__print_start, bool) or self.__print_start):
			fn._log(self.__print_start, self.__description)

	def __exit__(self, type, value, traceback):
		if traceback is not None or self.__print_end is None or (
			isinstance(self.__print_end, bool) and not self.__print_end
		):
			return
		nanos = time.perf_counter_ns() - self.__start
		micros = int(nanos / 1000)
		nanos = int(nanos % 1000)
		micros = float(micros) + float(nanos) / 1000.0
		fn._log(self.__print_end, rf'{self.__description} completed in {timedelta(microseconds=micros)}.')
