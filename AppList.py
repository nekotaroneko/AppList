# coding: utf-8

'''
JB Device needed
Return App data
App List
'''
import glob
import os,six

try:
	import biplist
except:
	from stash.stash import StaSh
	_stash = StaSh()
	#_stash.launch()
	_stash("pip install biplist")
finally:
	import biplist

class AppList (object):
	def __init__(self):
		self.app_dict = {}
		app_plist = glob.glob('/var/containers/Bundle/Application/*/iTunesMetadata.plist')
		if len(app_plist) == 0:
			print('Your device seem to be jailed')
		else:
			
			for _plist in app_plist:
				data = biplist.readPlist(_plist)
				id = data['softwareVersionBundleId']
				if 'bundleDisplayName' in data:
					name = data['bundleDisplayName']
				elif 'title' in data: #for TestFlight app
					name = data['title']
				else:
					name = None
				
				
				self.app_dict[id] = {'name':name, 'id':id,'app_dir':os.path.dirname(_plist)}
		
			app_data_plist = glob.glob('/var/mobile/Containers/Data/Application/*/.com.apple.mobile_container_manager.metadata.plist')
			for _plist in app_data_plist:
				data = biplist.readPlist(_plist)
				id = data['MCMMetadataIdentifier']
				if id in self.app_dict:
					self.app_dict[id]['data_dir'] = os.path.dirname(_plist)#os.path.join(os.path.dirname(_plist),'Documents')
				
	def search_by_name(self,name):
		result = False
		for id, _dict in six.iteritems(self.app_dict):
			app_name = _dict['name']
			if app_name:
				if name in app_name:
					result = _dict
		if result:
			return result
		else:
			return None
	
	def search_by_id(self,id):
		result = False
		for app_id, _dict in six.iteritems(self.app_dict):
			if id in app_id:
				result = _dict
		if result:
			return result
		else:
			return None
			

if __name__ == '__main__':
	App_List = AppList()
	app_name = 'Pythonista'
	data = App_List.search_by_name(app_name)
	if data:
		app_dir = data['app_dir']
		print(data)
		import subprocess
	#subprocess.call(['uiopen','filza://{}'.format(app_dir)])
