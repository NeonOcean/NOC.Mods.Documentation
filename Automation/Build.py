if __name__ == "__main__":
	import os
	import sys
	from importlib import util
		
	sys.path.append(os.path.join(os.path.dirname(__file__), "NeonOcean.NOC.Mods.Documentation"))
	Main = util.find_spec("Site_NeonOcean_NOC_Mods_Documentation.Main").loader.load_module()
		
	Main.BuildSite()