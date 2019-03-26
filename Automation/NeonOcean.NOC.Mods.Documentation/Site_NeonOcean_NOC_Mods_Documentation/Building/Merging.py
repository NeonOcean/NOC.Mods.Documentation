import os
from distutils import dir_util

from Site_NeonOcean_NOC_Mods_Documentation import Paths
from Site_NeonOcean_NOC_Mods_Documentation.Tools import IO

def Merge () -> None:
	IO.ClearDirectory(Paths.BuildPath)

	_MergeLoose()
	_MergeDocuments()
	_MergeStructure()

def _MergeLoose () -> None:
	if os.path.exists(Paths.LoosePath):
		dir_util.copy_tree(Paths.LoosePath, Paths.BuildPath)

def _MergeDocuments () -> None:
	if os.path.exists(Paths.DocumentsBuildPath):
		dir_util.copy_tree(Paths.DocumentsBuildPath, Paths.BuildPath)

def _MergeStructure () -> None:
	if os.path.exists(Paths.StructureBuildPath):
		dir_util.copy_tree(Paths.StructureBuildPath, Paths.BuildPath)