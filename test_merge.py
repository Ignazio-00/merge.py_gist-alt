import unittest

from merge import MergeRequest
import unittest


class TestMergeRequest(unittest.TestCase):
    def setUp(self):
        self.mr = MergeRequest()

    def test_close_approved(self):
        self.mr.vote("Alice", "upvote")
        self.mr.vote("Bob", "upvote")
        self.assertEqual(self.mr.close(), "Merge request has been approved and closed")
        self.assertEqual(self.mr.status(), "closed")

    def test_close_rejected(self):
        self.mr.vote("Alice", "downvote")
        self.mr.vote("Bob", "downvote")
        self.assertEqual(self.mr.close(), "Merge request has been rejected and closed")
        self.assertEqual(self.mr.status(), "closed")

    def test_close_pending(self):
        self.assertEqual(
            self.mr.close(),
            "Cannot close merge request until it has been approved or rejected",
        )
        self.assertEqual(self.mr.status(), "pending")

    def test_getvotes_no_votes(self):
        self.assertEqual(self.mr.getvotes(), "No votes yet")

    def test_getvotes_only_upvotes(self):
        self.mr.vote("Alice", "upvote")
        self.assertEqual(self.mr.getvotes(), "1 upvotes")

    def test_getvotes_only_downvotes(self):
        self.mr.vote("Alice", "downvote")
        self.assertEqual(self.mr.getvotes(), "1 downvotes")

    def test_getvotes_upvotes_and_downvotes(self):
        self.mr.vote("Alice", "upvote")
        self.mr.vote("Bob", "downvote")
        self.assertEqual(self.mr.getvotes(), "1 upvotes, 1 downvotes")

    def test_vote_upvote(self):
        self.assertEqual(self.mr.vote("Alice", "upvote"), None)
        self.assertEqual(self.mr.status(), "pending")
        self.assertEqual(self.mr.vote("Bob", "upvote"), None)
        self.assertEqual(self.mr.status(), "approved")

    def test_vote_downvote(self):
        self.assertEqual(self.mr.vote("Alice", "downvote"), None)
        self.assertEqual(self.mr.status(), "rejected")

    def test_vote_closed(self):
        self.mr.vote("Alice", "upvote")
        self.mr.vote("Bob", "upvote")
        self.mr.close()
        self.assertEqual(
            self.mr.vote("Alice", "upvote"), "can't vote on a closed merge request"
        )

    def test_status_pending(self):
        self.assertEqual(self.mr.status(), "pending")
        self.mr.vote("Alice", "upvote")
        self.assertEqual(self.mr.status(), "pending")
        self.mr.vote("Bob", "downvote")
        self.assertEqual(self.mr.status(), "rejected")

    def test_status_approved(self):
        self.mr.vote("Alice", "upvote")
        self.mr.vote("Bob", "upvote")
        self.assertEqual(self.mr.status(), "approved")

    def test_status_rejected(self):
        self.mr.vote("Alice", "downvote")
        self.mr.vote("Bob", "downvote")
        self.assertEqual(self.mr.status(), "rejected")


if __name__ == "__main__":
    unittest.main()
