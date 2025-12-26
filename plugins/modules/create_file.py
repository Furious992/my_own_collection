#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Student <student@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: create_file

short_description: Creates a text file with specified content.

version_added: "1.0.0"

description: This module creates a text file on the remote host at a given path with the specified content.

options:
    path:
        description: The absolute path where the file should be created.
        required: true
        type: path
    content:
        description: The content to write into the file.
        required: true
        type: str

author:
    - Student (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Create a file with welcome message
- name: Create a welcome file
  my_namespace.yandex_cloud_elk.create_file:
    path: /tmp/welcome.txt
    content: "Hello from Ansible!"

# Create a configuration file
- name: Create a config file
  my_namespace.yandex_cloud_elk.create_file:
    path: /etc/app/config.conf
    content: |
      parameter1=value1
      parameter2=value2
'''

RETURN = r'''
file_path:
    description: The path to the created file.
    type: str
    returned: always
    sample: '/tmp/welcome.txt'
content:
    description: The content that was written to the file.
    type: str
    returned: always
    sample: 'Hello from Ansible!'
changed:
    description: Indicates if the file was created or modified.
    type: bool
    returned: always
    sample: true
'''

import os
from ansible.module_utils.basic import AnsibleModule

def run_module():
    # Определяем аргументы модуля
    module_args = dict(
        path=dict(type='path', required=True),
        content=dict(type='str', required=True)
    )

    # Задаем начальные значения для результата
    result = dict(
        changed=False,
        file_path='',
        content=''
    )

    # Создаем объект AnsibleModule
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Извлекаем параметры
    file_path = module.params['path']
    file_content = module.params['content']

    # Сохраняем параметры в результат
    result['file_path'] = file_path
    result['content'] = file_content

    # Режим проверки (Check Mode): ничего не меняем, только сообщаем, изменилось бы ли состояние
    if module.check_mode:
        # Проверяем, существует ли файл и совпадает ли его содержимое
        if not os.path.exists(file_path):
            result['changed'] = True
        else:
            try:
                with open(file_path, 'r') as f:
                    existing_content = f.read()
                if existing_content != file_content:
                    result['changed'] = True
            except IOError:
                module.fail_json(msg="Failed to read existing file for comparison", **result)
        module.exit_json(**result)

    # ОСНОВНАЯ ЛОГИКА МОДУЛЯ
    try:
        # Читаем текущий файл, если он существует
        file_exists = os.path.exists(file_path)
        existing_content = ''
        if file_exists:
            with open(file_path, 'r') as f:
                existing_content = f.read()

        # Сравниваем содержимое
        if not file_exists or existing_content != file_content:
            # Содержимое разное или файла нет — нужно записать
            with open(file_path, 'w') as f:
                f.write(file_content)
            result['changed'] = True
        else:
            # Файл уже существует с нужным содержимым — ничего не делаем
            result['changed'] = False

    except Exception as e:
        module.fail_json(msg=f"Failed to create/write file: {str(e)}", **result)

    # Возвращаем успешный результат
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
EOF
