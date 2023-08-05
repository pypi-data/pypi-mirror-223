"""
    update the site settings
"""
from ramda import path_or
from reva.lib.utils.get_namespaces import get_namespace_by_argument_and_path
from reva.lib.base.base import RevaUpdate
from reva.lib.graphql_queries.site_settings import update_site_settings_query
from reva.lib.utils.filter_data_with_id import filter_data_with_id

class SiteSettingsUpdate(RevaUpdate):
    """
    update the site settings
    """

    def __init__(self, arguments):
        super().__init__(arguments)
        self.argument = arguments

    def get_json_paths_to_update(self):
        """
        THis function will return the json files
        to update
        """
        namespaces_to_update = get_namespace_by_argument_and_path(
            self.argument, self.get_ui_customization_path()
        )
        return self.get_file_paths_ui(namespaces_to_update, ["STS_"])

    def start(self):
        """
        update the site settings
        """
        site_settings_json_data = self.get_file_by_paths(
            self.get_json_paths_to_update()
        )
        query_datas = []
        for json_data in site_settings_json_data:
            filtered_json_data = filter_data_with_id(path_or([],["data"], json_data))
            if not filtered_json_data:
                continue
            query_datas.append(update_site_settings_query(filtered_json_data))
        return self.excecute_for_list_of_query_data(query_datas)
