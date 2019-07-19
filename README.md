Image-Merger-API
-----------------------

A Flask based Web API to merge a two PNG images(i.e may be background and foreground) and it returns the output image url and in base64 format also.
The API is REST API and uses nothing for user authentication purposes. Currently, return format for all endpoints is [JSON](http://json.org/ "JSON").

## API Resources and URI Structure
URIs for a Image Merging REST API resource have the following structure:

    http://image-merger.herokuapp.com/api/v1.0/
Method Supported : **POST**

Send a payload of JSON format like this:

    {
       "foreground_url" : "image url",
       "background_url" : "image url"
    }

**Note** :

  1. Request must be JSON type i.e **Content-Type : application/json**
  2. Images should be of same sizes and of **PNG** format.

## Media Types
This REST API return HTTP responses in JSON formats:

    {
        "output_image" : {
            "name" : "Image Name",
            "url" : "Image Absolute Url",
            "base64" : "Image in base64 format"
        }
    }

You can download the merged output image through url returned in reponse.

## HTTP Error Response
This REST API also return HTTP error response in JSON formats with proper HTTP Status Code as follows:

    {
       "Error" : "Message"
    }

Error Message may be of following types:

   *  Not Valid Url ( __HTTP Status Code : 202__ )
   *  Images Not Found ( __HTTP Status Code : 202__ )
   *  Format Not Supported ( __HTTP Status Code : 202__ )
   *  Not Same Size Images ( __HTTP Status Code : 202__ )
   *  Internal Error. Please Try Again ( __HTTP Status Code : 202__ )
   *  Bad Request ( __HTTP Status Code : 400__ )
   *  Not Found ( __HTTP Status Code : 404__ )
   *  Method Not Allowed ( __HTTP Status Code : 405__ )
   *  Internal Server Error ( __HTTP Status Code : 500__ )

## Example
Let we make a **POST** request with payload in valid format, like this:

    {
       "foreground_url" : "http://akshayon.net/images/foreground.png",
       "background_url" : "http://akshayon.net/images/background.png"
    }

**Foreground Image**
![Foreground Image](http://akshayon.net/images/foreground.png "Foreground Image")

**Background Image**
![Background Image](http://akshayon.net/images/background.png "Background Image")

Then , we get a response in JSON style , like this:

    {
        "output_image" : {
            "name" : "5c359e06d7b9e4c21b699758c18ce335.jpeg",
            "url" : "http://image-merger.herokuapp.com/image/5c359e06d7b9e4c21b699758c18ce335.jpeg",
            "base64" : "iVBORw0KGgoAAAANSUhEUgA.....SUVORK5CYII="
        }
    }

**Merged Output Image**
![Merged Image](http://akshayon.net/images/merged.jpeg "Merged Image")

