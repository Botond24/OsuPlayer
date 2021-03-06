from osuparser import OsuFileParser,TimePoint
from position import PositionPlayer,PositionPlayerThread
from click import ClickPlayer,ClickPlayerThread
import win32gui
import codecs
import sys
import time
import PyHook3
import pythoncom
import os
from config import Config

config = Config()

def onKeyboardEvent(event):
	global pp,cp,config

	print("KeyID:", event.KeyID)

	if (event.KeyID == 32):
		config.dump()
		os._exit(0)
	elif (event.KeyID == 39):
		config.dict["_XB"] += 0.005
		pp.config(config)
	elif (event.KeyID == 37):
		config.dict["_XB"] -= 0.005
		pp.config(config)
	elif (event.KeyID == 38):
		config.dict["_YB"] -= 0.005
		pp.config(config)
	elif (event.KeyID == 40):
		config.dict["_YB"] += 0.005
		pp.config(config)
	# 同鼠标事件监听函数的返回值
	return True

if __name__ == "__main__":
	global pp,cp

	if (len(sys.argv) == 1):
		parser = OsuFileParser()
		print("Please Input the Osu! file!")
		parser.parse_file(input())

		handle = win32gui.FindWindow(None, "osu!")
		class_name = win32gui.GetClassName(handle)

		for t in parser.get_list():
			print([t.x,t.y,t.time,t.typ])

		pp = PositionPlayer(parser.get_list(), class_name)
		cp = ClickPlayer(parser.get_list())

		position_thread = PositionPlayerThread(pp)
		click_thread = ClickPlayerThread(cp)


		print("The Parser is finished!, Make the map selected. ")
		print(" input the maxtime(seconds) you want the engine to play for you, -1 or nothing represent the whole map")
		maxtime = -1
		try:
			maxtime = int(input())
		except Error as e:
			maxtime = -1

		print("Input a experience acording origin number, the max the number is, the early the orgin will come")
		dim_threshold = float(input())

		print("Input First Sleep Time")
		sl = float(input())


		pp.maxtime = maxtime
		cp.maxtime = maxtime
		pp.begin2()
		if (sl > 0):
			time.sleep(sl)

	elif (len(sys.argv) == 2):
		file = codecs.open(sys.argv[1])
		lines = file.readlines()
		parser = OsuFileParser()
		parser.parse_file(lines[0].strip())
		handle = win32gui.FindWindow(None, "osu!")
		class_name = win32gui.GetClassName(handle)

		for t in parser.get_list():
			print([t.x,t.y,t.time,t.typ])

		pp = PositionPlayer(parser.get_list(), class_name)
		cp = ClickPlayer(parser.get_list())

		position_thread = PositionPlayerThread(pp)
		click_thread = ClickPlayerThread(cp)
		maxtime = int(lines[1])
		dim_threshold = float(lines[2])
		sl = float(lines[3])


		pp.maxtime = maxtime
		cp.maxtime = maxtime
		pp.dim_threshold = dim_threshold
		pp.begin2()
		if (sl > 0):
			time.sleep(sl)
		else:
			pp.padding = -1000 * sl
			cp.padding = -1000 * sl

	pp.config(config)
	cp.config(config)

	hm = PyHook3.HookManager()
	hm.KeyDown = onKeyboardEvent
	hm.HookKeyboard()

	print("\n\n*****************Begin*****************\n\n")
	position_thread.start()
	click_thread.start()

	pythoncom.PumpMessages()
