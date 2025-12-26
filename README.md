# My Own Collection

This is a custom Ansible collection created for educational purposes.

## Modules

### create_file
Creates a text file with specified content on the remote host.

## Roles

### create_file_role
A simple role that uses the create_file module with configurable parameters.

## Usage

```yaml
- name: Use create_file module
  my_namespace.yandex_cloud_elk.create_file:
    path: "/path/to/file.txt"
    content: "File content"
```

## License
GPL-3.0-or-later
