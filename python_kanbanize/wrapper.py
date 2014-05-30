from requests import Session
import json
import logging

class Kanbanize(Session):
    """ Specialized version of restkit.Resource to deal with kanbanize.com APIs

        :param apikey: Your kanbanize.com API key
        :type apikey: str

    """

    def __init__(self, apikey, **kwargs):
        self.apikey = apikey
        super(Kanbanize, self).__init__(**kwargs)


    def request(self, method, url=None, data=None, headers=None, **kwargs):
        URI = 'http://kanbanize.com/index.php/api/kanbanize'
        url = '%s%s/format/json' % (URI, url)
        headers = { 'apikey': self.apikey, 'content-type': 'application/json' }

        logging.debug('Kanbanize.request:%s - %s - %s' % (url, data, "json"))

        return super(Kanbanize, self).request(
            method,
            url=url,
            data=data,
            headers=headers,
            **kwargs
        )


    def get_all_tasks(self, boardid):
        """
        Retireves a list of all tasks on 'boardid' board

        :param boardid: Board number to retrieve tasks from
        :type boardid: int

        Example::

            >>> from kanbanize.wrapper import Kanbanize
            >>> from credentials import *

            >>> k = Kanbanize(apikey)
            >>> k.get_all_tasks(5)
            [{u'columnname': u'backlogr, u'blockedreason': None, u'lanename':
            u'Default Swimlane', u'subtaskdetails': [], u'subtasks': None,
            u'title': u'Task title', u'color': u'#F0F0F0', u'tags': u'',
            u'priority': u'Average', u'assignee': u'None', u'deadline': None,
            u'taskid': u'38', u'subtaskscomplete': None, u'extlink': u'',
            u'blocked': None, u'type': u'0', u'leadtime': 1, u'size': u'2'},
            {u'columnname': u'Backlog', u'blockedreason': None, u'lanename':
            u'Default Swimlane', u'subtaskdetails': [], u'subtasks': u'0',
            u'title': u'Kanbanize test task 01', u'color': u'#99b399', u'tags':
            None, u'priority': u'Average', u'assignee': u'None', u'deadline':
            None, u'taskid': u'27', u'subtaskscomplete': u'0', u'extlink':
            None, u'blocked': u'0', u'type': u'0', u'leadtime': 15, u'size':
            u'2'}, {u'columnname': u'Backlog', u'blockedreason': None,
            u'lanename': u'Default Swimlane', u'subtaskdetails': [],
            u'subtasks': u'0', u'title': u'Kanbanize test task 02', u'color':
            u'#99b399', u'tags': None, u'priority': u'Average', u'assignee':
            u'None', u'deadline': None, u'taskid': u'28', u'subtaskscomplete':
            u'0', u'extlink': None, u'blocked': u'0', u'type': u'0',
            u'leadtime': 15, u'size': u'2'}]

        """
        response = self.post('/get_all_tasks/boardid/%s' % boardid)
        return response.json()


    def get_task_details(self, boardid, taskid):
        """
        Retireves 'taskid' task details from 'boardid' board

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param taskid: Id of the task to retrieve details from
        :type taskid: int

        """
        response = self.post('/get_task_details/boardid/%s/taskid/%s' %
            (boardid, taskid))
        return response.json()


    def create_new_task(self, boardid, **kwargs):
        """
        Creates a new task in 'boardid' board with optional 'details'

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param kwargs: Task details
        :type kwargs: recognized params are:
            title	Title of the task
            description	Description of the task
            priority	One of the following: Low, Average, High
            assignee	Username of the assignee (must be a valid username)
            color	Any color code (e.g. "34a97b")
            size	Size of the task
            tags	Space separated list of tags
            deadline	Dedline in the format: yyyy-mm-dd (e.g. "2011-12-13")
            extlink	A link ("http://google.com")
            type	The name of the type you want to set.
            template	The name of the template you want to set.
        :rtype: xml
        """

        kwargs['boardid'] = boardid
        params = json.dumps(kwargs)
        logging.debug('create_new_task:%s' % params)
        response = self.post('/create_new_task/', data=params)
        return response.json()


    def delete_task(self, boardid, taskid):
        """
        Deletes the task identified withe 'boardid' and 'taskid'.

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param taskid: Task number to delete
        :type boardid: int
        :rtype: xml
        """

        kwargs = {}
        kwargs['boardid'] = boardid
        kwargs['taskid'] = taskid
        params = json.dumps(kwargs)
        logging.debug('delete_task:%d/%d' % (boardid, taskid))
        response = self.post('/delete_task/', data=params)
        return response.json()


    def edit_task(self, boardid, taskid, **kwargs):
        """
        Edit a task in 'boardid' board with provided 'details'

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param kwargs: New task details
        :type kwargs: recognized params are:
            title	New title of the task
            description	New description of the task
            priority	New priority, can be: "Low", "Average" or "High"
            assignee	New assigned username (must be a valid username)
            color	Code of the new color (e.g. "34a97b")
            size	New size of the task
            tags	Space separated list of tags (e.g. "demo security")
            deadline	New dedline in format: yyyy-mm-dd (e.g. "2011-12-13")
            extlink	A new link.
            type	New name of the type.

            If one parameter is not especified will left unchanged.
        :rtype: json
        """

        kwargs['boardid'] = boardid
        kwargs['taskid'] = taskid
        params = json.dumps(kwargs)
        logging.debug('edit_task:%s' % params)
        response = self.post('/edit_task/', data=params)
        return response.json()


    def move_task(self, boardid, taskid, column, **kwargs):
        """
        With this action you can move tasks on the board by specifying the
        column name and optionally the swim-lane name.

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param taskdid: task number
        :type taskid: int
        :param column: column name
        :type taskid: string
        :param details: Another options
        :type details: dict with this optional parameters:
            lane	The name of the swim-lane to move the task into.
            position	The position of the task in the new column (zero-based).
            exceedingreason	If you can exceed a limit with a reason, supply
                it with this parameter.
        :rtype: xml
        """

        kwargs['boardid'] = boardid
        kwargs['taskid'] = taskid
        kwargs['column'] = column
        params = json.dumps(kwargs)
        logging.debug('move_task:%s' % params)
        response = self.post('/move_task/', data=params)
        return response.json()


if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    k = Kanbanize("5xW5t7vT6ONde4JYT8ekUuvNxh4QX4LXLZzTXjlk")
    print k.create_new_task(2, {})
