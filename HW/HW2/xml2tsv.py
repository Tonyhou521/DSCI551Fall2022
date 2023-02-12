import pandas as pd
import sys
import lxml
from lxml import etree
import datetime
from collections import defaultdict


def read_xml(user_input_first):
    f = open(user_input_first)
    tree = etree.parse(f)
    return tree

def getChildren(tree,parentID):
    childrenID = []
    for element in tree.xpath("//INodeDirectorySection/directory[parent="+parentID+"]/child/text()"):
            childrenID.append(int(element))
    return childrenID

def getRootDirectoryID(tree):
    ## find the root of the directory
    for element in tree.xpath("//INodeSection/inode[not(name/text())]/id/text()"):
        rootID = str(element)
    return rootID

def get_path(tree,pathID):
    current_path = ''
    pathID = str(pathID)
    tree_search_res = tree.xpath("//INodeSection/inode[id=" +pathID+ "]/name/text()")
    return str(current_path if len(tree_search_res) == 0 else (current_path + tree_search_res[0]))

def build_graph(tree,graph,node):
    visited = []
    stack = []

    visited.append(node)
    stack.append(node) 

    while stack:
        s = stack.pop()    
        graph[str(s)] = getChildren(tree,str(s))
        # reverse iterate through edge list so results match recursive version
        for n in reversed(graph[str(s)]):
            if n not in visited:
                visited.append(n)
                stack.append(n)
    return graph

def build_results(graph, tree, starting_point, res):
    visited = []
    stack = []
    visited.append(starting_point)
    stack.append((starting_point, '/'))
    res.append(('/',str(starting_point)))
    while stack:
        s = stack.pop()
        for n in reversed(graph[str(s[0])]):
            if n not in visited:
                correct_child = s[1] + '/' + get_path(tree, n) if s[1] != '/' else s[1] + get_path(tree, n)
                visited.append(n)
                stack.append((n, correct_child))
                res.append((correct_child, str(n)))

def get_perms(octal, file_type):
    result = "" if file_type == "DIRECTORY" else "-"
    value_letters = [(4,"r"),(2,"w"),(1,"x")]
    # Iterate over each of the digits in octal
    for digit in [int(n) for n in str(octal)]:
        # Check for each of the permissions values
        for value, letter in value_letters:
            if digit >= value:
                result += letter
                digit -= value
            else:
                result += '-'
    return 'd' + result[3:] if file_type == "DIRECTORY" else result[3:]

def main():
    res = []
    user_input_first = sys.argv[1]
    user_input_foroutput = sys.argv[2]
    
    xml_import = read_xml(user_input_first)
    tree = read_xml(user_input_first)

    startingDir_ID = getRootDirectoryID(tree)
    graph = {str(startingDir_ID): startingDir_ID}
    
    build_graph(tree,graph,startingDir_ID)
    build_results(graph=graph, tree=tree,starting_point=str(startingDir_ID), res=res)

    lookupTable = {}

    for r in res:
        lookupTable[r[1]] = r[0]

    # Given res
    def getInodeInfo(tree):
        all_inodes = []
        for element in tree.xpath("//INodeSection/inode"):
            inode_info = {}
            id = element.find('id').text
            mtime = element.find('mtime').text
            file_type = element.find('type').text
            permission = element.find('permission').text
            permission = get_perms(permission[-4:], file_type)
            num_blocks = 0
            filesize = 0
            if file_type == "FILE":
                blocks_el = element.find('blocks')
                blocks_list = blocks_el.xpath(".//block")
                num_blocks = len(blocks_list)
                for block_el in blocks_list:
                    filesize += int(block_el.find('numBytes').text)

            inode_info['Path'] = lookupTable[(id)]
            inode_info['ModificationTime'] = datetime.datetime.utcfromtimestamp(int(mtime)/1000).strftime("%m/%d/%Y %H:%M")
            inode_info['BlocksCount'] = num_blocks
            inode_info['FileSize'] = filesize
            inode_info['Permission'] = permission
            all_inodes.append(inode_info)
        return all_inodes

    tsv_temp = getInodeInfo(tree)
    tsv_temp = pd.DataFrame(tsv_temp)
    tsv_temp.to_csv(user_input_foroutput, sep='\t', index=False)




if __name__ == "__main__":
    main()