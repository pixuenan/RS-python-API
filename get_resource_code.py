#!/usr/bin/python
"""
Upload audio files to the resourcespace through REST API
03/03
"""
import hashlib
# import json
private_key = "*"
user = "test1"
resource_ID = "1"
get_file_path = "true"
size = ""
generate = "true"
extension = "mp3"
page, watermarked, alternative = "", "", ""
query = "user=%s&function=get_resource_path&param1=%s&param2=%s&param3=%s&param4=%s&param5=%s&param6=%s&param7=%s&param8=%s" \
        % (user, resource_ID, get_file_path, size, generate, extension, page, watermarked, alternative)
sign = hashlib.sha256(private_key+query).hexdigest()
print sign
query_url = "http://*/api/index.php?%s&sign=%s" % (query, sign)
print query_url
# result = json.loads()
