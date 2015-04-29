
# coding: utf-8

# A collection of functions

# In[2]:




# In[3]:

# create a network given a directory
# this can be added to a previous network if provided
# network architecture: {user_name1 : {user_name2 : set(messages between) } }
def extract_network(directory, current_network = dict()):
    
    # new network
    network = current_network
    
    # import XML parser
    import xml.etree.ElementTree as ET
    
    import os

    # walk directory
    for dir_name, subdir_list, file_list in os.walk(directory):

        print "working in " + dir_name

        for file_name in file_list:
            # open file
            if ("Thread" in file_name) and (".xml" in file_name):
    #             print "working on " + dir_name + '/' + file_name

                # parse the file
                tree = ET.parse(dir_name + '/' + file_name)
                root = tree.getroot()

                # depth first traversal 
                for elem in root.iter():
                    # is this a node with comments?
                    comments = elem.find('Comments')
                    if comments != None:
                        # if it is it should have a poster
                        poster = elem.find('user').text.strip()
                        # find the name of users that replied
                        for comment in comments.findall('Comment'):
                            commenter = comment.find('user').text.strip()
                            comment_text = comment.find('body').text
                            if comment_text == None:
                                #if somehow the comment has no body, exit this loop
                                break

                            #save these in the dictionary
                            if poster not in network:
                                # first time seing this user as poster. add him
                                network[poster] = {commenter: set([comment_text.strip()]) }
                            else:
                                if commenter not in network[poster]:
                                    # first time this commenter is commenting on this user 
                                    network[poster][commenter] = set([comment_text.strip()])
                                else:
                                    # add text to existing list
                                    network[poster][commenter] = network[poster][commenter] | set([comment_text.strip()])
    return network


# In[4]:

#symmetrizse a given network
def symmetrize_network(network):
    # given a network of the form {user_name1 : {user_name2 : {relationship features} } }
    # returns a symmetrical version of that network

    import copy
    sym_network = copy.deepcopy(network)

    #go through network
    for user_A in network.keys():
        for user_B in network[user_A].keys():
            msgs = network[user_A][user_B]

            if user_B not in sym_network:
                sym_network[user_B] = {user_A:msgs}
            elif user_A not in sym_network[user_B]:
                sym_network[user_B][user_A] =  msgs
            else:
                sym_network[user_B][user_A] = sym_network[user_B][user_A] | msgs


    return sym_network


# In[ ]:



