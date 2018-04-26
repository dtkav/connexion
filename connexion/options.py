import pathlib
from typing import Optional  # NOQA

MODULE_PATH = pathlib.Path(__file__).absolute().parent

class ConnexionOptions(object):
    def __init__(self, options=None):
        self._options = {}
        if options:
            self._options.update(filter_values(options))

    def extend(self, new_values=None):
        # type: (Optional[dict]) -> ConnexionOptions
        """
        Return a new instance of `ConnexionOptions` using as default the currently
        defined options.
        """
        if new_values is None:
            new_values = {}

        options = dict(self._options)
        options.update(filter_values(new_values))
        return ConnexionOptions(options)

    def as_dict(self):
        return self._options

    @property
    def openapi_spec_available(self):
        # type: () -> bool
        """
        Whether to make available the OpenAPI Specification under
        `openapi_console_ui_path`/swagger.json path.

        Default: True
        """
        # NOTE: Under OpenAPI v3 this should change to "/openapi.json"
        return self._options.get('swagger_json', True)

    @property
    def openapi_spec_version(self):
        # type: () -> str
        """
        The version of the OpenAPI Specification

        Default: "2.0.0"
        """
        return self._options.get('openapi_spec_version', "2.0.0")

    @property
    def openapi_spec_major_version(self):
        # type: () -> str
        """
        The major version of the OpenAPI Specification (likely either "2" or "3")
        """
        return self._options.get('openapi_spec_version', "2.0.0").split(".")[0]

    @property
    def openapi_console_ui_available(self):
        # type: () -> bool
        """
        Whether to make the OpenAPI Console UI available under the path
        defined in `openapi_console_ui_path` option. Note that if enabled,
        this overrides the `openapi_spec_available` option since the specification
        is required to be available via a HTTP endpoint to display the console UI.

        Default: True
        """
        return self._options.get('swagger_ui', True)

    @property
    def openapi_spec_path(self):
        # type: () -> str
        """
        Path to mount the OpenAPI Console UI and make it accessible via a browser.

        Default: /openapi.json for openapi3, otherwise /swagger.json
        """
        major_version = self.openapi_spec_major_version
        default_path = "/swagger.json"
        if major_version == "3":
            default_path = "/openapi.json"
        return self._options.get('openapi_spec_path', default_path)

    @property
    def openapi_console_ui_path(self):
        # type: () -> str
        """
        Path to mount the OpenAPI Console UI and make it accessible via a browser.

        Default: /ui
        """
        return self._options.get('swagger_url', '/ui')

    @property
    def openapi_console_ui_from_dir(self):
        # type: () -> str
        """
        Custom OpenAPI Console UI directory from where Connexion will serve
        the static files.

        Default: Connexion's vendored version of the OpenAPI Console UI.
        """
        major_version = self.openapi_spec_major_version
        ui_path = MODULE_PATH / 'vendor' / 'swagger-ui-{version}'.format(
            version=major_version)
        return self._options.get('swagger_path', ui_path)


def filter_values(dictionary):
    # type: (dict) -> dict
    """
    Remove `None` value entries in the dictionary.

    :param dictionary:
    :return:
    """
    return dict([(key, value)
                 for key, value in dictionary.items()
                 if value is not None])
