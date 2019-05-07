#!/usr/bin/env python3

import jenkins, sys, getopt, time, getpass

check = 'tempest-compute-host-check'
cloud = 'production'

def connect_to_server (uri, username, password):
    server = jenkins.Jenkins(uri, username=username, password=password)
    return server

def get_next_build (server, check):
    build_number = server.get_job_info(check)['nextBuildNumber']
    return build_number

def create_build (server, check, params):
    build = server.build_job(check, params)

def get_build_info (server, check, build_number):
    build_info = server.get_build_info(check, build_number)
    return build_info

def main (argv):
    global zone
    try:
        opts, args = getopt.getopt(argv, "u:p:n:s:z:h")
    except getopt.GetoptError:
        print ('usage: %s [-u <username>] [-p <password>] [-n'
        '<fqhn>] [-z <az>]\nUsername and password will be read from stdin'
               ' if not supplied.'%(sys.argv[0]))
    for opt, arg in opts:
        if opt == '-u':
            username = arg
        elif opt == '-p':
            password = arg
        elif opt == '-n':
            host = arg
        elif opt == '-s':
            jenkins_server = arg
        elif opt == '-z':
            zone = arg
        elif opt == '-h':
            print ('usage: %s [-u <username>] [-p <password>] [-n'
            '<fqhn>] [-z <az>]\nUsername and password will be read from stdin'
                   ' if not supplied.'%(sys.argv[0]))
            return 1

    try:
        username
    except NameError:
        username = input('Jenkins username: ')
    try:
        password
    except NameError:
        password = getpass.getpass()

    server = connect_to_server(jenkins_server, username, password)
    build_number = get_next_build(server, check)

    try:
        host
    except NameError:
        params = {'CLOUD': cloud, 'AVAILABILITY_ZONE': zone}
    else:
        params = {'CLOUD': cloud, 'AVAILABILITY_ZONE': zone, 'HOST': host}

    create_build(server, check, params)
    time.sleep(120)
    build_info = get_build_info(server, check, build_number)

    # code.interact(local=dict(globals(), **locals()))
    while build_info['result'] == None:
        time.sleep(20)
        build_info = get_build_info(server, check, build_number)

    if build_info['result'] == 'SUCCESS':
        print ("GREAT SUCCESS!")
        sys.exit(0)
    else:
        print ("An error occured: %s/job/%s/%s/console"%(jenkins_server, check,
                                                         build_number),file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
