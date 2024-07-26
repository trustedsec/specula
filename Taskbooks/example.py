def TaskBook(helpers, agent):
    mod = helpers.get_module('enumerate/host/list_applocker') # this doesn't take arguments, so we aren't giving it any
    helpers.insertTask(agent, mod, 'enumerate/host/list_applocker')
    mod = helpers.get_module('execute/host/cmd') # this does take an argument so we need to populate it
    helpers.setModOption(mod, 'command', prompt="What command would you like to run: ")
    helpers.insertTask(agent, mod, 'execute/host/cmd')
    #we don't have to prompt for the input though
    mod = helpers.get_module('operation/file/listdir')
    helpers.setModOption(mod, 'strpath', optval="C:\Windows")
    helpers.insertTask(agent, mod, 'operation/file/listdir')



