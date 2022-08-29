from fcache.cache import FileCache
import hashlib
import logging

class Cache:

	def __init__(self, name):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing "+ name + " cache ...")

		self.file_cache = FileCache(name, flag='cs')
		num_elements = len(list(self.file_cache))
		if (num_elements > 0):
			print("Loading",num_elements,"elements from cache:",self.file_cache.cache_dir,"...")
		else:
			print("initializing cache in",self.file_cache.cache_dir,"...")


	def get_hash(self,text):
		hash_object = hashlib.md5(text.encode())
		md5_hash = hash_object.hexdigest()
		return str(md5_hash)
    		
	def close(self):
		self.file_cache.close()

	def get(self,key):
		key_value = self.get_hash(key)
		self.logger.debug("reading value of "+ key_value + " from cache")
		return self.file_cache[key_value]

	def set(self,key,value):
		key_value = self.get_hash(key)
		self.file_cache[key_value] = value

	def exists(self,key):
		key_value = self.get_hash(key)
		return key_value in self.file_cache