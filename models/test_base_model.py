def test_save():
    try:
        bm = BaseModel()
        old_updated_at = bm.updated_at
        bm.save()
        new_updated_at = bm.updated_at
        assert new_updated_at > old_updated_at
        print("OK")
    except Exception as e:
        print("Failed:", e)

def test_to_dict():
    try:
        bm = BaseModel()
        d = bm.to_dict()
        assert type(d) is dict
        assert "__class__" in d
        assert type(d["created_at"]) is str
        print("OK")
    except Exception as e:
        print("Failed:", e)

# Call tests
test_save()
test_to_dict()
