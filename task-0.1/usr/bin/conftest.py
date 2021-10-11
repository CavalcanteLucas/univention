from collections import namedtuple

Group = namedtuple('Group', ['gr_name', 'gr_passwd', 'gr_gid', 'gr_mem'])

groupA = Group('groupA', 'x', 1001, ['user1'])
groupB = Group('groupB', 'x', 1002, ['user1', 'user2'])
groupC = Group('groupC', 'x', 1003, ['user2', 'user3'])
groupD = Group('groupD', 'x', 1004, ['user1', 'user2', 'user3'])
groupE = Group('groupE', 'x', 1005, [])

test_dir = '/tmp/tmpdir'

filename1 = f'{test_dir}/file1'
filename2 = f'{test_dir}/file2'
filename3 = f'{test_dir}/file3'

def mock_getgrall():
    return [groupA, groupB, groupC, groupD, groupE]
