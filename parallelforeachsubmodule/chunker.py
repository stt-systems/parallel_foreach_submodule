# -*- coding: utf-8 -*-


def split_load(list_submodules, chunks):
    list_submodules_list = list()
    num_jobs = 0
    while num_jobs < chunks:
        list_submodules_list.append(list())
        num_jobs += 1

    i = 0
    for submodule in list_submodules:
        list_submodules_list[i % num_jobs].append(submodule)
        i += 1
    return list_submodules_list
