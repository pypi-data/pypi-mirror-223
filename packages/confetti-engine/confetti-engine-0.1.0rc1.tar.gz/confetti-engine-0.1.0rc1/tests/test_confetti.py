from confetti_engine.confetti import Datastore


def test_datastore():
    # Declaring datastore
    data = Datastore(file="Testing.json")

    # Prepping for data saving then save
    data.prep("Eggs", "Spam")
    data.save()

    #  Test returned value
    loaded = data.load()
    assert loaded.get("Eggs") == "Spam"
