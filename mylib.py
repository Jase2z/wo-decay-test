import requests
from requests.exceptions import HTTPError

class DashBunnyStorage:
    """
    dash.bunny.net utilities.
    """

    def __init__(self, api_key, storage_zone, storage_zone_region="de"):
        """
        Creates an object for using BunnyCDN Storage API
        Parameters
        ----------
        api_key                                 : String
                                                  Your bunnycdn storage
                                                  Apikey/FTP password of
                                                  storage zone

        storage_zone                            : String
                                                  Name of your storage zone

        storage_zone_region(optional parameter) : String
                                                  The storage zone region code
                                                  as per BunnyCDN
        """
        self.headers = {
            # headers to be passed in HTTP requests
            "AccessKey": api_key,
            "Content-Type": "application/json",
            "Accept": "applcation/json",
        }

        # applying constraint that storage_zone must be specified
        assert storage_zone != "", "storage_zone is not specified/missing"

        # For generating base_url for sending requests
        if storage_zone_region == "de" or storage_zone_region == "":
            self.base_url = "https://storage.bunnycdn.com/" + storage_zone + "/"
        else:
            self.base_url = (
                "https://"
                + storage_zone_region
                + ".storage.bunnycdn.com/"
                + storage_zone
                + "/"
            )
    
    def GetStoragedObjectsList(self) -> list[dict]:
        """
        This functions returns a list of files and directories located in a
        given storage_path.
        """
        
        b = bytearray()
        http_status = int()
        storage_list = []
        url = self.base_url
        # Sending GET request
        try:
            with requests.get(url, headers=self.headers) as r:
                http_status = r.status_code
                r.raise_for_status()
                for dictionary in r.json():
                    temp_dict = {}
                    for key in dictionary:
                        if key == "ObjectName" and dictionary["IsDirectory"] is False:
                            temp_dict["File_Name"] = dictionary[key]
                        if key == "ObjectName" and dictionary["IsDirectory"]:
                            temp_dict["Folder_Name"] = dictionary[key]
                    storage_list.append(temp_dict)
            return storage_list
        except HTTPError as http:
            return {
                "status": "error",
                "HTTP": http_status,
                "msg": f"http error occured {http}",
            }   

    def DownloadStorageFile(self, file_name: str) -> dict:
        # to return appropriate help messages if file is present or not and download file if present
        b = bytes()
        http_status = int()
        url = f'{self.base_url}{file_name}'
        try:
            with requests.get(url, headers=self.headers, stream=True) as r:
                http_status = r.status_code
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=None):
                    if chunk:
                        b = b''.join([b, chunk])
                return {
                "status": "success",
                "HTTP": http_status,
                "msg": "File downloaded Successfully",
                "data": b
            }
        except HTTPError as http:
            return {
                "status": "error",
                "HTTP": http_status,
                "msg": f"Http error occured {http}",
            }
        except Exception as err:
            return {
                "status": "error",
                "HTTP": http_status,
                "msg": f"error occured {err}",
            }
