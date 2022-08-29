from fcache.cache import FileCache

class Cache:

	def __init__(self, name):
		self.file_cache = FileCache(name, flag='cs')
		num_elements = len(list(self.file_cache))
		if (num_elements > 0):
			print("Loading",num_elements,"elements from cache:",self.file_cache.dir,"...")
		else:
			print("initializing cache in",self.file_cache.dir,"...")

	def close(self):
		self.file_cache.close()

	def get(self,key):
		return self.file_cache[key]

	def set(self,key,value):
		self.file_cache[key] = value

	def exists(self,key):
		return self.file_cache[key]