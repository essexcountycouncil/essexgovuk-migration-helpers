import csv
import json
from shared.helpers import get_latest_file

image_data = '''{"url":"//images.contentful.com/knkzaf64jx5x/6BMBhzMDYxvH2bkGW3zjmq/a9f8c65cc397149b8fcc60fb01421c06/1280x720_WEB_images11.jpg","details":{"size":233295,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images11.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/6F7Z9A9vHQjukIhPhFeAS4/121db46e048d7959260745ce1d6fc205/1280x720_WEB_images12.jpg","details":{"size":254095,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images12.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/71UQHraqWaJXJUDXIFMnBv/145ae59787f098ee629934a52046c825/1280x720_WEB_images13.jpg","details":{"size":215393,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images13.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/6R5OUfV2EjHHVwlIS8MVBQ/d0ba62d7804894f075c4d659b37a2174/1280x720_WEB_images5.jpg","details":{"size":202781,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images5.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/IwFzNUFkDwwKelTuPwSdV/6a4124aedf1ac472f267fa4184153858/1280x720_WEB_images6.jpg","details":{"size":253162,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images6.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/13IFQFk7UaHR2Jxz1dY5rP/82fc780af6a30a1f62d732a76433d3b3/1280x720_WEB_images10.jpg","details":{"size":259817,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images10.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/3L847NKxfUlxw5i3KUGsVq/34781844eee13aef4c27cbd1689f61d9/1280x720_WEB_images19.jpg","details":{"size":206516,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images19.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/3UuIkUz7x4ROecVxJDwq02/63b677f46117994d013a3d87bafa2a6c/1280x720_WEB_images7.jpg","details":{"size":433502,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images7.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/5pcbpVRiaL9jDV0tHSxuvX/f19d0d411451a4d508b04d30792e9898/1280x720_WEB_images3.jpg","details":{"size":344097,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images3.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/6xVCfL9MJfmrRXGetiSsgA/7faf37bf92de07771b5cb52d99a81180/1280x720_WEB_images4.jpg","details":{"size":234933,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images4.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/1JFSg3scDSu0rUGm88tSP0/23437f3b211189b4059314f9ffd7203d/1280x720_WEB_images25.jpg","details":{"size":284989,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images25.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/13kf5CaGg1wD0IeqdK6968/14797ff0bda3d91a1a665ea2274d1e86/1280x720_WEB_images26.jpg","details":{"size":219135,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images26.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/2NfwXjYvHb53CikxygQash/e4679a464dc155bd8bad8f89a123d3f8/1280x720_WEB_images27.jpg","details":{"size":210620,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images27.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/iku6hISwHIl0vRCOPCUzg/04672e38e2186c9ef3e53305a685cddc/1280x720_WEB_images24.jpg","details":{"size":232050,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images24.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/3JFpJ2avMhDTelf1vndpuO/811c205f2b1d281261c72387999c66a2/1280x720_WEB_images21.jpg","details":{"size":212851,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images21.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/ULKyiDFWfKtB4fQpABzc1/7963efb72c34fdab7e0fd981324bb300/1280x720_WEB_images20.jpg","details":{"size":305032,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images20.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/47lKvm4soXO1UlIcOVbBiq/d36eb69d66beccec08f2c31c6f0aa1e0/1280x720_WEB_images29.jpg","details":{"size":465548,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images29.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/2F0LRyyaaIoiJLYhd4xdaQ/ba725eb5dcf45e07d5d02e03032c8861/1280x720_WEB_images28.jpg","details":{"size":476656,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images28.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/5GRPTe3MjmAT7dE2VsQ6i5/18b24599f16ff7175d4447ebad8fd202/1280x720_WEB_images35.jpg","details":{"size":190127,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images35.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/1S0vO6dGnnhZpV8LBue95u/03e726440d289f4d2012ed50a1abfbcf/1280x720_WEB_images31.jpg","details":{"size":436256,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images31.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/6HnF0Ao2TwoW1mR1RjBihD/db9950ee0b0ddda81783d26e6dae7183/1280x720_WEB_images30.jpg","details":{"size":483171,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images30.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/1vuedT9Eg8siX2GcNX4vmT/0386bd58927e278799a6a428c3b5febc/1280x720_WEB_images33.jpg","details":{"size":254860,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images33.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/Fqnrta0wLzMLh633RUu9j/e0db3902dafacaa11321a24017c63d0c/1280x720_WEB_images34.jpg","details":{"size":328991,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images34.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/VwMwxnA46E00zBMmkcEPY/29c7cba80e7f686e14543b24c00197b7/1280x720_WEB_images17.jpg","details":{"size":204464,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images17.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/2VF5rDGyknyVzE3wGWK6Lg/f89d3e2b3a4ccca63658ad1dd9f980c2/1280x720_WEB_images18.jpg","details":{"size":269004,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images18.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/3JaAq1lbtAbH1IsEk7YO30/61f7337ef22f23d54373cf91d8f595ff/1280x720_WEB_images37.jpg","details":{"size":211278,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images37.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/1nroIMzidpEQaU7W6slhuk/a5664e543a3b4110532303e76c0fcd60/1280x720_WEB_images38.jpg","details":{"size":360416,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images38.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/7xx7VswhIgm0VTBd74CiEM/381232f5cd01f86c7c4a1a43cf3b7b41/1280x720_WEB_images43.jpg","details":{"size":203257,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images43.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/4c7HdKYkq2SCLiLEOCNNeV/4aa9076e890e6a7be5dc5f63010a498a/1280x720_WEB_images42.jpg","details":{"size":244867,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images42.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/4Hb0dUKWUG7nzl7KWNDdgA/84e83b42b948988acb328444e003cdf6/1280x720_WEB_images41.jpg","details":{"size":326885,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images41.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/5FsYJkT4bRHh3at8PsRhr7/f92bf56f8c07c20d72c85022f8aad8a7/1280x720_WEB_images40.jpg","details":{"size":300251,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images40.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/2YQXisl9anwJBaMwo6pO6X/0b6187aa812a0eca5fcda82783faa4b4/1280x720_WEB_images39.jpg","details":{"size":232765,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images39.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/4xYcphToWjAA8C6Lkj1Iex/80220d3d04cf6dd971e58454e859feee/1280x720_WEB_images22.jpg","details":{"size":269982,"image":{"width":1280,"height":720}},"fileName":"1280x720_WEB_images22.jpg","contentType":"image/jpeg"}
{"url":"//images.contentful.com/knkzaf64jx5x/65tITwbQqY3jJVweJzMbIJ/b1b9d6ff97824307643f17a86a715271/NEWS_PROMOTING_essexcoronavirus_1280x720_WEB.jpg","details":{"size":322303,"image":{"width":1280,"height":720}},"fileName":"NEWS_PROMOTING_essexcoronavirus_1280x720_WEB.jpg","contentType":"image/jpeg"}
'''.split()

image_bank_ids = []
for i in image_data:
    j = json.loads(i)
    contentful_id = j['url'].split("/")[4]
    image_bank_ids.append(contentful_id)

with open(get_latest_file("./output", "contentful-export")) as f:
    root = json.load(f)

content_dict = dict()

for x in root['assets']:
    content_dict[x["sys"]["id"]] = x

with open('output/image_bank.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(("URL", "Name", "Alt text"))

    for image_id in image_bank_ids:
        image_dict = content_dict[image_id]['fields']
        try:
            description = image_dict['description']['en-GB']
        except KeyError:
            pass
        url = f"https:{image_dict['file']['en-GB']['url']}"
        name = image_dict['title']['en-GB']
        w.writerow((url, name, description))
