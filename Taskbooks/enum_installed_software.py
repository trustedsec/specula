def TaskBook(helpers, agent):
    mod = helpers.get_module('operation/file/list_dir')
    helpers.setModOption(mod, 'directory', optval="c:\Program Files")
    helpers.setModOption(mod, 'recurselevels', optval="0")
    helpers.setModOption(mod, 'depth', optval="0")
    helpers.setModOption(mod, 'filetype', optval="*")
    helpers.setModOption(mod, 'filename', optval="*")
    helpers.setModOption(mod, 'nodirectories', optval="False")
    helpers.setModOption(mod, 'sizeformat', optval="mb")
    helpers.setModOption(mod, 'nofiles', optval="True")
    helpers.setModOption(mod, 'output_console', optval="False")
    helpers.insertTask(agent, mod, 'operation/file/list_dir')

    mod = helpers.get_module('operation/file/list_dir')
    helpers.setModOption(mod, 'directory', optval="c:\Program Files (x86)")
    helpers.setModOption(mod, 'recurselevels', optval="0")
    helpers.setModOption(mod, 'depth', optval="0")
    helpers.setModOption(mod, 'filetype', optval="*")
    helpers.setModOption(mod, 'filename', optval="*")
    helpers.setModOption(mod, 'nodirectories', optval="False")
    helpers.setModOption(mod, 'sizeformat', optval="mb")
    helpers.setModOption(mod, 'nofiles', optval="True")
    helpers.setModOption(mod, 'output_console', optval="False")
    helpers.insertTask(agent, mod, 'operation/file/list_dir')
    
    mod = helpers.get_module('enumerate/host/list_installedapps')
    helpers.insertTask(agent, mod, 'enumerate/host/list_installedapps')