"""
This program extracts information via StackOverflow API
We will extract all questions from specific Tags.
After getting the questions we will get question_id and extract the answers calling a different API endpoint.


API returns information in gzip format hence we need to decompressed it for reading purposes.
Example CURL:
$URL = 'http://api.stackexchange.com/2.2/questions'
curl --compressed -H "Accept-Encoding: gzip" -X GET '${URL}?page_number=1&pagesize=25&order=desc&sort=activity&tagged=amp-html&site=stackoverflow&run=true'

"""
import json
import time
import string
import requests
from answer import Answer
from item import Item
from formatter import Formatter
from question import Question

PAGE_NUMBER = 1
PAGE_SIZE = 25
MAX_REQUESTS = 25


def process_question_items(content):
    """
    Process response and generate dictionary with questions and URL
    :param content:
    :return:
    """
    questions = list()
    if "items" in content:
        items = content["items"]
        for item in items:
            question = Question()
            question.id = item['question_id']
            question.title = item['title']
            question.link = item['link']
            question.tags = item['tags']
            question.is_answered = item['is_answered']
            question.answer_count = item['answer_count']
            questions.append(question)
    return questions


def process_question_body(content):
    """

    :param content:
    :param beautify:
    :return:
    """
    question_body = None
    if "items" in content:
        items = content["items"]
        for item in items:
            question_body = item['body']
    return question_body


def process_answer_items(content, beautify=True):
    """
    Process response and generate dictionary with questions and URL
    :param content:
    :param beautify:
    :return:
    """
    answers = list()
    if "items" in content:
        items = content["items"]
        for item in items:
            answer = Answer()
            answer.id = item['answer_id']
            answer.body = item['body']
            answer.is_accepted = item['is_accepted']
            if beautify:
                formatter = Formatter()
                answer.body_clean = formatter.beautify(answer.body)
            answers.append(answer)
    return answers


def get_questions():
    """
    Will call Stackoverflow API. Will check has_more value and if true will call following page. Starts calling page 1
    This will get all questions from specific tag and will return a list of objects containing each question
    :return:
    """
    url = 'http://api.stackexchange.com/2.2/questions'
    max_requests = MAX_REQUESTS
    page_number = PAGE_NUMBER
    page_size = PAGE_SIZE
    next_page = 'page={}&pagesize={}'.format(page_number, page_size)
    params = '?' + next_page + '&order=desc&sort=activity&tagged=amp-html&site=stackoverflow&run=true'
    try:
        total_questions = list()

        while True:
            if page_number > max_requests:
                print '|Max requests reached! {}'.format(max_requests)
                break

            res = requests.get(url + params)
            if res.status_code == 200:
                content = json.loads(res.content)
                # print json.dumps(content, indent=4)
                questions = process_question_items(content)
                total_questions.extend(questions)
                questions[:] = []
                if not content["has_more"]:
                    break
                else:
                    page_number += 1
                    params = string.replace(params, next_page, 'page={}&pagesize={}'.format(page_number, page_size))
                    next_page = 'page={}&pagesize={}'.format(page_number, page_size)
            else:
                print res.status_code
                break
            time.sleep(1)
        return total_questions

    except ValueError, e:
        print e


def get_question_body(question_id):
    """

    curl --compressed -H "Accept-Encoding: gzip" -X GET 'https://api.stackexchange.com/2.2/questions/37745529?site=stackoverflow&filter=withbody'
    :param question_id:
    :param beautify:
    :return:
    """

    if not question_id:
        print 'No question id'
        return

    url = 'http://api.stackexchange.com/2.2/questions/' + str(question_id) + '?site=stackoverflow&filter=withbody'

    try:
        res = requests.get(url)
        question_body = None
        if res.status_code == 200:
            content = json.loads(res.content)
            # print json.dumps(content, indent=4)
            question_body = process_question_body(content)
        else:
            print 'HTTP Error: {} reading question body'.format(res.status_code)

        return question_body

    except ValueError, e:
        print e


def get_answers(question_id):
    """

    curl --compressed -H "Accept-Encoding: gzip" -X GET 'https://api.stackexchange.com/2.2/questions/37745529/answers?&site=stackoverflow&filter=withbody'
    :param question_id:
    :return:
    """

    url = 'http://api.stackexchange.com/2.2/questions/' + str(question_id) + '/answers'
    max_requests = MAX_REQUESTS
    page_number = PAGE_NUMBER
    page_size = PAGE_SIZE
    next_page = 'page={}&pagesize={}'.format(page_number, page_size)
    params = '?' + next_page + '&order=desc&sort=activity&site=stackoverflow&filter=withbody'

    if not question_id:
        print 'No question id'
        return

    try:
        answer_list = list()
        while True:
            try:
                if page_number > max_requests:
                    print '|Max requests reached! {}'.format(max_requests)
                    break

                res = requests.get(url + params)
                if res.status_code == 200:
                    content = json.loads(res.content)
                    # print json.dumps(content, indent=4)
                    answers = process_answer_items(content)
                    answer_list.extend(answers)
                    answers[:] = []
                    if not content["has_more"]:
                        break
                    else:
                        page_number += 1
                        params = string.replace(params, next_page, 'page={}&pagesize={}'.format(page_number, page_size))
                        next_page = 'page={}&pagesize={}'.format(page_number, page_size)
                else:
                    print res.status_code
                    break
                time.sleep(1)

            except requests.exceptions.ConnectionError:
                continue

        return answer_list


    except ValueError, e:
        print e


def main():
    """
    Get all questions, for each question get all the answers.
    :return:
    """

    print '|Getting questions from Stackoverflow. Please wait...|'
    items = list()
    questions = get_questions()
    print '|Total questions: {} |'.format(len(questions))
    if questions:
        for question in questions:
            formatter = Formatter()
            question.body = get_question_body(question.id)
            question.body_clean = formatter.beautify(question.body)
            question.answers = get_answers(question.id)             # Iterate over each question and get all answers

    print '|Display information'
    for question in questions:
        item = Item()
        if question.title and question.body_clean:
            item.text = question.title + ' ' + question.body_clean

        if question.answers:
            for answer in question.answers:
                item.text += ' ' + answer.body_clean
                item.text.rstrip('\r\n')
        items.append(item)
        print '<<'
        print item.text



if __name__ == '__main__':
    main()
