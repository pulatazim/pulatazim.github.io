import os

from github import Github, GithubException


def get_github_repo():
    """
    Github repo obyektini qaytaradi
    .env dan TOKEN va REPO_NAME o'qiydi.
    """
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO")

    g = Github(token)
    repo = g.get_repo(repo_name)  # pyright: ignore[reportArgumentType]
    return repo


def read_file(path, content, message):
    """Github dan fayl o'qiydi"""

    repo = get_github_repo()
    file = repo.get_contents(path)
    return file.decoded_content.decode("utf-8")  # pyright: ignore[reportAttributeAccessIssue]


def write_file(path, content, message):
    """Githubga yangi fayl yozadi yoki mavjudini yangilaydi"""

    repo = get_github_repo()
    try:
        # Fayl mavjudligini tekshirish
        existing = repo.get_contents(path)

        # Fayl mavjud bo'lsa yangilash
        repo.update_file(
            path=path,
            message=message,
            content=content,
            sha=existing.sha,  # pyright: ignore[reportAttributeAccessIssue]
        )
    except GithubException:
        # Fayl mavjud emas, yangi yaratish
        repo.create_file(path=path, message=message, content=content)


def delete_file(path, message):
    """Github dan fayl o'chiradi"""

    repo = get_github_repo()

    # Fayl mavjudligini tekshirish
    existing = repo.get_contents(path)

    # Fayl mavjud bo'lsa o'chirish
    repo.delete_file(
        path=path,
        message=message,
        sha=existing.sha,  # pyright: ignore[reportAttributeAccessIssue]
    )


def list_files(folder):
    """Github dagi fayllarni ro'yxatini qaytaradi"""

    repo = get_github_repo()

    # Fayllarni ro'yxatini olish
    contents = repo.get_contents(folder)
    files = [file.path for file in contents if file.name.endswith(".md")]  # pyright: ignore[reportGeneralTypeIssues]

    # Fayllarni ro'yxatini qaytarish
    return files
