Help on module pyfree:

NAME
    pyfree

FILE
    /home/saou/Documents/pyfree/pyfree/pyfree.py

DESCRIPTION
    This API is an unofficial imlplementation of the official Freebox OS API
    detailed here http://dev.freebox.fr/sdk/os/

CLASSES
    Freebox
    
    class Freebox
     |  Methods defined here:
     |  
     |  __init__(self, freebox_ip=None, freebox_port=None, debug=False)
     |  
     |  ask_authorization(self, app_id, app_name, app_version, device_name)
     |      This must be call the first time the application is lauched.
     |      An authorization has to be done directly on the Freebox.
     |      See http://dev.freebox.fr/sdk/os/login/
     |  
     |  create_contact(self, display_name=None, first_name=None, last_name=None)
     |      Create a contact.
     |      See http://dev.freebox.fr/sdk/os/contacts/
     |  
     |  delete_contact(self, contact_id)
     |      Delete a contact.
     |      See http://dev.freebox.fr/sdk/os/contacts/
     |  
     |  download_file(self, file_path_b64, file_path_save)
     |      Dowload file 'file_path_b64' and save it at 'file_path_save'
     |      See http://dev.freebox.fr/sdk/os/fs/#download-a-file
     |  
     |  get_call_list(self)
     |      Access the Freebox call logs.
     |      See http://dev.freebox.fr/sdk/os/call/
     |  
     |  get_contact(self, contact_id)
     |      Access a given contact entry.
     |      See http://dev.freebox.fr/sdk/os/contacts/
     |  
     |  get_contact_list(self)
     |      Get list of contacts.
     |      See http://dev.freebox.fr/sdk/os/contacts/
     |  
     |  get_file_list(self, directory)
     |      Get a list of files from a specific directory.
     |      See http://dev.freebox.fr/sdk/os/fs/#list-files
     |  
     |  get_lcd_config(self)
     |      Get the current LCD configuration.
     |      See http://dev.freebox.fr/sdk/os/lcd/
     |  
     |  get_missed_call(self, today=False, convert_date=True)
     |      Return missing call generator.
     |      See http://dev.freebox.fr/sdk/os/call/
     |  
     |  is_authorization_granted(self)
     |      Return True if an authorization has already been granted on the freebox.
     |  
     |  login(self, app_id)
     |      This function has to be called after the authorization has been granted by the function ask_authorization.
     |  
     |  print_debug(self, message)
     |  
     |  reboot(self)
     |      Reboot Freebox
     |  
     |  set_wifi_status(self, enabled=True)
     |      Change Wifi status (on/off)
     |      See http://dev.freebox.fr/sdk/os/wifi/
     |  
     |  update_lcd_config(self, brightness=None, orientation=None, orientation_forced=None)
     |      Update the current LCD configuration.
     |      See http://dev.freebox.fr/sdk/os/lcd/
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  api_base_url
     |      The API root path on the HTTP server.
     |  
     |  api_version
     |      The current API version on the Freebox.
     |  
     |  device_name
     |      The device name "Freebox Server".
     |  
     |  device_type
     |      “FreeboxServer1,1” for the Freebox Server revision 1,1
     |  
     |  uid
     |      The device unique id.
