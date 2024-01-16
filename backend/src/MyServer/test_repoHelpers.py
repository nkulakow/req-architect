import os
import shutil
import tempfile
import unittest
import git
from unittest.mock import patch, MagicMock
from MyServer.repoHelpers import getReposFromFile, stageChanges, repoName2DirName, getRepoInfo, cloneRepo, pullRepo, checkIfExists, OAuthProvider


class TestRepoHelpers(unittest.TestCase):
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="repo1 https://github.com/user1/repo1.git\nrepo2 https://gitlab.com/user2/repo2.git")
    def test_getReposFromFile(self, mock_open):
        result = getReposFromFile()
        expected_result = {"repo1": "https://github.com/user1/repo1.git", "repo2": "https://gitlab.com/user2/repo2.git"}
        self.assertEqual(result, expected_result)

    def test_stageChanges_successful(self):
        with patch("MyServer.repoHelpers.git.Repo") as mock_repo:
            repo_instance = MagicMock()
            mock_repo.return_value = repo_instance
            repo_instance.remote.return_value = MagicMock()
            result = stageChanges("repo_folder", "commit message", "user_name", "user_email")
            repo_instance.git.add.assert_called_with("repo_folder")
            repo_instance.index.commit.assert_called_with("commit message")
            repo_instance.remote().push.assert_called_once()
            self.assertTrue(result)

    def test_stageChanges_invalid_repo(self):
        with patch("MyServer.repoHelpers.git.Repo", side_effect=git.InvalidGitRepositoryError):
            result = stageChanges("invalid_repo_folder", "commit message", "user_name", "user_email")
            self.assertFalse(result)

    @patch("MyServer.repoHelpers.git.Repo", side_effect=git.NoSuchPathError)
    def test_stageChanges_no_such_path(self, mock_os):
        result = stageChanges("nonexistent_folder", "commit message", "user_name", "user_email")
        self.assertFalse(result)

    @patch("MyServer.repoHelpers.git.Repo", side_effect=OSError)
    def test_stageChanges_os_error(self, mock_os):
        result = stageChanges("repo_folder", "commit message", "user_name", "user_email")
        self.assertFalse(result)

    def test_repoName2DirName(self):
        result = repoName2DirName("user_folder/repo")
        self.assertEqual(result, "user_folder-repo")

    @patch("MyServer.repoHelpers.config") 
    def test_getRepoInfo(self, mock_config):
        mock_config.return_value = "/default/repos/folder"
        request_mock = MagicMock()
        request_mock.GET.get.return_value = "user/repo"
        request_mock.auth.uid = "123"
        request_mock.auth.provider = OAuthProvider.GITHUB
        result = getRepoInfo(request_mock)
        expected_result = ("/default/repos/folder/github/123/user-repo", "user/repo")
        self.assertEqual(result, expected_result)

    @patch("MyServer.repoHelpers.git.Repo.clone_from")
    @patch("os.makedirs")
    def test_cloneRepo_github(self, mock_makedirs, mock_clone_from):
        mock_repo = MagicMock()
        mock_clone_from.return_value = mock_repo
        result = cloneRepo("repo_folder", "repo_url", "token", OAuthProvider.GITHUB)
        self.assertEqual(result, mock_repo)
        mock_clone_from.assert_called_once_with("https://token:@repo_url", "repo_folder")

    @patch("MyServer.repoHelpers.git.Repo.clone_from")
    @patch("os.makedirs")
    def test_cloneRepo_gitlab(self, mock_makedirs, mock_clone_from):
        mock_repo = MagicMock()
        mock_clone_from.return_value = mock_repo
        result = cloneRepo("repo_folder", "repo_url", "token", OAuthProvider.GITLAB)
        self.assertEqual(result, mock_repo)
        mock_clone_from.assert_called_once_with("https://oauth2:token@repo_url.git", "repo_folder")

    @patch("MyServer.repoHelpers.git.Repo")
    def test_pullRepo(self, mock_repo):
        mock_instance = MagicMock()
        mock_repo.return_value = mock_instance
        result = pullRepo("repo_folder", "token")
        mock_instance.remote.assert_called_once()
        mock_instance.remote().pull.assert_called_once()
        self.assertIsNone(result)

    def test_checkIfExists_exists(self):
        with patch("os.path.exists", return_value=True):
            result = checkIfExists("existing_folder")
            self.assertTrue(result)

    def test_checkIfExists_not_exists(self):
        with patch("os.path.exists", return_value=False):
            result = checkIfExists("non_existing_folder")
            self.assertFalse(result)
