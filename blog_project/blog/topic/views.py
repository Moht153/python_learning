import html
import json

from django.http import JsonResponse
from django.shortcuts import render
from tools.login_check import login_check, get_user_by_request
from topic.models import Topic
from user.models import UserProfile
from message.models import Message


# Create your views here.
@login_check('POST', 'DELETE')
def topics(request, username):
	# 127.0.0.1:8000/v1/topics/<username>?category=[tec|no-tec]
	if request.method == 'GET':
		# 获取用户博客数据
		# http://127.0.0.1:5000/<username>/topics
		# username 被访问的博客的博主用户名
		# vistor 访客{1.登陆了 2. 游客（未登陆）}

		# 根据username查询博主
		users = UserProfile.objects.filter(username=username)
		if not users:
			result = {'code': 301, 'error': 'no author: %s' % username}
			return JsonResponse(result)
		# 取出结果中的博主
		user = users[0]

		# visitor?
		visitor = get_user_by_request(request)
		visitor_name = None
		if visitor:
			visitor_name = visitor.username

		# 127.0.0.1:8000/v1/topics/<username>?t_id
		# 获取t_id
		t_id = request.GET.get('t_id')
		if t_id:
			# 当前是否为博主在访问自己的博客
			is_self = False
			# 根据t_id 进行查询
			t_id = int(t_id)  # str类型转换为int
			# 博主在访问自己的博客
			if username == visitor_name:
				is_self = True
				topic = Topic.objects.filter(id=t_id)[0]
				if not topic:
					result = {'code': 312, 'error': 'no topic'}
					return JsonResponse(result)
			else:
				topic = Topic.objects.filter(id=t_id, limit='public')[0]
				if not topic:
					result = {'code': 313, 'error': 'no topic!'}
					return JsonResponse(result)

			res = make_topic_res02(topic, user, is_self)
			return JsonResponse(res)

		else:

			# v1/topics/<username> 用户全量数据

			category = request.GET.get('category')
			if category in ('tec', 'no-tec'):
				# /v1/topics/<username>?category=[tec|no-tec]

				# 判断是谁在浏览
				if username == visitor_name:
					# 博主自己在访问自己的博客，获取全部数据
					# user_topics = user.topic_set.all()
					user_topics = Topic.objects.filter(author=user, category=category)
				else:
					# 访客来了，非博主本人
					user_topics = Topic.objects.filter(author=user, limit='public', category=category)

				result = make_topics_res(user, user_topics)
				return JsonResponse(result)
			else:
				# v1/topics/<username> 用户全量数据
				# 判断是谁在浏览
				if username == visitor_name:
					# 博主自己在访问自己的博客，获取全部数据
					# user_topics = user.topic_set.all()
					user_topics = Topic.objects.filter(author=user)
				else:
					# 访客来了，非博主本人
					user_topics = Topic.objects.filter(author=user, limit='public')

				result = make_topics_res(user, user_topics)
				return JsonResponse(result)

	elif request.method == 'POST':
		# 创建用户博客数据
		json_str = request.body
		if not json_str:
			result = {'code': 301, 'error': 'Please give me json'}
			return JsonResponse(result)
		json_obj = json.loads(json_str)


		# 获取内容
		title = json_obj.get('title')
		# xss 注入
		import html
		# 进行转义
		title = html.escape(title)


		if not title:
			result = {'code': 302, 'error': 'Please give me title'}
			return JsonResponse(result)

		content = json_obj.get('content')
		if not content:
			result = {'code': 303, 'error': 'Please give me content'}
			return JsonResponse(result)

		# 获取纯文本内容 -- 用于切割文章简介
		content_text = json_obj.get('content_text')
		if not content_text:
			result = {'code': 304, 'error': 'Please give me content_text'}
			return JsonResponse(result)
		# 切割简介
		introduce = content_text[:30]
		limit = json_obj.get('limit')
		if limit not in ('public', 'private'):
			result = {'code': 305, 'error': 'Your limit is wrong'}
			return JsonResponse(result)
		category = json_obj.get('category')
		if category not in ('tec', 'no-tec'):
			result = {'code': 306, 'error': 'Your category is wrong'}
			return JsonResponse(result)

		# 创建数据
		Topic.objects.create(
			title=title, category=category, limit=limit,
			content=content, introduce=introduce, author=request.user
		)
		result = {'code': 200, 'username': request.user.username}
		return JsonResponse(result)

	elif request.method == 'DELETE':
		print(request.body)
		# 博主删除自己的微薄
		# token存储的用户
		author = request.user
		token_author_id = author.username
		# url中传过来的username 必须与token中的用户名相等
		if username != token_author_id:
			result = {'code': 309, 'error': 'You can not do it'}
			return JsonResponse(result)

		# 获取目标
		topic_id = request.GET.get('topic_id')

		delete_topics = Topic.objects.filter(id=int(topic_id))
		if not delete_topics:
			result = {'code': 310, 'error': 'You can not do it!'}
			return JsonResponse(result)

		topic = delete_topics[0]
		# 删除之前要做检查，是不是当前博主的文章
		if topic.author.username != token_author_id:
			result = {'code': 311, 'error': 'You can not do it!!'}
			return JsonResponse(result)

		topic.delete()
		result = {'code': 200}
		return JsonResponse(result)


	return JsonResponse({'code': 200, 'error': 'this is test'})


def make_topic_res02(topic, user, is_self):
	"""
	根据topic对象和userProfile对象，查找topic,返回json对象
	@param topic:
	@param user:
	@param is_self:
	@return:
	"""
	if is_self:
		# 博主自己访问
		# 下一篇文章：取出ID大于当前博客ID的第一个 且 user为当前作者的博客
		next_topic = Topic.objects.filter(id__gt=topic.id, author=user).first()
		# 上一篇文章：取出ID小于当前博客ID的最后一个 且 user为当前作者的博客
		last_topic = Topic.objects.filter(id__lt=topic.id, author=user).last()
	else:
		# 访客访问博主
		# 下一篇文章：取出ID大于当前博客ID的第一个 且 user为当前作者的博客, 且limit='public'
		next_topic = Topic.objects.filter(id__gt=topic.id, author=user, limit='public').first()
		# 上一篇文章：取出ID小于当前博客ID的最后一个 且 user为当前作者的博客, 且limit='public'
		last_topic = Topic.objects.filter(id__lt=topic.id, author=user, limit='public').last()

	# 获取message信息
	# messages = Message.objects.filter(topic_id=topic.id, parent_message=0)
	# list_mes = []
	# for message in messages:
	# 	list_reply = []
	# 	replies = Message.objects.filter(parent_message=message.id)
	# 	for reply in replies:
	# 		dict_reply = {
	# 			'publisher': reply.publisher.username,
	# 			'publisher_avatar': str(reply.publisher.avatar),
	# 			'created_time': reply.created_time.strftime('%Y-%m-%d %H:%M:%S'),
	# 			'content': reply.content,
	# 			'msg_id': reply.id
	# 		}
	# 		list_reply.append(dict_reply)
	#
	# 	dict_mes = {
	# 		'id': message.id,
	# 		'content': message.content,
	# 		'publisher': message.publisher.username,
	# 		'publisher_avatar': str(message.publisher.avatar),
	# 		'reply': list_reply,
	# 		'created_time': message.created_time.strftime('%Y-%m-%d %H:%M:%S')
	# 	}
	# 	list_mes.append(dict_mes)


	all_messages = Message.objects.filter(topic=topic).order_by('-created_time')
	# 所有的留言
	list_parent = []
	# 留言&回复的映射字典
	child_dict = {}
	msg_count = 0
	for mes in all_messages:
		if mes.parent_message == 0:
			# 当前是留言
			list_parent.append(
				{
					'id': mes.id,
					'content': mes.content,
					'publisher': mes.publisher.nickname,
					'publisher_avatar': str(mes.publisher.avatar),
					'reply': [],
					'created_time': mes.created_time.strftime('%Y-%m-%d %H:%M:%S')
				}
			)
			msg_count += 1
		else:
			# 当前是回复
			child_dict.setdefault(mes.parent_message, [])
			child_dict[mes.parent_message].append(
				{
					'publisher': mes.publisher.nickname,
					'publisher_avatar': str(mes.publisher.avatar),
					'created_time': mes.created_time.strftime('%Y-%m-%d %H:%M:%S'),
					'content': mes.content,
					'msg_id': mes.id
				}
			)
			msg_count += 1

	# 合并 msg_list 和 reply_dict
	for _mes in list_parent:
		if _mes['id'] in child_dict:
			_mes['reply'] = child_dict[_mes['id']]


	next_id = next_topic.id if next_topic else None
	next_title = next_topic.title if next_topic else None
	last_id = last_topic.id if last_topic else None
	last_title = last_topic.title if last_topic else None
	res = {'code': 200, 'data': {
		'nickname': user.nickname,
		'title': topic.title,
		'category': topic.category,
		'created_time': topic.created_time.strftime('%Y-%m-%d %H:%M:%S'),
		'content': topic.content,
		'introduce': topic.introduce,
		'author': user.nickname,
		'next_id': next_id,
		'next_title': next_title,
		'last_id': last_id,
		'last_title': last_title,
		'messages': list_parent,
		'messages_count': msg_count,
		}}
	return res


def make_topics_res(user, user_topics):
	list_topics = []
	for topic in user_topics:
		dict_topic = {
			'id': topic.id,
			'title': topic.title,
			'category': topic.category,
			'created_time': topic.created_time.strftime('%Y-%m-%d %H:%M:%S'),
			'content': topic.content,
			'introduce': topic.introduce,
			'author': topic.author.nickname
		}
		list_topics.append(dict_topic)
	result = {
		'code': 200,
		'data': {
			'nickname': user.nickname,
			'topics': list_topics
		}
	}
	return result


















