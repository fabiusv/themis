from .gcloud import *
from .openai import *
from .gcloud.client_api_key import credentials as gcp_client_api_key
from .gcloud.client_secret import credentials as gcp_client_secret
from .openai.openai_key import credentials as openai_key

class Authenticator():

  @staticmethod
  def get_openai_key():
    return openai_key["api_key"]
  
  @staticmethod 
  def get_google_cloud_key():
    return gcp_client_api_key["api_key"]

  @staticmethod
  def get_google_cloud_client_secret():
    return gcp_client_secret["client_secret"]
  
  @staticmethod
  def get_maps_platform_key():
    return gcp_client_api_key["api_key"]
