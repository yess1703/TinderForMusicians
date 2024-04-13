import asyncio

from core.database import partner_collection, users_collection


def jaccard_similarity(set1: set, set2: set):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else False


async def recommend_user(user_id: int):
    user_preferences = await partner_collection.find_one({"_id": user_id})
    cursor = users_collection.find(
        {
            "_id": {"$ne": user_id},
            "age_group": user_preferences["age_group"],
            "gender": user_preferences["gender"],
            "location": user_preferences["location"],
        }
    )
    preference_set = set(user_preferences["musicians"])
    recommendations = []
    async for document in cursor:
        document_set = set(document["musicians"])
        similarity = jaccard_similarity(preference_set, document_set)
        if similarity != 0:
            recommendations.append((document, similarity))
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    return recommendations


# user_data_1 = {"age": 28, "gender": "М", "musicians": ["Гобоист"]}
#
#
# async def main():
#     result = await recommend_user(user_data_1)
#     print(result)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
