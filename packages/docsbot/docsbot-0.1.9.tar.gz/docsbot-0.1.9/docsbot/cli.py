#!/usr/bin/env python3
import argparse
import os
import json
import random
import string
import datetime
from prettytable import PrettyTable
from base import Base

from config import CONFIG

import nltk
if CONFIG.env.OPENAI_PROXY:
    nltk.set_proxy(CONFIG.env.OPENAI_PROXY)


class ChatBase:
    def __init__(self):
        self.bases_file = CONFIG.bases_file
        if os.path.exists(self.bases_file):
            with open(self.bases_file, 'r') as f:
                self.base = json.load(f)
        else:
            self.base = {}

    def save_base(self):
        with open(self.bases_file, 'w') as f:
            json.dump(self.base, f)

    def addbase(self, path):
        if os.path.isdir(path):
            base_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            base_id = f"base000{base_id.lower()}"
            self.base[base_id] = {'location': path}
            base = Base(base_id)
            docs = base.add(path)
            if not docs:
                print("No valid documents found in the directory")
                return
            self.base[base_id]['file_count'] = len(docs)
            self.base[base_id]['files'] = docs
            self.base[base_id]['vector_store_type'] = base.vector_store_type
            # created is the time the base was created
            self.base[base_id]['created'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_base()
            print(f"Added {path} to base {base_id},  {len(docs)} document(s)!")
        else:
            print("Invalid directory")

    def listbase(self):
        table = PrettyTable()
        table.field_names = ["ID", "Location", "Count", "Store", "Created"]
        for _id, base in self.base.items():
            table.add_row([_id, base['location'],
                           "N/A" if 'file_count' not in base else f"{base['file_count']} files",
                           "N/A" if 'vector_store_type' not in base else base['vector_store_type'],
                           "N/A" if 'created' not in base else base['created']
                           ])
        print(table)

    def deletebase(self, base_ids):
        for base_id in base_ids:
            if base_id in self.base:
                base = Base(base_id, self.base[base_id]['vector_store_type'])
                base.delete()
                del self.base[base_id]
                self.save_base()
                print(f"Deleted base with ID {base_id}")
            else:
                print(f"Invalid base ID {base_id}")


    def _pretty_print_query_result(self, data):
        print(f"查询: {data['query']}")
        if data['source_documents']:
            print(f"结果: {data['result']}")
            print("来源文件：")
        else:
            print("没有找到相关文件")
            return
        # 根据来源整理文档内容
        source_dict = {}
        for doc in data['source_documents']:
            content = doc.page_content.replace('\n', ' ')
            source = doc.metadata['source']
            if source in source_dict:
                source_dict[source].append(content)
            else:
                source_dict[source] = [content]

        # 打印整理后的文档内容
        for i, (source, contents) in enumerate(source_dict.items()):
            print(f"{i + 1}. 来源：{source}")
            for j, content in enumerate(contents, start=1):
                print(f"   内容{j}.：{content}")


    def query(self, base_id, question):
        if base_id in self.base:
            # Here you can implement the actual querying process
            base = Base(base_id, self.base[base_id]['vector_store_type'])
            self._pretty_print_query_result(base.query(question))
            print(f"Queried base with ID {base_id} with query {question}")
        else:
            print("Invalid base ID")


    def test(self):
        from qdrant_client import QdrantClient
        client = QdrantClient(url='http://127.0.0.1:6333')
        print(client.get_collections())
        print(os.environ)




def main():
    chat_base = ChatBase()

    parser = argparse.ArgumentParser(prog='chatbase')
    subparsers = parser.add_subparsers(dest='command')

    parser_addbase = subparsers.add_parser('addbase')
    parser_addbase.add_argument('path', type=str)

    parser_listbase = subparsers.add_parser('listbase')

    parser_deletebase = subparsers.add_parser('deletebase')
    parser_deletebase.add_argument('base_ids', nargs='+')

    parser_query = subparsers.add_parser('query')
    parser_query.add_argument('base_id', type=str)
    parser_query.add_argument('query', type=str)

    parser_query = subparsers.add_parser('test')

    args = parser.parse_args()

    if args.command == 'addbase':
        chat_base.addbase(args.path)
    elif args.command == 'listbase':
        chat_base.listbase()
    elif args.command == 'deletebase':
        chat_base.deletebase(args.base_ids)
    elif args.command == 'query':
        chat_base.query(args.base_id, args.query)
    elif args.command == 'test':
        chat_base.test()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
