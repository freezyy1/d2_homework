from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment

# Пользователи
user_sergey = User.objects.create_user('Сергей', 'sergey@gmail.com', 'Sergey1233password')
user_sergey.save()
user_matvey = User.objects.create_user('Матвей', 'matwey@gmail.com', 'Matveypassword7763482')
user_matvey.save()

# Авторы
sergey = Author.objects.create(author='sergey', one_to_one_rel=user_sergey)
matvey = Author.objects.create(author='matvey', one_to_one_rel=user_matvey)

# Категории
films = Category.objects.create(category='Фильмы')
reviews = Category.objects.create(category='Обзоры')
it = Category.objects.create(category='IT')
online_stores = Category.objects.create(category='Интернет магазины')
food = Category.objects.create(category='Готовка еды')

# 2 поста и 1 новость
post1 = Post(post_name='Обзор на фильм \"стражи галактики\"', content='Классный фильм', one_to_many_rel=sergey)
post1.st_or_new = "ST"
post1.many_to_many_rel.add(films, reviews)
post1.save()

post2 = Post.objects.create(post_name='Создание сайта на react', content='Скачайте node js...', one_to_many_rel=matvey)
post2.st_or_new = "ST"
post2.many_to_many_rel.add(it, online_stores)
post2.save()

new1 = Post.objects.create(post_name='Придуман новый рецепт чизкейка',
                           content='Покупайте рецепт чизкейка по ссылке снизу', one_to_many_rel=matvey)
new1.many_to_many_rel.add(food, online_stores)
new1.st_or_new = "NE"
new1.save()

# 4 комментария
comm1 = Comment.objects.create(comment='Я уже видел этот рецепт', one2many_post=new1, one2many_user=user_sergey)
comm2 = Comment.objects.create(comment='Не переходите по ссылке снизу, я обнаружил там вирус', one2many_post=new1,
                               one2many_user=user_sergey)
comm3 = Comment.objects.create(comment='Информативно', one2many_post=post1, one2many_user=user_matvey)
comm4 = Comment.objects.create(comment='Спасибо за информацию', one2many_post=post2, one2many_user=user_sergey)

# Дислайки и лайки под постами, новостями и комментариями
comm1.like()
comm1.like()
comm1.like()
comm1.like()
comm1.like()
comm1.dislike()
comm1.dislike()
comm1.save()

comm2.like()
comm2.like()
comm2.dislike()
comm2.like()
comm2.like()
comm2.save()

comm3.like()
comm3.dislike()
comm3.like()
comm3.like()
comm3.dislike()
comm3.save()

comm4.like()
comm4.dislike()
comm4.like()
comm4.like()
comm4.dislike()
comm4.save()

post1.like()
post1.like()
post1.dislike()
post1.like()
post1.like()
post1.save()

post2.like()
post2.like()
post2.save()

new1.like()
new1.like()
new1.like()
new1.dislike()
new1.dislike()
new1.like()
new1.like()
new1.dislike()
new1.save()

# Обновление рейтингов
sergey.update_rating()
sergey.rating_auth
matvey.update_rating()
matvey.rating_auth

# Лучший пользователь
best = Author.objects.all().order_by('-rating_auth')[0]
best_user = best.one_to_one_rel
print(best_user.username, best.rating_auth)

# Лучшая статья
best_st = Post.objects.all().order_by('-rating_post')[0]
print('Лучшая статья:' + best_st.post_name)
print('Дата создания: ' + str(best_st.created))
print('Пользователь: ' + str(best_st.one_to_many_rel.one_to_one_rel))
print('Рейтинг: ' + str(best_st.rating_post))
print('Превью: ' + best_st.preview())

# Вывод комментария
print('Комментарии:')
comms = best_st.comment_set.all()
for i in comms:
    print(i.created_comm, i.one2many_user, i.rating_comm, i.comment)
