from app.database.mongodb import database


class UserRepository:

    def __init__(self):
        self.collection = database["users"]

    def get_user_by_email(self, email: str) -> dict | None:
        """
        Returns a user by email.
        """
        user = self.collection.find_one(
            {"email": email.lower()},            
        )
        if user is None:
           return None

        user["id"] = str(user["_id"])
        del user["_id"]

        return user

    def create_user(self, user: dict) -> dict:
        """
        Creates a new user.
        """
        result = self.collection.insert_one(user)

        created_user = self.collection.find_one(
            {"_id": result.inserted_id}
        )

        created_user["id"] = str(created_user["_id"])
        del created_user["_id"]

        return created_user

    def get_user_by_id(self, user_id: str) -> dict | None:
        """
        Returns a user by their ID.
        """
        from bson import ObjectId

        try:
            object_id = ObjectId(user_id)
        except Exception:
            return None

        user = self.collection.find_one(
            {"_id": object_id}
        )

        if user is None:
            return None

        user["id"] = str(user["_id"])
        del user["_id"]

        return user

user_repository = UserRepository()    