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
        self._status = "open"

    def status(self):
        if self._status == "closed":
            return self._status
        else:
            if self._context["downvotes"]:
                return "rejected"
            else:
                if len(self._context["upvotes"]) >= 2:
                    return "approved"
                else:
                    return "pending"
        return None

    def vote(self, by_user, type):
        if self._status == "closed":
            return "can't vote on a closed merge request"

        if type == "downvote":
            self._context["upvotes"].discard(by_user)
            self._context["downvotes"].add(by_user)
        elif type == "upvote":
            self._context["downvotes"].discard(by_user)
            self._context["upvotes"].add(by_user)
        else:
            return "not correct type"

    def close(self):
        if self.status() == "approved":
            self._status = "closed"
            return "Merge request has been approved and closed"
        elif self.status() == "rejected":
            self._status = "closed"
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
