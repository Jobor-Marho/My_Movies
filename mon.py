# import requests
#
# MY_MOVIEDB_API_KEY = "a819076edfe7d3ad539ddbf630d0b37a"
# MOVIEDB_LINK = "https://api.themoviedb.org/3/movie/353486"
# link = "https://api.themoviedb.org/3/movie/353486/images/pIjv57padPCmbWm08U8FtJUX7Qn.jpg"
# PARAMS = {
#     "api_key": MY_MOVIEDB_API_KEY
#
# }
# HEADERS = {
#     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhODE5MDc2ZWRmZTdkM2FkNTM5ZGRiZjYzMGQwYjM3YSIsInN1YiI6IjYzZ'
#                      'jc1ZjZhNjhiMWVhMDA4MmY2MGY1YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mwpI4iZQVj8ZRjxT90l'
#                      '1LiYCzBvrEISzHoKAm87LRtk',
#     'Content-Type': 'application/json;charset=utf-8'
# }
# try:
#     response = requests.get(url=MOVIEDB_LINK, headers=HEADERS)
#     data = response.json()
# except requests.exceptions.ConnectionError:
#     print("No Internet Access")
# else:
#     for key in data:
#         print(key)
#     # print(data['results'][0])
#     # title = data['results'][0]['original_title']
#     # date = data['results'][0]['release_date']
#     # movie = f"{title} - {date}"
#     # print(movie)
#     print(data)

day = [7.3, 1.2, 7.3, 1.2]
day.sort(reverse=True)
print(day)