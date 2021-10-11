from mock import patch
from parameterized import parameterized
from subprocess import call
import unittest

import conftest
import main


class TestClass(unittest.TestCase):
    @parameterized.expand(
        [
            (
                'groupA',
                ['user1'],
                " [*] Obtained user members of group 'groupA'",
            ),
            (
                'groupB',
                ['user1', 'user2'],
                " [*] Obtained user members of group 'groupB'",
            ),
            (
                'groupC',
                ['user2', 'user3'],
                " [*] Obtained user members of group 'groupC'",
            ),
            (
                'groupD',
                ['user1', 'user2', 'user3'],
                " [*] Obtained user members of group 'groupD'",
            ),
            ('groupE', [], " [*] Obtained user members of group 'groupE'"),
        ]
    )
    @patch('grp.getgrall')
    def test_get_group_members(
        self, groupname, userlist, caplog, mock_getgrall
    ):
        mock_getgrall.return_value = conftest.mock_getgrall()

        with self.assertLogs() as captured:
            group_members = main.get_group_members(groupname)

        self.assertEqual(userlist, group_members)
        self.assertEqual(captured.records[0].getMessage(), caplog)

    @parameterized.expand(
        [
            (
                [conftest.filename1],
                [f" [*] Moved '{conftest.filename1}' to directory 'archive'"],
            ),
            (
                [conftest.filename1, conftest.filename2],
                [
                    f" [*] Moved '{conftest.filename1}' to directory 'archive'",
                    f" [*] Moved '{conftest.filename2}' to directory 'archive'",
                ],
            ),
            (
                [conftest.filename1, conftest.filename2, conftest.filename3],
                [
                    f" [*] Moved '{conftest.filename1}' to directory 'archive'",
                    f" [*] Moved '{conftest.filename2}' to directory 'archive'",
                    f" [*] Moved '{conftest.filename3}' to directory 'archive'",
                ],
            ),
        ]
    )
    def test_move_files(self, files, caplog):
        call('mkdir /tmp/tmpdir', shell=True)
        call(f'touch {conftest.filename1}', shell=True)
        call(f'touch {conftest.filename2}', shell=True)
        call(f'touch {conftest.filename3}', shell=True)

        with self.assertLogs() as captured:
            main.move_files(files)

        for i, log in enumerate(caplog):
            self.assertEqual(captured.records[i].getMessage(), log)

        call('rm -r /tmp/tmpdir', shell=True)

    @parameterized.expand(
        [('user1', " [*] Obtained list of files owned by user 'user1'")]
    )
    def test_get_all_files_owned_by_user(self, username, caplog):
        with self.assertLogs() as captured:
            main.get_all_files_owned_by_user(username)

        self.assertEqual(
            captured.records[0].getMessage(),
            caplog,
        )

    @parameterized.expand(
        [('user1', " [*] Successfully moved all files owned by user 'user1'")]
    )
    @patch('main.get_all_files_owned_by_user')
    @patch('main.move_files')
    def test_move_files_of_an_owner(
        self,
        username,
        caplog,
        mock_get_all_files_owned_by_user,
        mock_move_files,
    ):
        mock_get_all_files_owned_by_user.return_value = []
        mock_move_files.return_value = None
        with self.assertLogs() as captured:
            main.move_files_of_an_owner(username)

        self.assertEqual(
            captured.records[0].getMessage(),
            caplog,
        )


if __name__ == '__main__':
    unittest.main()
