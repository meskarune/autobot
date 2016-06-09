class PluginManager(object):
    def __init__(self, botnick, prefix):
        """ Manage Plugins """
        self.plugin_list = []

        self.botnick = botnick
        self.prefix = prefix

        command_regex = re.compile(
                   r'^(' + re.escape(self.botnick) + '( |[:,] ?)'
                   r'|' + re.escape(self.prefix) + ')'
                   r'([^ ]*)( (.*))?$', re.IGNORECASE)
    def load_plugins(self):
        for plugin in plugin_list:
            try:
                importlib.import_module(plugins.plugin)
            except Exception:
                sys.stderr.write("{0} didn't load correctly".format(plugin))
                continue
    def reload_plugin(self, plugin):
        try:
            importlib.reload(plugin_list[plugin])
    def reply(self, command):
        if is_threaded:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                response = executor.map(do_command, command)
        else:
                do_command(command)
