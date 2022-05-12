import argparse
from googleapiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

def get_service(api_name, api_version, scope, client_secrets_path):

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
  flags = parser.parse_args([])

  flow = client.flow_from_clientsecrets(
      client_secrets_path, scope=scope,
      message=tools.message_if_missing(client_secrets_path))

  storage = file.Storage(api_name + '.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage, flags)
  http = credentials.authorize(http=httplib2.Http())

  service = build(api_name, api_version, http=http)

  return service

def get_first_profile_id(service):
  accounts = service.management().accounts().list().execute()
  if accounts.get('items'):
    account = accounts.get('items')[0].get('id')
    properties = service.management().webproperties().list(
        accountId=account).execute()
      
    if properties.get('items'):
      property = properties.get('items')[0].get('id')
      profiles = service.management().profiles().list(
          accountId=account,
          webPropertyId=property).execute()

      if profiles.get('items'):
        return profiles.get('items')[0].get('id')

  return None

def get_results(service, profile_id):
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='2019-10-01',
      end_date='today',
      metrics='ga:sessions, ga:newUsers, ga:Users',
      dimensions='ga:socialNetwork, ga:deviceCategory, ga:city, ga:year, ga:month, ga:day').execute()

def print_results(results):
  if results:
    print( 'View (Profile): %s'% results.get('profileInfo').get('profileName'))

  else:
    print ('No results found')

# def viewid():
#   scope = ['https://www.googleapis.com/auth/analytics.readonly']
#   service = get_service('analytics', 'v3', scope, 'client_secret_10241093559.json')
#   profile = get_first_profile_id(service)
#   print(get_results(service, profile))

# if __name__ == '__main__':
#   viewid()