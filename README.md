#Image-Merging-API

A flask based Web API to merge a two PNG images(i.e background and foreground) and it returns the output image encoded in base64.
The API is REST API and uses nothing for user authentication purposes. Currently, return format for all endpoints is [JSON](http://json.org/ "JSON").

***

##API Resources and URI Structure
URIs for a Image Merging REST API resource have the following structure:

    http://www.example.com/api/v1.0/merge

Send a payload of JSON format like this:

    {
       "foreground_url" : "image url",
       "background_url" : "image url"
    }

**Note**- Request must be JSON type i.e **Content-Type : application/json**

##Media Types
This REST API return HTTP responses in JSON formats:

    {
        "output_image" : "base64 data of output image"
    }
    
##HTTP Error Response 
This REST API also return HTTP error response in JSON formats:

    {
       "Error" : "Error message"
    }

Error Message may be of following types:

   *  Bad Request ( HTTP Error Code : 400)
   *  Not Found ( HTTP Error Code : 404)
   *  Method Not Allowed ( HTTP Error Code : 405)
   *  Internal Server Error ( HTTP Error Code : 500)
 
