#!/usr/bin/python
"""
Manage resource on the resourcespace through REST API
Xuenan Pi
07/03
"""
import hashlib
import urllib2
import parameters


class RSAPI(object):
    def __init__(self):
        self.site_ip = "10.217.22.49"
        # admin name and private key
        self.user = "user"
        self.private_key = "2079c5142c54874d1f0b6eb787f96e0f2a79bf960963238cf7778a7ebe449d6c"
        self.function_list = ["get_resource_path", "create_resource", "upload_file", "add_resource_to_collection"]

    def query(self, function_to_query, parameters):
        """
        """
        query = "user=%s&function=%s&%s" % (self.user, function_to_query, parameters)
        sign = hashlib.sha256(self.private_key+query).hexdigest()
        query_url = "http://%s/api/index.php?%s&sign=%s" % (self.site_ip, query, sign)
        print query_url
        try:
            result = urllib2.urlopen(query_url).read()
        except (IOError, UnicodeDecodeError, urllib2.URLError, urllib2.HTTPError) as err:
            print err
        else:
            return result

    def upload_resource(self, file_path, title, collection_id):
        """
        Create a resource, move the server file under /filestore, attach it to the resource id, add the resource to the
        collection, update title and date for the upload file.
        :param file_path: original file path on the server
        :param title: title of the file
        :param collection_id: id of the collection to be added
        """
        resource_id = self.query("create_resource", parameters.create_resource("4"))
        upload_success = self.query("upload_file", parameters.upload_file(resource_id, file_path))
        if upload_success:
            self.query("update_field", parameters.update_field(resource_id, "8", title))
            self.query("update_field", parameters.update_field(resource_id, "12"))
            self.query("add_resource_to_collection", parameters.add_resource_to_collection(resource_id, collection_id))

    def get_resource_folder(self, resource_id, extension):
        """
        :return: the server path to the folder that contains the resource file
        """
        full_path = self.query("get_resource_path", parameters.get_resource_path(resource_id, extension))
        if full_path:
            # escape the double quote in the two ends of the string
            # escape the file name because it is the same as the folder name which is not correct
            folder_path = "".join(full_path.split("\\")[1:-1])
            return folder_path

if __name__=="__main__":
    test = RSAPI()
    # resource_path = test.query("get_resource_path", test.get_resource_path("1", "mp3"))
    # resource_id = test.query("create_resource", parameters.create_resource("4"))
    # print resource_id
    # upload_result = test.query("upload_file", parameters.upload_file(resource_id, "/home/bitnami/test/MaidwiththeFlaxenHair.mp3"))
    # print upload_result
    # add_result = test.query("add_resource_to_collection", parameters.add_resource_to_collection("13", "3"))
    # print add_result
    # update_field_result = test.query("update_field", parameters.update_field("13", "12"))
    # print update_field_result
    # test.upload_resource("/home/bitnami/test/MaidwiththeFlaxenHair.mp3", "testmusictitle", "3")
    print test.get_resource_folder("13", "mp3")

