import pytest

def test_profile_str(profile):
    """test for profile model str represantation"""
    assert profile.__str__() == f"{profile.user.username}'s profile"


