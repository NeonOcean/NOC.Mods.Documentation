import os
import typing
import json

from Site_NeonOcean_NOC_Mods_Documentation import Paths
from Site_NeonOcean_NOC_Mods_Documentation.Tools import Formatting

def BuildBreadcrumbs (documentPath: str) -> str:
	documentPath = documentPath.replace(os.path.altsep, os.path.sep)

	with open(os.path.join(Paths.TemplatesPath, "BreadcrumbsPart.html")) as breadcrumbsPartTemplateFile:
		breadcrumbsPartText = breadcrumbsPartTemplateFile.read()  # type: str

	with open(os.path.join(Paths.TemplatesPath, "BreadcrumbsLink.html")) as breadcrumbsLinkTemplateFile:
		breadcrumbsLinkText = breadcrumbsLinkTemplateFile.read()  # type: str

	with open(os.path.join(Paths.TemplatesPath, "BreadcrumbsSeparator.html")) as breadcrumbsSeparatorTemplateFile:
		breadcrumbsSeparatorText = breadcrumbsSeparatorTemplateFile.read()  # type: str

	combinedText = ""

	documentPathParts = documentPath.split(os.path.sep)  # type: typing.List[str]

	for documentPathPartIndex in range(len(documentPathParts)):
		combinedPathParts = str.join(os.path.sep, documentPathParts[:documentPathPartIndex])  # type: str

		if combinedPathParts == documentPath:
			currentStructureConfigFilePath = os.path.join(Paths.StructureSourcePath, os.path.splitext(combinedPathParts)[0] + ".json")
			currentDocumentPath = combinedPathParts
		else:
			currentStructureConfigFilePath = os.path.join(Paths.StructureSourcePath, combinedPathParts, "index.json")  # type: str
			currentDocumentPath = os.path.join(combinedPathParts, "index.html")

		if os.path.exists(currentStructureConfigFilePath):
			with open(currentStructureConfigFilePath) as currentStructureConfigFile:
				currentStructureConfig = json.JSONDecoder().decode(currentStructureConfigFile.read())  # type: dict

			currentStructureInvisible = currentStructureConfig["Invisible"]  # type: bool
			currentStructureName = currentStructureConfig["Name"]  # type: str
			currentStructureLink = currentStructureConfig["Link"]  # type: bool

			if currentStructureInvisible:
				continue

			if currentStructureLink:
				breadcrumbText = Formatting.Format(breadcrumbsLinkText, BreadcrumbName = currentStructureName, BreadcrumbLink = currentDocumentPath)  # type: str
			else:
				breadcrumbText = Formatting.Format(breadcrumbsPartText, BreadcrumbName = currentStructureName)  # type: str

			if combinedText != "":
				combinedText += "\n\n" + breadcrumbsSeparatorText + "\n\n" + breadcrumbText
			else:
				combinedText += breadcrumbText

	if os.path.splitext(os.path.split(documentPath)[1])[0] != "index":
		structureConfigFilePath = os.path.join(Paths.StructureSourcePath, os.path.splitext(documentPath)[0] + ".json")  # type: str

		if os.path.exists(structureConfigFilePath):
			with open(structureConfigFilePath) as structureConfigFile:
				structureConfig = json.JSONDecoder().decode(structureConfigFile.read())  # type: dict

			structureInvisible = structureConfig["Invisible"]  # type: bool
			structureName = structureConfig["Name"]  # type: str
			structureLink = structureConfig["Link"]  # type: bool

			if not structureInvisible:
				if structureLink:
					breadcrumbText = Formatting.Format(breadcrumbsLinkText, BreadcrumbName = structureName, BreadcrumbLink = documentPath)  # type: str
				else:
					breadcrumbText = Formatting.Format(breadcrumbsPartText, BreadcrumbName = structureName)  # type: str

				if combinedText != "":
					combinedText += "\n\n" + breadcrumbsSeparatorText + "\n\n" + breadcrumbText
				else:
					combinedText += breadcrumbText

	return combinedText