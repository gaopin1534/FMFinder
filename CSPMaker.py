from xml.etree import ElementTree
# output file
out_file = ""

#check if the relation is solitary
def ifSolitary(relation):
    for feature in relation:
        if(feature.tag=="solitaryFeature"):
            return True
    return False

#making the constraints while parsing the xml recursively
def recursiveXmlParse(elm):
    parent_name = elm.get("name")
    for child in elm:
        relation = child.find("cardinality")
        max_num = relation.get("max")
        min_num = relation.get("min")
        if(ifSolitary(child)):
            feature = child.find("solitaryFeature")
            print parent_name + " " +feature.get("name") + " max:"+max_num+" min:"+ min_num
            if(parent_name != "root"):
                with open(out_file, mode = 'a') as csp:
                    csp.write("(imp (= " + parent_name + " 0 ) (= "+feature.get("name")+" 0))" + "\n")
                    if(int(min_num) == 1):
                        csp.write("(imp (= " + parent_name + " 1 ) (= "+feature.get("name")+" 1))" + "\n")
            else:
                if(max_num == min_num):
                    with open(out_file, mode = 'a') as csp:
                        csp.write("(= " + feature.get("name")+" "+ max_num +")" + "\n")
            recursiveXmlParse(feature)
        else:
            feature_list = ""
            for feature in child:
                if(feature.tag=="cardinality"):
                    continue
                else:
                    if(parent_name != "root"):
                        with open(out_file, mode = 'a') as csp:
                            csp.write("(imp (= " + parent_name + " 0 ) (= "+feature.get("name")+" 0))" + "\n")
                    feature_list += feature.get("name") + " "
                recursiveXmlParse(feature)
            if(parent_name != "root"):
                condition = "(imp (= " + parent_name + " 1) (&&(>= (+ " + feature_list + ") " + min_num + ") ( <= (+ " + feature_list + ")" + max_num +")))"
            else:
                condition = "(&&(>= (+ " + feature_list + ") " + min_num + ") ( <= (+ " + feature_list + ")" + max_num +"))"
            with open(out_file, mode = 'a') as csp:
                csp.write(condition + "\n")

#getting cross-tree constraints
def crossTree(elm):
    for exclude in elm.findall(".//excludes"):
        first = exclude.get("excludes")
        second = exclude.get("feature")
        with open(out_file, mode = 'a') as csp:
            csp.write("(imp (= " + first+ " 1) (= " + second + " 0))\n")
            csp.write("(imp (= " + second+ " 1) (= " + first + " 0))\n")
    for exclude in elm.findall(".//requires"):
        first = exclude.get("feature")
        second = exclude.get("requires")
        with open(out_file, mode = 'a') as csp:
            csp.write("(imp (= " + first+ " 1) (= " + second + " 1))\n")

#target xml file
xml = ""

tree = ElementTree.parse(xml)
title = tree.getroot()
root = title.find("feature")
features = root.findall(".//solitaryFeature")
features.extend(tree.findall(".//groupedFeature"))
with open(out_file, mode = 'a') as csp:
        csp.write("(domain range (0 1))" + "\n")
for feature in features:
    with open(out_file, mode = 'a') as csp:
        csp.write("(int " +feature.get("name") +" range)" + "\n")
recursiveXmlParse(root)
crossTree(tree)