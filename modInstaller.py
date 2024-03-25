from pyunpack import Archive
import argparse
import shutil
import os


def ErrorExit(reason):
	print(reason)
	exit(1)


def ClearDir(dir):
	if os.path.exists(dir):
		if os.listdir(dir):
			shutil.rmtree(dir)
			os.mkdir(dir)
	else:
		os.mkdir(dir)


def CheckEnd(item, endings):
	for i in endings:
		if item.endswith(i):
			return True

	return False


def Merge(source, destination):
	for root, dirs, files in os.walk(source):
		for file in files:
			path = os.path.join(root, file)
			dest = path.replace(source, destination)
			os.makedirs(dest.replace(file, ''), exist_ok=True)
			shutil.move(path, dest)


parser = argparse.ArgumentParser(
	prog='spt mod installer',
	description="Installs mods from zip files"
)
parser.add_argument("mods", help="file fill of mods to install")
parser.add_argument("SPTFolder", help="The path to your SPT folder")
args = parser.parse_args()

if not os.path.exists(args.SPTFolder) and not os.path.exists(os.path.abspath(args.SPTFolder)):
	ErrorExit("SPT folder doesn't exist")

args.SPTFolder = os.path.abspath(args.SPTFolder)

if not os.path.exists(args.mods) and not os.path.exists(os.path.abspath(args.mods)):
	ErrorExit("file with mods doesn't exist")

args.mods = os.path.abspath(args.mods)

if len(os.listdir(args.SPTFolder)) == 0:
	ErrorExit("SPT folder is empty")

if len(os.listdir(args.mods)) == 0:
	ErrorExit("mod file is empty")

if "user" not in os.listdir(args.SPTFolder) or "BepInEx" not in os.listdir(args.SPTFolder):
	ErrorExit("SPT isn't setup correctly, or you picked the wrong folder")

n = 0
for i in os.listdir(args.mods):
	if CheckEnd(i, [".zip", ".7z", ".tar.gz", ".rar"]):
		n += 1

if n == 0:
	ErrorExit("mods folder has no zips, did you already unzip them?")

tmp = args.SPTFolder + "\\temp\\"

ClearDir(tmp)

n = 0
for i in os.listdir(args.mods):
	if CheckEnd(i, [".zip", ".7z", ".tar.gz", ".rar"]):
		path = tmp + i
		print("installing", i)
		Archive(os.path.join(args.mods, i)).extractall(tmp, patool_path="C:\\Users\\Joseph\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\patool.exe")
		os.remove(os.path.join(args.mods, i))

		# should auto merge
		if "BepInEx" in os.listdir(tmp):
			Merge(os.path.join(tmp, "BepInEx"), os.path.join(args.SPTFolder, "BepInEx"))
		elif "bepinex" in os.listdir(tmp):
			Merge(os.path.join(tmp, "bepinex"), os.path.join(args.SPTFolder, "BepInEx"))

		if "user" in os.listdir(tmp):
			Merge(os.path.join(tmp, "user"), os.path.join(args.SPTFolder, "user"))

		if "BepInEx" not in os.listdir(tmp) and "user" not in os.listdir(tmp) and "bepinex" not in os.listdir(tmp):
			for file in os.listdir(tmp):
				Merge(os.path.join(tmp, file), os.path.join(args.SPTFolder, os.path.join("user\\mods", file)))

		ClearDir(tmp)
		n += 1
	#  for mods that are only BepInEx plugins
	elif i.endswith(".dll"):
		shutil.move(os.path.join(args.mods, i), os.path.join(args.SPTFolder, "BepInEx\\plugins"))

print(f"installed {n} mods")
