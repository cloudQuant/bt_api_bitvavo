from bt_api_base.plugins.protocol import PluginInfo


PLUGIN_INFO = PluginInfo(
    name="bt_api_bitvavo",
    version="0.1.0",
    description="Bitvavo exchange plugin",
    dependencies=["bt_api_base>=0.1.0"],
)


def register_plugin():
    from bt_api_bitvavo.registry_registration import register_bitvavo

    register_bitvavo()
