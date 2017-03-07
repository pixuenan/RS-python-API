#!/usr/bin/python
"""
Manage resource on the Resourcespace through REST API. The Resourcespace version is 7.9-2.
Xuenan Pi
07/03
"""
import hashlib
import urllib2
import parameters


class RSAPI(object):
    def __init__(self, user, private_key):
        self.site_ip = "10.217.22.49"
        # user name and private key
        # user can only create collection for himself
        # to create a collection for a user, the user's account name and private key has to be used
        self.user = user
        self.private_key = private_key
        # support API functions
        # get_resource_path, create_collection, delete_collection, delete_resource,
        # create_resource, upload_file, update_field, add_resource_to_collection

    def query(self, function_to_query, parameters):
        """
        :return: the query result
        """
        query = "user=%s&function=%s&%s" % (self.user, function_to_query, parameters)
        sign = hashlib.sha256(self.private_key+query).hexdigest()
        query_url = "http://%s/api/index.php?%s&sign=%s" % (self.site_ip, query, sign)
        # print query_url
        try:
            result = urllib2.urlopen(query_url).read()
        except (IOError, UnicodeDecodeError, urllib2.URLError, urllib2.HTTPError) as err:
            print err
        else:
            return result

    def upload_resource(self, file_path, title, collection_id):
        """
        The original file to be uploaded has to be on the same server where Resourcespace is installed.
        Create a resource, move the file to /filestore, attach it to the resource id, add the resource to the
        collection, update title and date for the uploaded file.
        :param file_path: original file path on the server
        :param title: title of the file
        :param collection_id: id of the collection to be added
        """
        resource_id = self.query("create_resource", parameters.create_resource("4"))
        upload_success = self.query("upload_file", parameters.upload_file(resource_id, file_path))
        if upload_success:
            # add title to the resource
            self.query("update_field", parameters.update_field(resource_id, "8", title))
            # add upload date to the resource
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

    def create_collection(self, collection_name):
        collection_id = self.query("create_collection", parameters.create_collection(collection_name))
        return collection_id

    def delete_collection(self, collection_id):
        delete_result = self.query("delete_collection", parameters.delete_collection(collection_id))
        return delete_result

    def delete_resource(self, resource_id):
        """
        Delete the resource. One time query cannot really work.
        Keep query until API return false to make sure the resource is deleted.
        Restrict to 3 iteration of the query.
        """
        for i in range(3):
            delete_result = self.query("delete_resource", parameters.delete_resource(resource_id))
            if not delete_result:
                break

if __name__=="__main__":
    # user = "user"
    # private_key = "2079c5142c54874d1f0b6eb787f96e0f2a79bf960963238cf7778a7ebe449d6c"
    user = "test1"
    private_key = "a62318fb6daabda2c87ca1793575913cae1173165be277c1ab54d9c566ba6157"
    test = RSAPI(user, private_key)
    test.upload_resource("/home/bitnami/test/MaidwiththeFlaxenHair.mp3", "testmusictitle", "8")
    # print test.get_resource_folder("13", "mp3")
    # test.delete_resource("15")
    # print test.create_collection("col1")
