from enum import Enum

class MergeStatus:
    OPEN = "open"
    PENDING = "pending"
    REJECTED = "rejected"
    APPROVED = "approved"
    CLOSED = "closed"

class MergeRequest:
    """
    Represents a merge request that can be voted on by users.

    The `MergeRequest` object keeps track of the number of upvotes and downvotes
    for the merge request, as well as its status (open or closed).

    Attributes:
        _context (dict): A dictionary that stores the number of upvotes and downvotes
            for the merge request.
        _status (str): A string that represents the status of the merge request.

    Methods:
        status(): Returns the status of the merge request based on the number of
            upvotes and downvotes.
        vote(by_user, type): Records a vote by a user (either an upvote or downvote)
            for the merge request.
    """

    def __init__(self):
        self._context = {"upvotes": set(), "downvotes": set()}
        self._status = MergeStatus.OPEN

    def status(self):
        if self._status == MergeStatus.CLOSED:
            return self._status
        if self._context["downvotes"]:
            self._status = MergeStatus.REJECTED
        elif len(self._context["upvotes"]) >= 2:
            self._status = MergeStatus.APPROVED
        else:
            self._status = MergeStatus.PENDING
        return self._status

    def remove_users_previous_votes(self, voting_user):
        self._context["upvotes"].discard(voting_user)
        self._context["downvotes"].discard(voting_user)
        
    
    def vote(self, voting_user, vote_type):
        if self._status == MergeStatus.CLOSED:
            return "can't vote on a closed merge request"
        
        self.remove_users_previous_votes(voting_user)
        
        if vote_type == "downvote":
            self._context["downvotes"].add(voting_user)
        elif vote_type == "upvote":
            self._context["upvotes"].add(voting_user)
        else:
            return "not correct type"

    def close(self):
        if self.status() == MergeStatus.APPROVED:
            self._status = MergeStatus.CLOSED
            return "Merge request has been approved and closed"
        elif self.status() == MergeStatus.REJECTED:
            self._status = MergeStatus.CLOSED
            return "Merge request has been rejected and closed"
        else:
            return "Cannot close merge request until it has been approved or rejected"

    def getvotes(self):
        upvotes = len(self._context["upvotes"])
        downvotes = len(self._context["downvotes"])
        if upvotes == 0 and downvotes == 0:
            return "No votes yet"
        elif upvotes == 0:
            return f"{downvotes} downvotes"
        elif downvotes == 0:
            return f"{upvotes} upvotes"
        else:
            return f"{upvotes} upvotes, {downvotes} downvotes"
