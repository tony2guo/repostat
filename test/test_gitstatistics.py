import unittest
import datetime
from tools.gitstatistics import CommitDictFactory
from tools.gitstatistics import AuthorDictFactory

class TestCommitDictFactory(unittest.TestCase):
	
	def setUp(self):
		pass

	def testCreateCommitAuthorName(self):
		commit = CommitDictFactory.create_commit('Test Author', 1, 2, '2019.03.15', datetime.datetime.now().timestamp())
		self.assertEqual(commit[CommitDictFactory.AUTHOR_NAME], 'Test Author')
		self.assertEqual(commit[CommitDictFactory.AUTHOR_NAME], CommitDictFactory.getAuthor(commit))

	def testCreateCommitLinesAdded(self):
		commit = CommitDictFactory.create_commit('Test Author', 1, 2, '2019.03.15', datetime.datetime.now().timestamp())
		self.assertEqual(commit[CommitDictFactory.LINES_ADDED], 1)
		self.assertEqual(commit[CommitDictFactory.LINES_ADDED], CommitDictFactory.getLinesAdded(commit))

	def testCreateCommitLinesRemoved(self):
		commit = CommitDictFactory.create_commit('Test Author', 1, 2, '2019.03.15', datetime.datetime.now().timestamp())
		self.assertEqual(commit[CommitDictFactory.LINES_REMOVED], 2)
		self.assertEqual(commit[CommitDictFactory.LINES_REMOVED], CommitDictFactory.getLinesRemoved(commit))

	def testCreateCommitTimeStamp(self):
		ts = datetime.datetime.now().timestamp()
		commit = CommitDictFactory.create_commit('Test Author', 1, 2, '2019.03.15', ts)
		self.assertEqual(commit[CommitDictFactory.TIMESTAMP], ts)
		self.assertEqual(commit[CommitDictFactory.TIMESTAMP], CommitDictFactory.getTimeStamp(commit))

class TestAuthorDictFactory(unittest.TestCase):
	testData = {}

	def setUp(self):
		firstCommit: datetime = datetime.datetime.strptime('2019-01-01', '%Y-%m-%d')
		lastCommit = datetime.datetime.strptime('2019-03-15', '%Y-%m-%d')		
		self.testData['basic'] = {
			'first_commit_ts': firstCommit.timestamp(),
			'last_commit_ts': lastCommit.timestamp(),
			'author_name': 'Test Author',
			'active_days': '2015-03-01',
			'lines_added': 1000,
			'lines_removed': 100,
			'commits': 50}
			

	def createTestAuthor(self, data):
		return AuthorDictFactory.create_author(data['author_name'], data['lines_removed'], data['lines_added'], data['active_days'], data['commits'], data['first_commit_ts'], data['last_commit_ts'])

	def getTestAuthor(self):
		return self.createTestAuthor(self.testData['basic'])

	def testAuthorCreateDict(self):
		author = self.getTestAuthor()
		activeDays = author[AuthorDictFactory.ACTIVE_DAYS]
		self.assertTrue(activeDays.__len__() == 1)
		self.assertTrue('2015-03-01' in activeDays)
		self.assertEqual(author[AuthorDictFactory.AUTHOR_NAME], self.testData['basic']['author_name'])
		self.assertEqual(author[AuthorDictFactory.COMMITS], self.testData['basic']['commits'])
		self.assertEqual(author[AuthorDictFactory.FIRST_COMMIT], self.testData['basic']['first_commit_ts'])
		self.assertEqual(author[AuthorDictFactory.LAST_COMMIT], self.testData['basic']['last_commit_ts'])
		self.assertEqual(author[AuthorDictFactory.LINES_ADDED], self.testData['basic']['lines_added'])
		self.assertEqual(author[AuthorDictFactory.LINES_REMOVED], self.testData['basic']['lines_removed'])


	def testAuthorAddActiveDay(self):
		author = self.getTestAuthor()
		activeDays = author[AuthorDictFactory.ACTIVE_DAYS]
		dayCount = activeDays.__len__()
		AuthorDictFactory.addActiveDay(author, '2000.01.01')
		self.assertEqual(author[AuthorDictFactory.ACTIVE_DAYS].__len__(), dayCount+1)
		self.assertTrue('2000.01.01' in author[AuthorDictFactory.ACTIVE_DAYS])

	def testAuthorLinesAdd(self):
		author = self.getTestAuthor()
		init = author[AuthorDictFactory.LINES_ADDED]
		AuthorDictFactory.addLinesAdded(author, 10)
		self.assertEqual(author[AuthorDictFactory.LINES_ADDED], init + 10)

	def testAuthorLinesRemoved(self):
		author = self.getTestAuthor()
		init = author[AuthorDictFactory.LINES_REMOVED]
		AuthorDictFactory.addLinesRemoved(author, 13)
		self.assertEqual(author[AuthorDictFactory.LINES_REMOVED], init + 13)

	def testAuthorLinesCommit(self):
		author = self.getTestAuthor()
		init = author[AuthorDictFactory.COMMITS]
		AuthorDictFactory.addCommit(author, 10)
		self.assertEqual(author[AuthorDictFactory.COMMITS], init + 10)

	def testAuthorCheckFirstCommit(self):
		author = self.getTestAuthor()
		init = author[AuthorDictFactory.FIRST_COMMIT]
		
		# expected: first_commit not change
		AuthorDictFactory.checkFirstCommitStamp(author, init + 1000)
		self.assertEqual(author[AuthorDictFactory.FIRST_COMMIT], init)

		# expected: first_commit change to the earlier timestamp
		AuthorDictFactory.checkFirstCommitStamp(author, init - 1000)
		self.assertEqual(author[AuthorDictFactory.FIRST_COMMIT], init - 1000)
		
	def testAuthorLastCommit(self):
		author = self.getTestAuthor()
		init = author[AuthorDictFactory.LAST_COMMIT]
		lastCommit_after = datetime.datetime.strptime('2019-03-20', '%Y-%m-%d')
		lastCommit_before = datetime.datetime.strptime('2019-03-10', '%Y-%m-%d')

		# expected: first_commit not change
		AuthorDictFactory.checkLastCommitStamp(author, lastCommit_before.timestamp())
		self.assertEqual(author[AuthorDictFactory.LAST_COMMIT], init)

		# expected: first_commit change to the earlier timestamp
		AuthorDictFactory.checkLastCommitStamp(author, lastCommit_after.timestamp())
		self.assertEqual(author[AuthorDictFactory.LAST_COMMIT], lastCommit_after.timestamp())
		self.assertEqual(author[AuthorDictFactory.LAST_ACTIVE_DAY], '2019-03-20')





if __name__ == '__main__':
	unittest.main()