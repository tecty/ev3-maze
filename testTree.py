#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from treelib import Tree, Node
tree = Tree()
tree.create_node("Harry", "harry",data = [90, 200])
tree.create_node("Jane", "jane", parent="harry",data = {big:180, small:150})
tree.create_node("Jane1", "jane1", parent="harry", data = {big:90, small:200})
tree.show(data_property="")
