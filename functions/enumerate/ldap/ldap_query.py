from lib.core.specmodule import SpecModule
from lib.modhandlers.generic import quotedstring,escapequotes


class Spec(SpecModule):
    def __init__(self, templatepath, helpers):
        self.options = {}
        self.helpers = helpers
        self.help = """
        A module to query LDAP with. To find a list of attributes/values to query use WMI Explorer and look under ROOT\directory\LDAP.
        Some classes: ds_domain, ds_computer , ds_container , ds_group , ds_top , ds_user 
        Currently not getting all attributes. Struggling with SWbemObjectEx sub objects.

        The WHERE_* is only used if they are specified. 
        A query without WHERE_* specified looks like this:
        SELECT <SELECT OPTION> FROM <FROM OPTION>

        A query with WHERE_* specified looks like this:
        SELECT <SELECT OPTION> FROM <FROM OPTION> WHERE <WHERE_Attribute> = '<WHERE_Value>'

        It uses WbemScripting.SWbemLocator
        - ConnectServer(\\root\\directory\\LDAP)
        - Query: SELECT <SELECT OPTION> FROM <FROM OPTION> WHERE <WHERE_Attribute> = '<WHERE_Value>'
        """
        self.entry = 'ldap_query'
        self.depends = []
        self.options['SELECT'] = {
            "value": "*",
            "required": True,
            "description": "Attribute to get - Ex: DS_givenName or DS_samaccountname or * for everything"
        }
        self.options['FROM'] = {
            "value": "ds_user",
            "required": True,
            "description": "What Class to get the attributes from - Ex: ds_user or ds_computer or ds_domain"
        }
        self.options['WHERE_Attribute'] = {
            "value": None,
            "required": False,
            "description": "Specify attribute Search critera. Only used if specified. Ex: ds_samaccountname"
        }
        self.options['WHERE_Value'] = {
            "value": None,
            "required": False,
            "description": "Specify what to search for. Ex: user1"
        }
        self.options['query'] = {
            "value": "Will_Be_generated_from_other_options",
            "required": True,
            "description": "Query that is issued, You do not need to set this option since it is generated based on the other options, only reason this is shown is so you can see it in qlist",
            "handler": quotedstring
        }
        super().__init__(templatepath)

    def preprocess(self, agent):
        if self.options['WHERE_Attribute']['value'] and self.options['WHERE_Value']['value'] == None:
            raise RuntimeError("Need to specify WHERE_Value when you are specifying WHERE_Attribute")
        if self.options['WHERE_Value']['value'] and self.options['WHERE_Attribute']['value'] == None:
            raise RuntimeError("Need to specify WHERE_Attribute when you are specifying WHERE_Value")
        
        if self.options['WHERE_Attribute']['value'] and self.options['WHERE_Value']['value']:
               composed_query = "SELECT " + self.options['SELECT']['value'] + " FROM " + self.options['FROM']['value'] + " Where " + self.options['WHERE_Attribute']['value'] + " = '" + self.options['WHERE_Value']['value'] + "'"
        else:
            composed_query = "SELECT " + self.options['SELECT']['value'] + " FROM " + self.options['FROM']['value']
        
        self.options['query']['value'] = composed_query
        