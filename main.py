import vk_api
import json
import datetime

datalist = []


current_date = datetime.date.today()
mdk = 57846937

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def default(obj):
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')

def get_data():
    vk_session = vk_api.VkApi('login', 'password',captcha_handler=captcha_handler, app_id=2685278)# при использовании логина и пароля из import auth вылезает капча
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    posts = vk.wall.get(owner_id =-mdk, count = 40)


    with open('posts.json', "w", encoding='utf-8') as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)

def sort_data():
    with open('posts.json', "r", encoding='utf-8') as file:
        data = json.load(file)
        del data['count']
        items = data.get('items')

        for i in items:
            if "is_pinned" not in i:
                date = i.get('date')
                timestamp_date = datetime.datetime.fromtimestamp(date).date()

                likes = i.get('likes').get('count')
                text = i.get('text')
                attachments = i.get('attachments')
                try:
                    for i in attachments:
                        photo = i.get('photo').get("sizes")
                        for i in photo:
                           url = i.get('url')
                except Exception as ex:
                    pass
                if timestamp_date == current_date:
                    datalist.append(
                        {
                            "Ссылка": url,
                            "Текст": text,
                            "Лайки": likes,
                            "Дата": timestamp_date,
                        }
                    )

        sorted_likes_list = sorted(datalist, key=lambda x: x['Лайки'], reverse=True)
        top_likes = sorted_likes_list[:10]


        with open('top_posts.json', "w", encoding='utf-8') as file:
            json.dump(top_likes, file, indent=4, ensure_ascii=False, default=default)


def main():
    get_data()
    sort_data()



if __name__=="__main__":
    main()