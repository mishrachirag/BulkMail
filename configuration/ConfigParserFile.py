from configparser import ConfigParser

def changeConfig(keydata,valuedata):
    parser = ConfigParser()
    parser.read('configuration/configuration.txt')
    parser.set('Setting',keydata,valuedata)
    with open('configuration/configuration.txt','w') as configFile:
        parser.write(configFile)