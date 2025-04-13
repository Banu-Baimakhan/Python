from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]]=param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config


if __name__=='__main__':
    config=load_config()
    print(config)
    
#This code shouldn't run, because it is just parser.
#However I've already created the database which called labwork using these actions:
#on the terminal I wrote the command: psql -U postgres
#Then I signed with password, in my case password is password
#Then I wrote this command: CREATE DATABASE labwork;