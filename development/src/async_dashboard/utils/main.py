import os
import sys
import asyncio
import aiohttp

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
)
sys.path.append(project_root)

from development.src.async_dashboard.configurations.conf import config


async def user_service(url, id, session):
    user_service_url = f"{url}/users/{id}"
    print(user_service_url)
    async with session.get(user_service_url) as response:
        if response.status == 200:
            user_data = await response.json()
            return {
                "id": user_data.get("id"),
                "name": user_data.get("name"),
                "email": user_data.get("email")
            }
        else:
            print(f"Failed to fetch data for user {id}. Status code: {response.status}")
            return None


async def post_service(url, id, session):
    post_service_url = f"{url}/posts/{id}"
    print(post_service_url)
    async with session.get(post_service_url) as response:
        if response.status == 200:
            post_data = await response.json()
            return {
                "id": post_data.get("id"),
                "title": post_data.get("title"),
                "body": post_data.get("body")
            }
        else:
            print(f"Failed to fetch data for post {id}. Status code: {response.status}")
            return None


async def albums_service(url, id, session):
    albums_service_url = f"{url}/albums/{id}"
    print(albums_service_url)
    async with session.get(albums_service_url) as response:
        if response.status == 200:
            albums_data = await response.json()
            return {
                "id": albums_data.get("id"),
                "title": albums_data.get("title"),
                "userId": albums_data.get("userId")
            }
        else:
            print(f"Failed to fetch data for album {id}. Status code: {response.status}")
            return None


async def photos_service(url, id, session):
    photos_service_url = f"{url}/photos/{id}"
    print(photos_service_url)
    async with session.get(photos_service_url) as response:
        if response.status == 200:
            photos_data = await response.json()
            return {
                "albumId": photos_data.get("albumId"),
                "id": photos_data.get("id"),
                "title": photos_data.get("title"),
                "url": photos_data.get("url"),
                "thumbnailUrl": photos_data.get("thumbnailUrl")
            }
        else:
            print(f"Failed to fetch data for photo {id}. Status code: {response.status}")
            return None


async def dashboard(url):
    async with aiohttp.ClientSession() as session:
        user_data, post_data, albums_data, photos_data = await asyncio.gather(
            user_service(url, 1, session),
            post_service(url, 1, session),
            albums_service(url, 1, session),
            photos_service(url, 1, session)
        )

    dashboard_data = {
        "user": user_data,
        "post": post_data,
        "album": albums_data,
        "photo": photos_data
    }
    print(dashboard_data)  # <-- Added print so you see the result
    return dashboard_data


if __name__ == "__main__":
    conf = config()
    print(conf.url)

    try:
        asyncio.run(dashboard(conf.url))
    except aiohttp.ClientError as e:
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
