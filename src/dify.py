import json
import re


def print_dict(dict):
    print(json.dumps(dict, indent=4, sort_keys=True, ensure_ascii=False))


# 拆為標題和內容
def get_markdown_headers(markdown_text):
    pattern = r'^#{1,6} .*?$'
    headers = re.findall(pattern, markdown_text, re.MULTILINE)
    return headers


# main
def main_split_header_chapter(input: str) -> dict:
    splited_content = re.split('^#.*$', input, flags=re.MULTILINE)[1:]
    for i in range(len(splited_content)):
        splited_content[i] = splited_content[i].strip()
    return {
        'headers': get_markdown_headers(input),
        'chapters_content': splited_content,
    }


# 章節內容拆段落(紀錄段落數)
def main_chapters_to_paragraphs(chapters_content: list[str]) -> dict:
    chapter_paragraphs_num = []
    all_paragraphs = []
    for chapter in chapters_content:
        paragraphs = chapter.split('\n\n')
        chapter_paragraphs_num.append(len(paragraphs))
        all_paragraphs.extend(paragraphs)
    return {
        'all_paragraphs': all_paragraphs,
        'chapter_paragraphs_num': chapter_paragraphs_num,
    }


# 迭代
def fake_loop(all_paragraphs: list[str]) -> list:
    result = [paragraph + ' 已翻譯' for paragraph in all_paragraphs]
    return {'output': result}


# 合併中英文段落
def main_merge_paragraphs(
    all_paragraphs: list[str], translated_all_paragraphs: list[str]
) -> dict:
    merged_paragraphs = []
    for i in range(len(all_paragraphs)):
        merged_paragraphs.append(
            all_paragraphs[i] + '\n中文翻譯\n' + translated_all_paragraphs[i]
        )

    return {
        'merged_paragraphs': merged_paragraphs,
    }


# 拼接回章節的段落
def main_concact_paragraphs(
    merged_paragraphs: list[str], chapter_paragraphs_num: list[int]
) -> dict:
    merged_chapters_content = []
    start_index = 0
    for num in chapter_paragraphs_num:
        chapter_paragraphs_list = merged_paragraphs[start_index : start_index + num]
        start_index = start_index + num
        chapter_content = '\n\n'.join(chapter_paragraphs_list)
        merged_chapters_content.append(chapter_content)
    return {
        'merged_chapters_content': merged_chapters_content,
    }


# 合併標題和內容
def main_merge_header_content(
    headers: list[str], merged_chapters_content: list[str]
) -> dict:
    result = ''
    for i, header in enumerate(headers):
        result = result + '\n' + header + '\n\n' + merged_chapters_content[i] + '\n'
    result = result.strip() + '\n'
    return {
        'result': result,
    }


if __name__ == '__main__':
    with open('pdf/123.md', 'r', encoding='utf-8') as f:
        input = f.read()
    a = main_split_header_chapter(input)
    # print_dict(a)

    b = main_chapters_to_paragraphs(a['chapters_content'])
    # print_dict(b)

    c = fake_loop(b['all_paragraphs'])
    # print_dict(c)

    d = main_concact_paragraphs(c['output'], b['chapter_paragraphs_num'])
    # print_dict(d)

    e = main_merge_header_content(a['headers'], d['translated_chapters_content'])
    print_dict(e)
