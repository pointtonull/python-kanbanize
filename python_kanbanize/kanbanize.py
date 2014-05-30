#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import csv

from argparse import ArgumentParser

from wrapper import Kanbanize


def get_options():
    argparser = ArgumentParser()

    argparser.add_argument("csvfile", help=("The file with the tasks"),
        nargs='*')

    options = argparser.parse_args()
    return options


def proccess_csv(filepath):
    kanbanize = Kanbanize("5xW5t7vT6ONde4JYT8ekUuvNxh4QX4LXLZzTXjlk")
    reader = csv.DictReader(open(filepath))
    taskdicts = list(reader)

    changed = False
    for taskdict in taskdicts:

        if not taskdict.get("taskid", ""):
            result = kanbanize.create_new_task(**taskdict)
            if "id" in result:
                print "Created new task id:{taskid}.".format(**taskdict)
                taskdict["taskid"] = result["id"]
                changed = True
            else:
                raise ValueError("unexpected error: %s" % str(result))

            if taskdict.get("column", ""):
                result = kanbanize.move_task(**taskdict)
                if result:
                    print "Moved task id:{taskid} to column:{column}.".format(
                        **taskdict)
                else:
                    raise ValueError("unexpected error: %s" % str(result))

        else:
            result = kanbanize.edit_task(**taskdict)
            if result:
                print "Task id:{taskid} edited.".format(**taskdict)
            result = kanbanize.move_task(**taskdict)
            if result:
                print "Task id:{taskid} moved to {column}.".format(**taskdict)


    if changed:
        print "Print updating csv file %s." % filepath
        with open(filepath, "w") as fileobj:
            writer = csv.DictWriter(fileobj, reader.fieldnames)
            writer.writeheader()
            writer.writerows(taskdicts)



def main():
    options = get_options()
    for filepath in options.csvfile:
        proccess_csv(filepath)

if __name__ == "__main__":
    exit(main())
