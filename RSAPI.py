#!/usr/bin/python
"""
Manage resource on the resourcespace through REST API
Xuenan Pi
07/03
"""
import hashlib
import urllib2


class RSAPI(object):
    def __init__(self):
        self.site_ip = "10.217.22.49"
        # admin name and private key
        self.user = "user"
        self.private_key = "2079c5142c54874d1f0b6eb787f96e0f2a79bf960963238cf7778a7ebe449d6c"
        self.function_list = ["get_resource_path", "create_resource", "upload_file", "add_resource_to_collection"]

    def query(self, function_to_query, parameters):
        query = "user=%s&function=%s&%s" % (self.user, function_to_query, parameters)
        sign = hashlib.sha256(self.private_key+query).hexdigest()
        query_url = "http://%s/api/index.php?%s&sign=%s" % (self.site_ip, query, sign)
        try:
            result = urllib2.urlopen(query_url).read()
        except (IOError, UnicodeDecodeError, urllib2.URLError, urllib2.HTTPError) as err:
            pass
        else:
            return result

    @staticmethod
    def get_resource_path_parameter(resource_id, extension):
        get_file_path, size, generate = "true", "", "true"
        page, watermarked, alternative = "", "", ""
        parameters = "param1=%s&param2=%s&param3=%s&param4=%s&param5=%s&param6=%s&param7=%s&param8=%s" \
                     % (resource_id, get_file_path, size, generate, extension, page, watermarked, alternative)
        return parameters

    @staticmethod
    def upload_file_parameter(resource_id, file_path):
        no_exif, revert, autorotate = "1", "", "1"
        parameters = "param1=%s&param2=%s&param3=%s&param4=%s&param5=%s" \
                     % (resource_id, no_exif, revert, autorotate, file_path)
        return parameters

    @staticmethod
    def create_resource_parameter(resource_type):
        parameters = "param1=%s" % resource_type
        return parameters

    @staticmethod
    def add_resource_to_collection_parameter(resource_id, collection_id):
        parameters = "param1=%s&param2=%s" % (resource_id, collection_id)
        return parameters

if __name__=="__main__":
    test = RSAPI()
    print test.query("get_resource_path", test.get_resource_path_parameter("1", "mp3"))


