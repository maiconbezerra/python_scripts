import requests


class JumpCloud:

    def __init__(self, jc_api_call_header):
        self.jc_api_call_header = jc_api_call_header

    def jc_show_config(self):
        print(self.jc_api_call_header)

    '''
    USER GROUP CONFIGURATIONS
    '''
    #  Configure string query parameters
    def jc_set_usergroup_sq(self, jc_output_limit=50, jc_query_skip=0):
        """
        Used to set default string query for user groups in JumpCloud.
            -> jc_output_limit = The number of records to return at once (Limited to 100.
            -> jc_query_skip = The offset into the records to return.

        :param jc_output_limit - Limit the number of objets to be showed
        :param jc_query_skip - Set position where the query will start.
                For example: If you set to zero, the search will start from zero position
        """

        #  Configure HTTP parameters
        jc_query_string = {'limit': jc_output_limit,
                           'skip': jc_query_skip}

        return jc_query_string

    #  List user groups
    def jc_ls_usergroup(self, jc_string_query, grp_search='all'):
        """
        Query for user groups in JumpCloud.
        :param jc_string_query = Sets string query used on search.
        :param grp_search = By defaul, search for all groups (grp_seach=all). You can set value to search too.
        """

        #  All user groups
        jc_all_usergroups = list()

        #  API Call Parameters
        jc_api_call_url = 'https://console.jumpcloud.com/api/v2/groups'
        jc_api_call_header = self.jc_api_call_header
        jc_api_call_sq = jc_string_query

        #  Gets all group users
        response = requests.get(url=jc_api_call_url, headers=jc_api_call_header, params=jc_api_call_sq)
        jc_usergrp = response.json()

        for groups in jc_usergrp:
            jc_all_usergroups.append(groups)

        skip = 0
        while True:
            if jc_usergrp:

                jc_usergrp.clear()  # Clear list
                skip += 50  # Changing skip value
                jc_api_call_sq['skip'] = skip  # Changing skip value

                #  API call
                response = requests.get(url=jc_api_call_url, headers=jc_api_call_header, params=jc_api_call_sq)
                jc_usergrp = response.json()

                for groups in jc_usergrp:
                    jc_all_usergroups.append(groups)

                continue
            else:
                break

        if grp_search == 'all':
            #  Return all groups
            return jc_all_usergroups
        else:
            jc_filtered_usergroups = list()

            #  Expanding groups and filter groups based on search criteria
            for groups in jc_all_usergroups:
                if grp_search in groups['name']:
                    jc_filtered_usergroups.append(groups)

            #  Return filtered groups
            return jc_filtered_usergroups

    def jc_ls_usergroup_membership(self, jc_usergroup_id, jc_string_query):
        """
        Query for user groups membership in JumpCloud.
        :param jc_usergroup_id - JumpCloud unique id
        :param

         For more information
            format: https://console.jumpcloud.com/api/v2/usergroups/{Group-ID}/members'
            https://docs.jumpcloud.com/api/2.0/index.html#tag/User-Groups/operation/graph_userGroupMembersList
        """
        #  All user groups
        jc_all_usergroup_membership = list()

        #  API Call Parameters
        jc_api_call_url = 'https://console.jumpcloud.com/api/v2/usergroups/' + jc_usergroup_id + '/members'
        jc_api_call_header = self.jc_api_call_header
        jc_api_call_sq = jc_string_query

        #  Gets all group users
        response = requests.get(url=jc_api_call_url, headers=jc_api_call_header, params=jc_api_call_sq)
        jc_usergroup_membership = response.json()

        for members in jc_usergroup_membership:
            jc_all_usergroup_membership.append(members)

        skip = 0
        while True:
            if jc_usergroup_membership:

                jc_usergroup_membership.clear()  # Clear list
                skip += 50  # Changing skip value
                jc_api_call_sq['skip'] = skip  # Changing skip value

                #  API call
                response = requests.get(url=jc_api_call_url, headers=jc_api_call_header, params=jc_api_call_sq)
                jc_usergroup_membership = response.json()

                for groups in jc_usergroup_membership:
                    jc_all_usergroup_membership.append(groups)

                continue
            else:
                break

        return jc_all_usergroup_membership

    def jc_system_users(self, jc_string_query):
        jc_all_systemusers = list()

        #  API Call Parameters
        jc_api_call_url = 'https://console.jumpcloud.com/api/systemusers'
        jc_api_call_header = self.jc_api_call_header
        jc_api_call_sq = jc_string_query

        #  Gets all group users
        response = requests.get(url=jc_api_call_url, headers=jc_api_call_header, params=jc_api_call_sq)
        jc_system_users = response.json()

        #  Getting users
        for users in jc_system_users['results']:
            jc_all_systemusers.append(users)

        skip = 0
        while True:
            if jc_system_users['results']:
                jc_system_users.clear()  # Clear list
                skip += 50  # Changing skip value
                jc_api_call_sq['skip'] = skip  # Changing skip value

                #  API call
                response = requests.get(url=jc_api_call_url, headers=jc_api_call_header, params=jc_api_call_sq)
                jc_system_users = response.json()

                for users in jc_system_users['results']:
                    jc_all_systemusers.append(users)
                continue

            else:
                break

        return jc_all_systemusers