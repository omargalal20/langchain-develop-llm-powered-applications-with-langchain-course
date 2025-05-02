import re


def clean_markdown(markdown):
    # Remove duplicated sections like "Contact" and redundant lines
    markdown = re.sub(r"\*\*Connect with experts in your field\*\*.*?\[Join for free\]\(.*?\)", "", markdown,
                      flags=re.DOTALL)
    markdown = re.sub(r"\[Log in\]\(.*?\)", "", markdown)

    # Remove broken image references
    markdown = re.sub(r"!\[\]\(<Base64-Image-Removed>\)", "", markdown)
    markdown = re.sub(r"\!\[.*?\]\(<Base64-Image-Removed>\)", "", markdown)

    # Remove unnecessary links like Home and Institution headers
    markdown = re.sub(r"- \[Home\]\(.*?\)\n- \[.*?\]\(.*?\)", "", markdown, flags=re.DOTALL)

    # Clean up redundant Publication lines
    markdown = re.sub(r"Publications \(\d+\)", "## Publications", markdown)

    # Remove duplicate and unnecessary text in Publications section
    markdown = re.sub(r"\[View\]\(.*?\)", "", markdown)
    markdown = re.sub(r"Full-text available", "", markdown)

    # Remove publication authors links if redundant
    markdown = re.sub(r"- \[!\[.*?\]\(.*?\)\]\(.*?\)", "", markdown)

    # Clean up line breaks and empty lines
    markdown = re.sub(r"\n{2,}", "\n\n", markdown).strip()

    return markdown
