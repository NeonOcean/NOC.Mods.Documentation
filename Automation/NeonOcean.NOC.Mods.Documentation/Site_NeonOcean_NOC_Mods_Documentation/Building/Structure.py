import json
import numbers
import os
import typing

from Site_NeonOcean_NOC_Mods_Documentation import Paths
from Site_NeonOcean_NOC_Mods_Documentation.Tools import IO

class _StructureEntry:
	def __init__ (self, identifier: str):
		self.Identifier = identifier  # type: str
		self.Entries = list()  # type: typing.List[_StructureEntry]
		self.HasValues = False  # type: bool

		self.DocumentPath = None  # type: typing.Optional[str]
		self.Invisible = True  # type: bool
		self.StartOpened = False  # type: bool
		self.Name = None  # type: typing.Optional[str]
		self.Link = False  # type: bool
		self.Priority = 0  # type: numbers.Number

	def SetValues (self, documentPath: str, invisible: bool, startOpened: bool, name: str, link: bool, priority: numbers.Number):
		self.DocumentPath = documentPath
		self.Invisible = invisible
		self.StartOpened = startOpened
		self.Name = name
		self.Link = link
		self.Priority = priority

		self.HasValues = True

	def __str__ (self):
		entriesText = ""  # type: str

		for entry in self.Entries:  # type: _StructureEntry
			entryText = str(entry)

			if entryText == "":
				continue

			if entriesText == "":
				entriesText += entryText
			else:
				entriesText += ",\n" + entryText

		if not self.HasValues or self.Invisible:
			return entriesText
		else:
			structureText = "{"  # type: str

			structureText += "\n\t\"Name\": \"" + self.Name + "\""

			if self.Link:
				structureText += ",\n\t\"Path\": \"" + self.DocumentPath + "\""

			structureText += ",\n\t\"StartOpened\": " + str(self.StartOpened).lower()

			if entriesText != "":
				entriesText = "\t" + entriesText
				structureText += ",\n\t\"Entries\": [\n\t" + entriesText.replace("\n", "\n\t\t") + "\n\t]"

			structureText += "\n}"

			return structureText

def BuildStructure () -> bool:
	IO.ClearDirectory(Paths.StructureBuildPath)

	_BuildStructure()
	return True

def _BuildStructure () -> None:
	structureConfigs = list()  # type: typing.List[dict]

	rootStructureConfigFilePath = os.path.join(Paths.StructureSourcePath, "index.json")  # type: str

	if os.path.exists(rootStructureConfigFilePath):
		with open(rootStructureConfigFilePath) as rootStructureConfigFile:
			rootStructureConfig = json.JSONDecoder().decode(rootStructureConfigFile.read())
	else:
		rootStructureConfig = {
			"DocumentPath": "index.html",
			"EntryPath": "ROOT",
			"Invisible": True,
			"StartOpened": True,
			"Name": "",
			"Link": False,
			"Priority": 0
		}

	for directoryRoot, directoryNames, fileNames in os.walk(Paths.StructureSourcePath):  # type: str, typing.List[str], typing.List[str]
		for fileName in fileNames:  # type: str
			if os.path.splitext(fileName)[1] == ".json":
				structureConfigFilePath = os.path.join(directoryRoot, fileName)  # type: str

				try:
					structureConfig = _ReadStructureConfig(structureConfigFilePath)  # type: dict
				except Exception as e:
					raise Exception("Failed to read structure config from '" + structureConfigFilePath + "'.") from e

				if not (directoryRoot == Paths.StructureSourcePath and os.path.splitext(fileName)[0] == "index"):
					structureConfigs.append(structureConfig)

	structureDirectory = os.path.join(Paths.StructureBuildPath, "indexing")  # type: str
	structureFilePath = os.path.join(structureDirectory, "structure_indexing.js")  # type: str

	if not os.path.exists(structureDirectory):
		os.makedirs(structureDirectory)

	with open(structureFilePath, "w+") as structureFile:
		structureFile.write(_ReadStructure(rootStructureConfig, structureConfigs))

def _ReadStructureConfig (structureConfigFilePath: str) -> typing.Dict[str, typing.Any]:
	with open(structureConfigFilePath) as structureConfigFile:
		structureConfig = json.JSONDecoder().decode(structureConfigFile.read())  # type: dict

	structureFileExtension = structureConfig["FileExtension"]  # type: str

	documentRelativeFilePath = os.path.splitext(structureConfigFilePath.replace(Paths.StructureSourcePath + os.path.sep, ""))[0] + "." + structureFileExtension  # type: str
	documentRelativeFilePath = documentRelativeFilePath.replace("\\", "/")

	structureConfig["DocumentPath"] = documentRelativeFilePath

	if os.path.splitext(os.path.split(documentRelativeFilePath)[1])[0] == "index":
		structureConfig["EntryPath"] = os.path.split(documentRelativeFilePath)[0]
	else:
		structureConfig["EntryPath"] = os.path.splitext(documentRelativeFilePath)[0]

	return structureConfig

def _ReadStructure (rootStructureConfig: dict, structureConfigs: typing.List[dict]) -> str:
	rootStructureDocumentPath = rootStructureConfig.get("DocumentPath")  # type: str
	rootStructureInvisible = rootStructureConfig["Invisible"]  # type: bool
	rootStructureStartOpened = rootStructureConfig["StartOpened"]  # type: bool
	rootStructureName = rootStructureConfig["Name"]  # type: str
	rootStructureLink = rootStructureConfig["Link"]  # type: bool
	rootStructurePriority = rootStructureConfig["Priority"]  # type: numbers.Number

	rootStructure = _StructureEntry("ROOT")  # type: _StructureEntry
	rootStructure.SetValues(rootStructureDocumentPath, rootStructureInvisible, rootStructureStartOpened, rootStructureName, rootStructureLink, rootStructurePriority)

	for structureConfig in structureConfigs:  # type: dict
		structureEntryPath = structureConfig["EntryPath"]  # type: str

		structureDocumentPath = structureConfig["DocumentPath"]  # type: str
		structureInvisible = structureConfig["Invisible"]  # type: bool
		structureStartOpened = structureConfig["StartOpened"]  # type: bool
		structureName = structureConfig["Name"]  # type: str
		structureLink = structureConfig["Link"]  # type: bool
		structurePriority = structureConfig["Priority"]  # type: numbers.Number

		currentStructure = _CreateStructureEntry(rootStructure,
												 structureEntryPath)  # type: _StructureEntry

		currentStructure.SetValues(structureDocumentPath, structureInvisible, structureStartOpened, structureName, structureLink, structurePriority)

	_SortStructure(rootStructure)

	structureTextPrefix = "var StructureIndexing = [\n"  # type: str
	structureText = "\t" + str(rootStructure).replace("\n", "\n\t")  # type: str
	structureTextSuffix = "\n]"  # type: str

	return structureTextPrefix + structureText + structureTextSuffix

def _CreateStructureEntry (root: _StructureEntry, entryPath: str) -> _StructureEntry:
	entryPath = entryPath.replace(os.path.altsep, os.path.sep)
	entryComponentIndex = entryPath.find(os.path.sep)  # type: int

	if entryComponentIndex == -1:
		entryComponent = entryPath  # type: str
	else:
		entryComponent = entryPath[:entryComponentIndex]  # type: str

	for entry in root.Entries:  # type: _StructureEntry
		if entry.Identifier == entryComponent:
			if entryComponentIndex != -1:
				return _CreateStructureEntry(entry, entryPath[entryComponentIndex + 1:])
			else:
				return entry

	newEntry = _StructureEntry(entryComponent)
	root.Entries.append(newEntry)

	if entryComponentIndex != -1:
		return _CreateStructureEntry(newEntry, entryPath[entryComponentIndex + 1:])
	else:
		return newEntry

def _SortStructure (root: _StructureEntry) -> None:
	if len(root.Entries) == 0:
		return

	duplicateEntries = root.Entries.copy()  # type: typing.List[_StructureEntry]
	sortedEntries = list()  # type: typing.List[_StructureEntry]

	for count in range(len(root.Entries)):  # type: int
		currentEntryIndex = None  # type: int

		for entryIndex in range(len(duplicateEntries)):  # type: int
			if currentEntryIndex is None:
				currentEntryIndex = entryIndex
				continue

			if len(duplicateEntries[entryIndex].Entries) != 0:
				if len(duplicateEntries[currentEntryIndex].Entries) == 0:
					currentEntryIndex = entryIndex
					continue

				if duplicateEntries[currentEntryIndex].Identifier.lower() > duplicateEntries[entryIndex].Identifier.lower():
					currentEntryIndex = entryIndex
					continue
			else:
				if len(duplicateEntries[currentEntryIndex].Entries) == 0:
					if duplicateEntries[currentEntryIndex].Priority is None:

						if duplicateEntries[entryIndex].Priority is not None:
							currentEntryIndex = entryIndex
							continue

						if duplicateEntries[currentEntryIndex].Identifier.lower() > duplicateEntries[entryIndex].Identifier.lower():
							currentEntryIndex = entryIndex
							continue

					else:
						if duplicateEntries[entryIndex].Priority is not None:
							if duplicateEntries[currentEntryIndex].Priority < duplicateEntries[entryIndex].Priority:
								currentEntryIndex = entryIndex
								continue

							if duplicateEntries[currentEntryIndex].Priority == duplicateEntries[entryIndex].Priority:
								if duplicateEntries[currentEntryIndex].Identifier.lower() > duplicateEntries[entryIndex].Identifier.lower():
									currentEntryIndex = entryIndex
									continue

		currentEntry = duplicateEntries.pop(currentEntryIndex)  # type: _StructureEntry
		sortedEntries.append(currentEntry)

	for entry in sortedEntries:  # type: _StructureEntry
		_SortStructure(entry)

	root.Entries.clear()
	root.Entries.extend(sortedEntries)
