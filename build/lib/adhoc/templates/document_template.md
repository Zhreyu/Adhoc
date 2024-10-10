# Project Documentation

## Codebase Summary

{{ codebase_summary }}

## Change Explanations

{% for item in explanations %}
### File: {{ item.file_path }}

{% if item.commit_message %}
**Commit Message:** {{ item.commit_message }}
{% endif %}

**Explanation:**

{{ item.explanation }}

---

{% endfor %}
